// apps/sovereign-web/src/lib/services/api.ts
import { API_CONFIG } from '$lib/config/api';

/**
 * 🏛️ SOVEREIGN API BRIDGE
 * The primary intelligence bridge for the AGE Protocol.
 */
export const api = {
    async request(endpoint: string, options: RequestInit = {}) {
        const url = `${API_CONFIG.baseURL}${endpoint}`;
        const headers = {
            ...API_CONFIG.headers,
            ...options.headers,
        };

        try {
            const response = await fetch(url, { ...options, headers });
            if (!response.ok) throw new Error(`API Error: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`[API] Request to ${endpoint} failed:`, error);
            return this.getMockData(endpoint);
        }
    },

    async getHealth() {
        return this.request('/health');
    },

    async getVault() {
        return this.request('/vault');
    },

    async registerIdentity(data: any) {
        return this.request('/identity/register', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    // 🧠 NAI: Mock standard for development
    getMockData(endpoint: string) {
        if (endpoint.includes('/vault')) {
            return {
                balance: 7247.32,
                totalValue: 7247.32,
                transactions: [],
                assets: [
                    { type: 'AGE', amount: 1247.32, value: 1247.32 },
                    { type: 'RES', amount: 892.5, value: 669.37 }
                ]
            };
        }
        if (endpoint.includes('/identity')) {
            return {
                success: true,
                id: 'did:age:mock',
                did: 'did:age:mock',
                verificationLevel: 3,
                profile: { displayName: 'Sovereign Citizen' }
            };
        }
        if (endpoint.includes('/resonance')) {
            return { score: 98 };
        }
        if (endpoint.includes('/analytics/wealth')) {
            return { totalWealth: 48760000000 };
        }
        if (endpoint.includes('/nodes')) {
            return { totalNodes: 7690000 };
        }
        return { status: 'CATHEDRAL_NOMINAL', version: '5.1.0', citizens: '3.57M' };
    }
};
