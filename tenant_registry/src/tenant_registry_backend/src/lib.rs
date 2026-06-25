pub mod auth;
pub mod audit;
pub mod keys;
pub mod metrics;
pub mod models;
pub mod reserves;
pub mod tenants;

pub use auth::*;
pub use audit::*;
pub use keys::*;
pub use metrics::*;
pub use models::*;
pub use reserves::*;
pub use tenants::*;

use candid::{CandidType, Deserialize, Principal};
use ic_stable_structures::{
    memory_manager::{MemoryId, MemoryManager, VirtualMemory},
    storable::{Bound, Storable},
    DefaultMemoryImpl, StableBTreeMap, StableCell,
};
use serde::Serialize;
use std::borrow::Cow;
use std::cell::RefCell;

pub type Memory = VirtualMemory<DefaultMemoryImpl>;

// ── Tenant Types ───────────────────────────────────────────────────

#[derive(CandidType, Deserialize, Serialize, Clone, Debug)]
pub struct TenantMetadata {
    pub name: String, pub credits_canister: Option<Principal>,
    pub settlement_canister: Option<Principal>, pub tier: String,
    pub created_at: u64, pub updated_at: u64, pub active: bool, pub label: String,
}

#[derive(CandidType, Deserialize, Serialize, Clone, Debug)]
pub struct TenantSummary {
    pub name: String, pub tier: String,
    pub credits_id: Option<String>, pub settlement_id: Option<String>,
    pub active: bool, pub created_at: u64, pub label: String,
}

#[derive(CandidType, Deserialize)]
pub struct RegisterTenantArg {
    pub name: String, pub tier: String, pub label: Option<String>,
    pub credits_canister: Option<Principal>, pub settlement_canister: Option<Principal>,
}

#[derive(CandidType, Deserialize)]
pub struct UpdateTenantArg {
    pub tier: Option<String>, pub label: Option<String>,
    pub credits_canister: Option<Principal>, pub settlement_canister: Option<Principal>,
}

impl Storable for TenantMetadata {
    fn to_bytes(&self) -> Cow<'_, [u8]> { candid::encode_one(self).unwrap().into() }
    fn into_bytes(self) -> Vec<u8> { candid::encode_one(&self).unwrap() }
    fn from_bytes(bytes: Cow<[u8]>) -> Self { candid::decode_one(&bytes).unwrap() }
    const BOUND: Bound = Bound::Unbounded;
}

// ── RBAC Types ─────────────────────────────────────────────────────

#[derive(CandidType, Deserialize, Serialize, Clone, Debug, PartialEq, PartialOrd)]
pub enum Role { Admin, Operator, Auditor, Tenant }

#[derive(CandidType, Deserialize, Serialize, Clone, Debug)]
pub struct RoleAssignment {
    pub principal: Principal, pub role: Role,
    pub tenant: Option<String>, pub assigned_by: Principal, pub assigned_at: u64,
}

impl Storable for RoleAssignment {
    fn to_bytes(&self) -> Cow<'_, [u8]> { candid::encode_one(self).unwrap().into() }
    fn into_bytes(self) -> Vec<u8> { candid::encode_one(&self).unwrap() }
    fn from_bytes(bytes: Cow<[u8]>) -> Self { candid::decode_one(&bytes).unwrap() }
    const BOUND: Bound = Bound::Unbounded;
}

// ── OIDC Types ─────────────────────────────────────────────────────

#[derive(CandidType, Deserialize, Serialize, Clone, Debug)]
pub struct OIDCClaims {
    pub sub: String, pub email: String, pub name: String,
    pub roles: Vec<String>, pub issuer: String,
}

#[derive(CandidType, Deserialize, Serialize, Clone, Debug)]
pub struct Session {
    pub principal: Principal, pub claims: OIDCClaims,
    pub created_at: u64, pub expires_at: u64,
}

impl Storable for Session {
    fn to_bytes(&self) -> Cow<'_, [u8]> { candid::encode_one(self).unwrap().into() }
    fn into_bytes(self) -> Vec<u8> { candid::encode_one(&self).unwrap() }
    fn from_bytes(bytes: Cow<[u8]>) -> Self { candid::decode_one(&bytes).unwrap() }
    const BOUND: Bound = Bound::Unbounded;
}

