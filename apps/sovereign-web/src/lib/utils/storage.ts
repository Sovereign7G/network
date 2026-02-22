import { browser } from '$app/environment';

export function loadFromStorage<T>(key: string, defaultValue: T): T {
    if (!browser) return defaultValue;

    try {
        const saved = localStorage.getItem(key);
        if (saved) {
            return JSON.parse(saved) as T;
        }
    } catch (e) {
        console.error(`Failed to load ${key} from localStorage:`, e);
    }

    return defaultValue;
}

export function saveToStorage<T>(key: string, value: T): void {
    if (!browser) return;

    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
        console.error(`Failed to save ${key} to localStorage:`, e);
    }
}
