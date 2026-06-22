pub mod cosmic {
    pub const PI: f64 = 3.14159265358979323846264338327950288;
    pub const C: f64 = 299792458.0; // m/s
    pub const PLANCK: f64 = 6.62607015e-34;
}

pub mod protocol {
    pub const VERSION: &str = "29.1";
    pub const AGE_PRECISION: u8 = 18;
    pub const QUADRATIC_THRESHOLD: u64 = 100; // sqrt weight units
}

pub mod error_codes {
    pub const ECONOMIC_HALT: u32 = 0x5C01;
    pub const TENANT_ISOLATION_FAILURE: u32 = 0x5C02;
    pub const SUBSTRATE_MISSING: u32 = 0x5C03;
    pub const EFFECT_OVERFLOW: u32 = 0x5C04;
    pub const GAS_EXHAUSTION: u32 = 0x5C05;
}