// ── Audit Types ────────────────────────────────────────────────────

#[derive(CandidType, Deserialize, Serialize, Clone, Debug)]
pub struct AuditEntry {
    pub id: u64, pub timestamp: u64, pub tenant: String, pub actor: String,
    pub action: String, pub resource: String, pub details: String,
    pub previous_hash: String, pub hash: String,
}

impl Storable for AuditEntry {
    fn to_bytes(&self) -> Cow<'_, [u8]> { candid::encode_one(self).unwrap().into() }
    fn into_bytes(self) -> Vec<u8> { candid::encode_one(&self).unwrap() }
    fn from_bytes(bytes: Cow<[u8]>) -> Self { candid::decode_one(&bytes).unwrap() }
    const BOUND: Bound = Bound::Unbounded;
}

// ── API Key Types ──────────────────────────────────────────────────

#[derive(CandidType, Deserialize, Serialize, Clone, Debug)]
pub struct APIKey {
    pub key_id: String, pub tenant: String, pub rate_limit: u64,
    pub created_at: u64, pub expires_at: Option<u64>,
    pub last_used: Option<u64>, pub active: bool,
}

impl Storable for APIKey {
    fn to_bytes(&self) -> Cow<'_, [u8]> { candid::encode_one(self).unwrap().into() }
    fn into_bytes(self) -> Vec<u8> { candid::encode_one(&self).unwrap() }
    fn from_bytes(bytes: Cow<[u8]>) -> Self { candid::decode_one(&bytes).unwrap() }
    const BOUND: Bound = Bound::Unbounded;
}

// ── Model Types ────────────────────────────────────────────────────

#[derive(CandidType, Deserialize, Serialize, Clone, Debug)]
pub struct ModelSLA {
    pub p50_latency: u64, pub p99_latency: u64, pub uptime: f32,
}

#[derive(CandidType, Deserialize, Serialize, Clone, Debug)]
pub struct ModelRegistration {
    pub model_id: String, pub provider: String, pub model_name: String,
    pub input_price: u64, pub output_price: u64, pub max_tokens: u64,
    pub capabilities: Vec<String>, pub regions: Vec<String>,
    pub sla: ModelSLA, pub active: bool,
}

impl Storable for ModelRegistration {
    fn to_bytes(&self) -> Cow<'_, [u8]> { candid::encode_one(self).unwrap().into() }
    fn into_bytes(self) -> Vec<u8> { candid::encode_one(&self).unwrap() }
    fn from_bytes(bytes: Cow<[u8]>) -> Self { candid::decode_one(&bytes).unwrap() }
    const BOUND: Bound = Bound::Unbounded;
}

// ── Reserve Types ──────────────────────────────────────────────────

#[derive(CandidType, Serialize, Deserialize, Clone)]
pub struct ReserveState {
    pub usdc_balance: u64, pub credits_issued: u64,
    pub credits_redeemed: u64, pub last_attestation: u64,
    pub reserve_ratio: f64, pub compliant: bool,
}

impl Storable for ReserveState {
    fn to_bytes(&self) -> Cow<'_, [u8]> { candid::encode_one(self).unwrap().into() }
    fn into_bytes(self) -> Vec<u8> { candid::encode_one(&self).unwrap() }
    fn from_bytes(bytes: Cow<[u8]>) -> Self { candid::decode_one(&bytes).unwrap() }
    const BOUND: Bound = Bound::Unbounded;
}

// ── Metrics Types ──────────────────────────────────────────────────

#[derive(CandidType, Serialize, Deserialize, Clone)]
pub struct CanisterMetrics {
    pub tenant_count: u64, pub model_count: u64,
    pub audit_entry_count: u64, pub api_key_count: u64,
    pub inference_count: u64, pub error_count: u64,
}

// ── Memory IDs & Storage ───────────────────────────────────────────

const T_MEM: MemoryId = MemoryId::new(0);
const R_MEM: MemoryId = MemoryId::new(1);
const S_MEM: MemoryId = MemoryId::new(2);
const A_MEM: MemoryId = MemoryId::new(3);
const K_MEM: MemoryId = MemoryId::new(4);
const M_MEM: MemoryId = MemoryId::new(5);

