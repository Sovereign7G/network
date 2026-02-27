interface ValidationResult {
    valid: boolean;
    errors: string[];
}

interface AddressValidationResult extends ValidationResult {
    network?: 'ethereum' | 'bitcoin' | 'solana';
}

function validateAddress(address: string): AddressValidationResult {
    const result: AddressValidationResult = { valid: false, errors: [] };

    // Ethereum (0x followed by 40 hex chars)
    if (/^0x[a-fA-F0-9]{40}$/.test(address)) {
        result.valid = true;
        result.network = 'ethereum';
        return result;
    }

    // Bitcoin (1 or 3 followed by 25-34 chars)
    if (/^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$/.test(address)) {
        result.valid = true;
        result.network = 'bitcoin';
        return result;
    }

    // Solana (base58, 32-44 chars)
    if (/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(address)) {
        result.valid = true;
        result.network = 'solana';
        return result;
    }

    result.errors.push('Invalid address format');
    return result;
}

function validateAmount(
    amount: number,
    min: number = 0,
    max: number = Infinity
): ValidationResult {
    const result: ValidationResult = { valid: true, errors: [] };

    if (isNaN(amount) || !isFinite(amount)) {
        result.valid = false;
        result.errors.push('Amount must be a finite number');
    }

    if (amount < min) {
        result.valid = false;
        result.errors.push(`Amount must be at least ${min}`);
    }

    if (amount > max) {
        result.valid = false;
        result.errors.push(`Amount cannot exceed ${max}`);
    }

    return result;
}

function validateEmail(email: string): ValidationResult {
    const result: ValidationResult = { valid: false, errors: [] };

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(email)) {
        result.errors.push('Invalid email format');
        return result;
    }

    result.valid = true;
    return result;
}
