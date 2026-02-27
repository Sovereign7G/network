interface HashResult {
    algorithm: 'sha256' | 'sha512';
    hash: string;
    salt?: string;
    iterations?: number;
}

interface KeyPair {
    publicKey: string;
    privateKey: string;
    algorithm: 'ed25519' | 'secp256k1';
}

async function hashData(
    data: string | Uint8Array,
    algorithm: 'sha256' | 'sha512' = 'sha256',
    salt?: string
): Promise<HashResult> {
    const encoder = new TextEncoder();
    const dataBytes = typeof data === 'string' ? encoder.encode(data) : new Uint8Array(data);

    const hashBuffer = await crypto.subtle.digest(
        algorithm.toUpperCase(),
        (salt ? encoder.encode(salt + data) : dataBytes) as BufferSource
    );

    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

    return {
        algorithm,
        hash: hashHex,
        salt,
        iterations: salt ? 1 : undefined
    };
}

async function generateKeyPair(
    algorithm: 'ed25519' | 'secp256k1' = 'ed25519'
): Promise<KeyPair> {
    const algoParam = algorithm === 'ed25519'
        ? { name: 'Ed25519' }
        : { name: 'ECDSA', namedCurve: 'P-256' };

    const keyPair = await crypto.subtle.generateKey(
        algoParam,
        true,
        ['sign', 'verify']
    ) as CryptoKeyPair;

    const exportedPublic = await crypto.subtle.exportKey('raw', keyPair.publicKey);
    const exportedPrivate = await crypto.subtle.exportKey('pkcs8', keyPair.privateKey);

    return {
        publicKey: Buffer.from(exportedPublic).toString('base64'),
        privateKey: Buffer.from(exportedPrivate).toString('base64'),
        algorithm
    };
}