thread_local! {
    pub static MM: RefCell<MemoryManager<DefaultMemoryImpl>> =
        RefCell::new(MemoryManager::init(DefaultMemoryImpl::default()));
    pub static TENANTS: RefCell<StableBTreeMap<String, TenantMetadata, Memory>> =
        RefCell::new(StableBTreeMap::init(MM.with(|m| m.borrow().get(T_MEM))));
    pub static RBAC: RefCell<StableBTreeMap<Principal, RoleAssignment, Memory>> =
        RefCell::new(StableBTreeMap::init(MM.with(|m| m.borrow().get(R_MEM))));
    pub static SESSIONS: RefCell<StableBTreeMap<Principal, Session, Memory>> =
        RefCell::new(StableBTreeMap::init(MM.with(|m| m.borrow().get(S_MEM))));
    pub static AUDIT_LOG: RefCell<StableBTreeMap<u64, AuditEntry, Memory>> =
        RefCell::new(StableBTreeMap::init(MM.with(|m| m.borrow().get(A_MEM))));
    pub static AUDIT_CTR: RefCell<u64> = RefCell::new(0);
    pub static API_KEYS: RefCell<StableBTreeMap<String, APIKey, Memory>> =
        RefCell::new(StableBTreeMap::init(MM.with(|m| m.borrow().get(K_MEM))));
    pub static MODELS: RefCell<StableBTreeMap<String, ModelRegistration, Memory>> =
        RefCell::new(StableBTreeMap::init(MM.with(|m| m.borrow().get(M_MEM))));
}

// ── Helpers ────────────────────────────────────────────────────────

pub fn require_role(min_role: Role) -> Result<(), String> {
    let caller = ic_cdk::api::msg_caller();
    if caller == ic_cdk::api::canister_self() { return Ok(()); }
    if RBAC.with(|s| s.borrow().len() == 0) { return Ok(()); }
    match RBAC.with(|s| s.borrow().get(&caller)) {
        None => Err("Unauthorized: no role assigned".to_string()),
        Some(a) if a.role > min_role => Err(format!(
            "Insufficient role: need {:?}, have {:?}", min_role, a.role)),
        _ => Ok(()),
    }
}

pub fn log_audit(tenant: &str, action: &str, resource: &str, details: &str) {
    use sha2::{Digest, Sha256};
    let id = AUDIT_CTR.with(|c| { *c.borrow_mut() += 1; *c.borrow() });
    let prev = AUDIT_LOG.with(|l| l.borrow().iter().last()
        .map(|e| e.into_pair().1.hash).unwrap_or_default());
    let now = ic_cdk::api::time();
    let actor = ic_cdk::api::msg_caller().to_text();
    let mut h = Sha256::new();
    h.update(id.to_le_bytes()); h.update(now.to_le_bytes());
    h.update(tenant.as_bytes()); h.update(actor.as_bytes());
    h.update(action.as_bytes()); h.update(resource.as_bytes());
    h.update(details.as_bytes()); h.update(prev.as_bytes());
    let hash = hex::encode(h.finalize());
    AUDIT_LOG.with(|l| l.borrow_mut().insert(id, AuditEntry {
        id, timestamp: now, tenant: tenant.into(), actor,
        action: action.into(), resource: resource.into(),
        details: details.into(), previous_hash: prev, hash,
    }));
}

pub fn gen_key() -> String {
    use sha2::{Digest, Sha256};
    let mut h = Sha256::new();
    h.update(ic_cdk::api::msg_caller().as_ref());
    h.update(ic_cdk::api::time().to_le_bytes());
    hex::encode(h.finalize())[..32].to_string()
}

// ── Reserve storage (needs separate thread_local) ──────────────────

thread_local! {
    pub static RESERVE: RefCell<StableCell<ReserveState, DefaultMemoryImpl>> =
        RefCell::new(StableCell::init(
            DefaultMemoryImpl::default(), ReserveState {
                usdc_balance: 0, credits_issued: 0, credits_redeemed: 0,
                last_attestation: 0, reserve_ratio: 0.0, compliant: false,
            }
        ));
}

ic_cdk::export_candid!();
