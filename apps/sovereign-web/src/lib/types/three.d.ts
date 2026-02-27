declare module 'three' {
    export class Scene { add(obj: any): void; }
    export class PerspectiveCamera {
        constructor(a: number, b: number, c: number, d: number);
        position: any;
        lookAt(x: number, y: number, z: number): void;
        aspect: number;
        updateProjectionMatrix(): void;
    }
    export class WebGLRenderer {
        constructor(opts?: any);
        setSize(w: number, h: number): void;
        domElement: any;
        render(s: any, c: any): void;
        dispose(): void;
    }
    export class Group {
        add(obj: any): void;
        children: any[];
    }
    export class AmbientLight { constructor(c: any, i: any); }
    export class DirectionalLight {
        constructor(c: any, i: any);
        position: any;
    }
    export class PlaneGeometry { constructor(a: any, b: any, c: any, d: any); }
    export class MeshPhongMaterial { constructor(opts: any); }
    export class Mesh {
        constructor(g: any, m: any);
        rotation: any;
        position: any;
    }
    export class GridHelper {
        constructor(a: any, b: any, c: any, d: any);
        position: any;
    }
    export class BoxGeometry { constructor(a: any, b: any, c: any); }
    export class Object3D {
        position: any;
    }
}
