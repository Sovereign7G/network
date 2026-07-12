export class WebGLPipelinedEngine {
    constructor(canvas, model) {
        this.gl = canvas.getContext('webgl2');
        if (!this.gl) throw new Error('WebGL2 not supported');

        this.numLayers = model.get_num_layers();
        this.tileWidth = model.get_tile_width();
        this.tileHeight = model.get_tile_height();

        // 1. Compile and link shader program
        this.program = this.compileProgram();
        this.gl.useProgram(this.program);

        // 2. Create Texture Array (width=4096, height=16, depth=48)
        const gl = this.gl;
        this.weightTextureArray = gl.createTexture();
        gl.bindTexture(gl.TEXTURE_2D_ARRAY, this.weightTextureArray);
        
        // Allocate storage
        gl.texImage3D(gl.TEXTURE_2D_ARRAY, 0, gl.RGBA8, this.tileWidth, this.tileHeight, this.numLayers, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
        
        // Upload layers
        const packedTextures = model.get_packed_weight_textures();
        for (let i = 0; i < packedTextures.length; i++) {
            gl.texSubImage3D(gl.TEXTURE_2D_ARRAY, 0, 0, 0, i, this.tileWidth, this.tileHeight, 1, gl.RGBA, gl.UNSIGNED_BYTE, packedTextures[i]);
        }
        
        gl.texParameteri(gl.TEXTURE_2D_ARRAY, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
        gl.texParameteri(gl.TEXTURE_2D_ARRAY, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
        
        // Bind to unit 1
        const loc = this.gl.getUniformLocation(this.program, 'u_weights');
        this.gl.uniform1i(loc, 1);

        // 3. Create tile texture (reused per inference, bound to texture unit 0)
        const tileData = new Uint8Array(this.tileWidth * this.tileHeight);
        this.tileTexture = this.createTexture2D(tileData, true);
        const tileLoc = this.gl.getUniformLocation(this.program, 'u_tiles');
        this.gl.uniform1i(tileLoc, 0);

        // 4. Allocate output buffer
        this.outputBuffer = new Uint8Array(this.tileWidth * this.tileHeight);
    }

    createTexture2D(data, isInteger = false) {
        const gl = this.gl;
        const texture = gl.createTexture();
        gl.bindTexture(gl.TEXTURE_2D, texture);
        
        if (isInteger) {
            gl.texImage2D(gl.TEXTURE_2D, 0, gl.R8UI, this.tileWidth, this.tileHeight, 0, gl.RED_INTEGER, gl.UNSIGNED_BYTE, data);
        } else {
            gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, this.tileWidth, this.tileHeight, 0, gl.RGBA, gl.UNSIGNED_BYTE, data);
        }
        
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
        return texture;
    }

    compileProgram() {
        const gl = this.gl;

        const vsSource = `#version 300 es
            in vec2 position;
            void main() {
                gl_Position = vec4(position, 0.0, 1.0);
            }
        `;

        const fsSource = `#version 300 es
            precision highp float;
            precision highp usampler2D;
            precision highp sampler2DArray;

            uniform usampler2D u_tiles;
            uniform sampler2DArray u_weights;
            out uint fragColor;

            int popcount(uint x) {
                int count = 0;
                for (int i = 0; i < 8; i++) {
                    if ((x & (1u << i)) != 0u) count++;
                }
                return count;
            }

            void main() {
                ivec2 coord = ivec2(gl_FragCoord.xy);
                if (coord.x >= 4096 || coord.y >= 16) {
                    fragColor = 0u;
                    return;
                }
                uint tile = texelFetch(u_tiles, coord, 0).r;
                int total_score = 0;
                for (int layer = 0; layer < 48; layer++) {
                    vec4 packed = texelFetch(u_weights, ivec3(coord, layer), 0);
                    uint w_pos = uint(packed.r * 255.0 + 0.5);
                    uint w_neg = uint(packed.g * 255.0 + 0.5);
                    uint pos_sim = ~(tile ^ w_pos) & 0xFFu;
                    uint neg_sim = ~(tile ^ w_neg) & 0xFFu;
                    total_score += popcount(pos_sim) - popcount(neg_sim);
                }
                fragColor = uint(total_score);
            }
        `;

        const vs = gl.createShader(gl.VERTEX_SHADER);
        gl.shaderSource(vs, vsSource);
        gl.compileShader(vs);
        if (!gl.getShaderParameter(vs, gl.COMPILE_STATUS)) {
            throw new Error(`Vertex Shader compile failed: ${gl.getShaderInfoLog(vs)}`);
        }

        const fs = gl.createShader(gl.FRAGMENT_SHADER);
        gl.shaderSource(fs, fsSource);
        gl.compileShader(fs);
        if (!gl.getShaderParameter(fs, gl.COMPILE_STATUS)) {
            throw new Error(`Fragment Shader compile failed: ${gl.getShaderInfoLog(fs)}`);
        }

        const program = gl.createProgram();
        gl.attachShader(program, vs);
        gl.attachShader(program, fs);
        gl.linkProgram(program);
        if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
            throw new Error(`Program link failed: ${gl.getProgramInfoLog(program)}`);
        }
        return program;
    }

    runInference(tiles) {
        const gl = this.gl;
        gl.useProgram(this.program);

        // 1. Upload input tiles
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, this.tileTexture);
        gl.texSubImage2D(gl.TEXTURE_2D, 0, 0, 0, this.tileWidth, this.tileHeight, gl.RED_INTEGER, gl.UNSIGNED_BYTE, tiles);

        // 2. Bind textures
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, this.tileTexture);
        
        gl.activeTexture(gl.TEXTURE1);
        gl.bindTexture(gl.TEXTURE_2D_ARRAY, this.weightTextureArray);

        // 3. Render
        const buffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
            -1, -1,  1, -1, -1,  1,
            -1,  1,  1, -1,  1,  1,
        ]), gl.STATIC_DRAW);

        const posAttr = gl.getAttribLocation(this.program, "position");
        gl.enableVertexAttribArray(posAttr);
        gl.vertexAttribPointer(posAttr, 2, gl.FLOAT, false, 0, 0);

        gl.viewport(0, 0, this.tileWidth, this.tileHeight);
        gl.drawArrays(gl.TRIANGLES, 0, 6);

        // 4. Read result from red channel
        gl.readPixels(0, 0, this.tileWidth, this.tileHeight, gl.RED, gl.UNSIGNED_BYTE, this.outputBuffer);
        return this.outputBuffer;
    }
}
