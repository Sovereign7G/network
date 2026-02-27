import type { A2UIFrame, A2UIComponent } from './types';

class NAIEngine {
    currentFrame = $state<A2UIFrame | null>(null);
    isMeshConnected = $state(false);
    isTurbulent = $state(false);

    lastFrameTime = 0;

    pushFrame(frame: A2UIFrame) {
        const now = Date.now();
        const isCritical = frame.priority === 'high' ||
            frame.priority === 'critical' ||
            frame.components.some(c => c.type === 'privacy' || c.type === 'verification');

        // 🧠 NAI: Prioritized Culling
        // Cull standard frames if they exceed 60fps (16ms) to preserve UI responsiveness
        if (!isCritical && (now - this.lastFrameTime) < 16) {
            return;
        }

        this.lastFrameTime = now;
        this.currentFrame = frame;

        // 🧠 NAI: Mesh State Detection
        if (frame.agentId === 'SYSTEM_MESH' && frame.metadata?.condition === 'turbulence') {
            this.isTurbulent = true;
        } else if (frame.agentId === 'SOPHIA_GOV' && frame.metadata?.condition === 'stable') {
            this.isTurbulent = false;
        }
    }

    /// 🧠 NAI: Mesh Inbound Bridge
    /// Handles frames received via the P2P Mesh (e.g., from Mobile Sentinel)
    injectMeshFrame(frame: A2UIFrame) {
        this.isMeshConnected = true;
        this.pushFrame(frame);
    }

    getComponents<T extends A2UIComponent>(type: T['type']): T[] {
        if (!this.currentFrame) return [];
        return this.currentFrame.components.filter(c => c.type === type) as T[];
    }

    clear() {
        this.currentFrame = null;
    }
}

export const naiEngine = new NAIEngine();
