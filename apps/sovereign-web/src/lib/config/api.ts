// apps/sovereign-web/src/lib/config/api.ts
// CRITICAL: Point to the backend intelligence standard

export const API_CONFIG = {
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000/api',
    wsURL: import.meta.env.VITE_WS_URL || 'ws://localhost:3000',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
    retryAttempts: 3
};
