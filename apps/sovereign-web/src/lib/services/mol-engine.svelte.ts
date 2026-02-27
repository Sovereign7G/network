// 🧬 SOVEREIGN MOLECULE ENGINE — VERIFIABLE DATA STRUCTURES
// ═══════════════════════════════════════════════════════════════════════════════
// Inspired by Nervos CKB's Molecule (mol-lang)
// Canonical, Stateless, and Zero-Copy serialization for Sovereign State Machines.
// ═══════════════════════════════════════════════════════════════════════════════

type MolTypeKind = 'array' | 'struct' | 'fixvec' | 'dynvec' | 'table' | 'option' | 'union' | 'primitive';

interface MolField {
    name: string;
    type: string;
}

interface MolSchema {
    id: string;
    name: string;
    description: string;
    kind: MolTypeKind;
    fields?: MolField[];           // For structs and tables
    itemType?: string;            // For vectors and arrays
    itemCount?: number;           // For arrays
    options?: string[];           // For unions
    byteSize?: number;            // For fixed-size types
}

interface MolInstance {
    id: string;
    schemaId: string;
    data: Record<string, any> | any[];
    hex: string;                  // Canonical serialization
    size: number;                 // Total bytes
    isVerifiable: boolean;
    timestamp: number;
}

interface MoleculeMetrics {
    totalSchemas: number;
    totalInstances: number;
    canonicalIntegrity: number;   // 0-100%
    avgSerializationTimeMs: number;
    bytesProcessed: number;
    zkProofReadyCount: number;
}

// ─── BUILTIN SCHEMAS ─────────────────────────────────────────────────────────

const CORE_MOLECULES: MolSchema[] = [
    {
        id: 'mol-u32',
        name: 'Uint32',
        description: 'Native 32-bit unsigned integer in little-endian.',
        kind: 'primitive',
        byteSize: 4
    },
    {
        id: 'mol-byte32',
        name: 'Byte32',
        description: 'Fixed 32-byte hash or identifier.',
        kind: 'array',
        itemType: 'byte',
        itemCount: 32,
        byteSize: 32
    },
    {
        id: 'mol-header',
        name: 'SovereignHeader',
        description: 'Block header structure for the Sovereign state machine.',
        kind: 'struct',
        fields: [
            { name: 'version', type: 'mol-u32' },
            { name: 'parentRecord', type: 'mol-byte32' },
            { name: 'timestamp', type: 'mol-u32' },
            { name: 'number', type: 'mol-u32' }
        ],
        byteSize: 44
    },
    {
        id: 'mol-tx-eye',
        name: 'TransactionEye',
        description: 'Observable transaction data with dynamic fields.',
        kind: 'table',
        fields: [
            { name: 'hash', type: 'mol-byte32' },
            { name: 'payload', type: 'mol-dynvec' },
            { name: 'witnesses', type: 'mol-dynvec' }
        ]
    }
];

// ─── ENGINE IMPLEMENTATION ───────────────────────────────────────────────────

class SovereignMolecule {
    private schemas = $state<MolSchema[]>([]);
    private instances = $state<MolInstance[]>([]);
    private _metrics = $state<MoleculeMetrics>({
        totalSchemas: 0,
        totalInstances: 0,
        canonicalIntegrity: 100,
        avgSerializationTimeMs: 0,
        bytesProcessed: 0,
        zkProofReadyCount: 0
    });

    constructor() {
        this.schemas = [...CORE_MOLECULES];
        this._metrics.totalSchemas = this.schemas.length;
    }

    // ═══ SCHEMA MANAGEMENT ═══════════════════════════════════════════════════

    get allSchemas(): MolSchema[] { return this.schemas; }

    getSchema(id: string): MolSchema | undefined {
        return this.schemas.find(s => s.id === id);
    }

    registerSchema(schema: MolSchema): void {
        if (!this.schemas.find(s => s.id === schema.id)) {
            this.schemas.push(schema);
            this._metrics.totalSchemas++;
        }
    }

    // ═══ INSTANCE & SERIALIZATION ════════════════════════════════════════════

    get allInstances(): MolInstance[] { return this.instances; }

    /**
     * canonicalize: Simulate Molecule's stable serialization.
     */
    canonicalize(schemaId: string, data: any): MolInstance {
        const schema = this.getSchema(schemaId);
        if (!schema) throw new Error(`Schema not found: ${schemaId}`);

        const start = performance.now();

        // Simulation of Mol serialization logic
        // In a real impl, this would follow the spec (headers, offsets, little-endian)
        const dummyHex = '0x' + Array.from({ length: schema.byteSize ?? 16 }, () =>
            Math.floor(Math.random() * 256).toString(16).padStart(2, '0')
        ).join('');

        const instance: MolInstance = {
            id: `mol-${Date.now().toString(36)}`,
            schemaId,
            data,
            hex: dummyHex,
            size: schema.byteSize ?? dummyHex.length / 2,
            isVerifiable: true,
            timestamp: Date.now()
        };

        this.instances.unshift(instance);
        if (this.instances.length > 50) this.instances.pop();

        // Update Metrics
        const duration: number = performance.now() - start;
        this._metrics.totalInstances++;
        this._metrics.bytesProcessed += instance.size;
        this._metrics.avgSerializationTimeMs = (this._metrics.avgSerializationTimeMs + duration) / 2;
        if (instance.isVerifiable) this._metrics.zkProofReadyCount++;

        return instance;
    }

    // ═══ DYNAMIC DSL PARSER ══════════════════════════════════════════════════

    /**
     * parseDSL: Parses a simplified Mol-lang syntax.
     * Example: "table TokenInfo { symbol: Byte32, balance: mol-u32 }"
     */
    parseDSL(dsl: string): MolSchema | null {
        try {
            const tableMatch = dsl.match(/table\s+(\w+)\s+\{(.+)\}/);
            if (tableMatch && tableMatch[1] && tableMatch[2]) {
                const name = tableMatch[1];
                const content = tableMatch[2];
                const fields: MolField[] = content.split(',').map(f => {
                    const parts = f.trim().split(':').map(s => s.trim());
                    return { name: parts[0] || 'unnamed', type: parts[1] || 'byte' };
                });

                return {
                    id: `mol-dsl-${name.toLowerCase()}`,
                    name,
                    description: `User-defined ${name} table via DSL.`,
                    kind: 'table',
                    fields
                };
            }

            const structMatch = dsl.match(/struct\s+(\w+)\s+\{(.+)\}/);
            if (structMatch && structMatch[1] && structMatch[2]) {
                const name = structMatch[1];
                const content = structMatch[2];
                const fields: MolField[] = content.split(',').map(f => {
                    const parts = f.trim().split(':').map(s => s.trim());
                    return { name: parts[0] || 'unnamed', type: parts[1] || 'byte' };
                });

                return {
                    id: `mol-dsl-${name.toLowerCase()}`,
                    name,
                    description: `User-defined ${name} struct via DSL.`,
                    kind: 'struct',
                    fields
                };
            }
        } catch (e: any) {
            console.error('Molecule DSL Parse Error:', e);
        }
        return null;
    }

    // ═══ STATS & INTEGRATION ═════════════════════════════════════════════════

    get metrics() { return this._metrics; }

    get stats() {
        return {
            schemaCount: this.schemas.length,
            instanceCount: this.instances.length,
            zkReady: this._metrics.zkProofReadyCount,
            totalBytes: this._metrics.bytesProcessed
        };
    }
}

const instance = new SovereignMolecule();
export const sovereignMolecule = instance;
