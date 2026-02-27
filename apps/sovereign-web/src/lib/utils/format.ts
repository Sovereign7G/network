type Currency = 'USD' | 'EUR' | 'GBP' | 'AGE' | 'SYND';

interface FormatOptions {
    decimals?: number;
    currency?: Currency;
    locale?: string;
    compact?: boolean;
}

function formatCurrency(
    amount: number,
    options: FormatOptions = {}
): string {
    const {
        decimals = 2,
        currency = 'USD',
        locale = 'en-US',
        compact = false
    } = options;

    if (compact && amount >= 1_000_000) {
        return `${(amount / 1_000_000).toFixed(1)}M`;
    }

    if (compact && amount >= 1_000) {
        return `${(amount / 1_000).toFixed(1)}K`;
    }

    return new Intl.NumberFormat(locale, {
        style: currency === 'AGE' || currency === 'SYND' ? 'decimal' : 'currency',
        currency: currency === 'USD' || currency === 'EUR' || currency === 'GBP' ? currency : undefined,
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(amount);
}

function formatPercentage(
    value: number,
    decimals: number = 2
): string {
    return `${(value * 100).toFixed(decimals)}%`;
}

function formatTime(ms: number): string {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d`;
    if (hours > 0) return `${hours}h`;
    if (minutes > 0) return `${minutes}m`;
    return `${seconds}s`;
}
