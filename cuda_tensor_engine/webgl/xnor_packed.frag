#version 300 es
precision highp usampler2D;
precision highp sampler2D;

// Inputs
uniform usampler2D u_tiles;         // Input tiles (4096×16, uint8)
uniform sampler2D u_weights[48];    // 48 packed RG textures (R=pos, G=neg)

// Output
out uint fragColor;

void main() {
    ivec2 coord = ivec2(gl_FragCoord.xy);
    
    // Clamp to texture bounds
    if (coord.x >= 4096 || coord.y >= 16) {
        fragColor = 0u;
        return;
    }
    
    // Fetch input tile once
    uint tile = texelFetch(u_tiles, coord, 0).r;
    
    // Accumulate across all 48 layers
    uint total_score = 0u;
    for (int layer = 0; layer < 48; layer++) {
        // Fetch packed RG texture
        vec4 packed = texelFetch(u_weights[layer], coord, 0);
        
        // Unpack: R = positive mask, G = negative mask
        uint w_pos = uint(packed.r * 255.0 + 0.5);
        uint w_neg = uint(packed.g * 255.0 + 0.5);
        
        // XNOR: ~(tile ^ weight)
        uint pos_sim = ~(tile ^ w_pos) & 0xFFu;
        uint neg_sim = ~(tile ^ w_neg) & 0xFFu;
        
        // Popcount and accumulate
        total_score += uint(bitCount(pos_sim) - bitCount(neg_sim));
    }
    
    fragColor = total_score;
}
