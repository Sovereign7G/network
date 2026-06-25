use candid::{CandidType, Deserialize, Principal};
use ic_stable_structures::{
    memory_manager::{MemoryId, MemoryManager, VirtualMemory},
    storable::{Bound, Storable},
    DefaultMemoryImpl, StableBTreeMap, StableCell,
};
use serde::Serialize;
use std::borrow::Cow;
use std::cell::RefCell;

type Memory = VirtualMemory<DefaultMemoryImpl>;

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

const T_MEM: MemoryId = MemoryId::new(0);
const R_MEM: MemoryId = MemoryId::new(1);
const S_MEM: MemoryId = MemoryId::new(2);
const A_MEM: MemoryId = MemoryId::new(3);
const K_MEM: MemoryId = MemoryId::new(4);
const M_MEM: MemoryId = MemoryId::new(5);

thread_local! {
    static MM: RefCell<MemoryManager<DefaultMemoryImpl>> =
        RefCell::new(MemoryManager::init(DefaultMemoryImpl::default()));
    static TENANTS: RefCell<StableBTreeMap<String, TenantMetadata, Memory>> =
        RefCell::new(StableBTreeMap::init(MM.with(|m| m.borrow().get(T_MEM))));
    static RBAC: RefCell<StableBTreeMap<Principal, RoleAssignment, Memory>> =
        RefCell::new(StableBTreeMap::init(MM.with(|m| m.borrow().get(R_MEM))));
    static SESSIONS: RefCell<StableBTreeMap<Principal, Session, Memory>> =
        RefCell::new(StableBTreeMap::init(MM.with(|m| m.borrow().get(S_MEM))));
    static AUDIT_LOG: RefCell<StableBTreeMap<u64, AuditEntry, Memory>> =
        RefCell::new(StableBTreeMap::init(MM.with(|m| m.borrow().get(A_MEM))));
    static AUDIT_CTR: RefCell<u64> = RefCell::new(0);
    static API_KEYS: RefCell<StableBTreeMap<String, APIKey, Memory>> =
        RefCell::new(StableBTreeMap::init(MM.with(|m| m.borrow().get(K_MEM))));
    static MODELS: RefCell<StableBTreeMap<String, ModelRegistration, Memory>> =
        RefCell::new(StableBTreeMap::init(MM.with(|m| m.borrow().get(M_MEM))));
}

fn require_role(min_role: Role) -> Result<(), String> {
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

fn log_audit(tenant: &str, action: &str, resource: &str, details: &str) {
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

fn gen_key() -> String {
    use sha2::{Digest, Sha256};
    let mut h = Sha256::new();
    h.update(ic_cdk::api::msg_caller().as_ref());
    h.update(ic_cdk::api::time().to_le_bytes());
    hex::encode(h.finalize())[..32].to_string()
}

// ── RBAC API ───────────────────────────────────────────────────────

#[ic_cdk::update]
fn assign_role(p: Principal, role: Role, t: Option<String>) -> Result<(), String> {
    require_role(Role::Admin)?;
    let role_name = format!("{:?}", role);
    RBAC.with(|s| s.borrow_mut().insert(p, RoleAssignment {
        principal: p, role, tenant: t,
        assigned_by: ic_cdk::api::msg_caller(), assigned_at: ic_cdk::api::time(),
    }));
    log_audit("system", "assign_role", &p.to_text(), &role_name);
    Ok(())
}

#[ic_cdk::update]
fn remove_role(p: Principal) -> Result<(), String> {
    require_role(Role::Admin)?;
    RBAC.with(|s| s.borrow_mut().remove(&p));
    log_audit("system", "remove_role", &p.to_text(), "");
    Ok(())
}

#[ic_cdk::query]
fn get_role(p: Principal) -> Option<RoleAssignment> { RBAC.with(|s| s.borrow().get(&p)) }

#[ic_cdk::query]
fn list_roles() -> Vec<RoleAssignment> {
    RBAC.with(|s| s.borrow().iter().map(|e| e.into_pair().1).collect())
}

// ── OIDC API ───────────────────────────────────────────────────────

#[ic_cdk::update]
fn oidc_login(claims: OIDCClaims, ttl_secs: Option<u64>) -> Result<Principal, String> {
    require_role(Role::Operator)?;
    let caller = ic_cdk::api::msg_caller();
    let now = ic_cdk::api::time() / 1_000_000_000;
    let ttl = ttl_secs.unwrap_or(3600).min(86400);
    SESSIONS.with(|s| s.borrow_mut().insert(caller, Session {
        principal: caller, claims, created_at: now, expires_at: now + ttl,
    }));
    log_audit("system", "oidc_login", &caller.to_text(), "");
    Ok(caller)
}

#[ic_cdk::query]
fn get_session(p: Principal) -> Option<Session> { SESSIONS.with(|s| s.borrow().get(&p)) }

#[ic_cdk::update]
fn oidc_logout() -> Result<(), String> {
    SESSIONS.with(|s| s.borrow_mut().remove(&ic_cdk::api::msg_caller()));
    Ok(())
}

// ── Audit API ──────────────────────────────────────────────────────

#[ic_cdk::query]
fn get_audit_log(tenant: String, start: u64, limit: u64) -> Vec<AuditEntry> {
    let limit = limit.min(100);
    let t = tenant;
    AUDIT_LOG.with(|l| l.borrow().iter()
        .filter(|e| e.value().tenant == t || t.is_empty())
        .skip(start as usize).take(limit as usize)
        .map(|e| e.value().clone()).collect())
}

#[ic_cdk::query]
fn verify_audit_integrity() -> bool {
    use sha2::{Digest, Sha256};
    AUDIT_LOG.with(|l| {
        let mut prev = String::new();
        for e in l.borrow().iter() {
            let entry = e.into_pair().1;
            if entry.previous_hash != prev { return false; }
            let mut h = Sha256::new();
            h.update(entry.id.to_le_bytes()); h.update(entry.timestamp.to_le_bytes());
            h.update(entry.tenant.as_bytes()); h.update(entry.actor.as_bytes());
            h.update(entry.action.as_bytes()); h.update(entry.resource.as_bytes());
            h.update(entry.details.as_bytes()); h.update(prev.as_bytes());
            if entry.hash != hex::encode(h.finalize()) { return false; }
            prev = entry.hash;
        }
        true
    })
}

// ── API Keys ──────────────────────────────────────────────────────

#[ic_cdk::update]
fn create_api_key(tenant: String, rate_limit: u64) -> Result<String, String> {
    require_role(Role::Admin)?;
    let key_id = gen_key();
    let k = key_id.clone();
    API_KEYS.with(|m| m.borrow_mut().insert(k, APIKey {
        key_id: key_id.clone(), tenant,
        rate_limit: rate_limit.max(1).min(10000),
        created_at: ic_cdk::api::time(), expires_at: None,
        last_used: None, active: true,
    }));
    log_audit("system", "create_api_key", &key_id, "{}");
    Ok(key_id)
}

#[ic_cdk::update]
fn revoke_api_key(key_id: String) -> Result<(), String> {
    require_role(Role::Admin)?;
    let kid = key_id.clone();
    API_KEYS.with(|m| {
        let mut map = m.borrow_mut();
        match map.get(&kid) {
            Some(mut key) => { key.active = false; map.insert(kid.clone(), key); Ok(()) }
            None => Err("API key not found".to_string()),
        }
    })?;
    log_audit("system", "revoke_api_key", &key_id, "{}");
    Ok(())
}

#[ic_cdk::query]
fn list_api_keys(tenant: String) -> Vec<APIKey> {
    let t = tenant;
    API_KEYS.with(|m| m.borrow().iter()
        .filter(|e| e.value().tenant == t || t.is_empty())
        .map(|e| e.value().clone()).collect())
}

// ── Model Marketplace API ──────────────────────────────────────────

#[ic_cdk::update]
fn register_model(m: ModelRegistration) -> Result<(), String> {
    require_role(Role::Admin)?;
    let id = m.model_id.clone();
    MODELS.with(|ms| ms.borrow_mut().insert(id.clone(), m));
    log_audit("system", "register_model", &id, "");
    Ok(())
}

#[ic_cdk::query]
fn list_models(provider: Option<String>, capability: Option<String>) -> Vec<ModelRegistration> {
    MODELS.with(|ms| {
        let ms = ms.borrow();
        let mut out: Vec<ModelRegistration> = ms.iter().map(|e| e.into_pair().1).collect();
        if let Some(ref p) = provider {
            out.retain(|m| &m.provider == p);
        }
        if let Some(ref c) = capability {
            out.retain(|m| m.capabilities.contains(c));
        }
        out
    })
}

#[ic_cdk::update]
fn update_model_pricing(model_id: String, input_price: u64, output_price: u64) -> Result<(), String> {
    require_role(Role::Admin)?;
    MODELS.with(|ms| {
        let mut ms = ms.borrow_mut();
        match ms.get(&model_id) {
            Some(mut m) => {
                m.input_price = input_price;
                m.output_price = output_price;
                ms.insert(model_id.clone(), m);
                log_audit("system", "update_model_pricing", &model_id, "");
                Ok(())
            }
            None => Err(format!("Model '{}' not found", model_id)),
        }
    })
}

// ── Tenant API ─────────────────────────────────────────────────────

#[ic_cdk::update]
fn register_tenant(args: RegisterTenantArg) -> Result<TenantMetadata, String> {
    require_role(Role::Admin)?;
    let name = args.name.trim().to_string();
    if name.is_empty() { return Err("Tenant name cannot be empty".to_string()); }
    let tier = args.tier.to_lowercase();
    if !["starter", "growth", "enterprise"].contains(&tier.as_str()) {
        return Err(format!("Invalid tier '{}'", tier));
    }
    if TENANTS.with(|t| t.borrow().contains_key(&name)) {
        return Err(format!("Tenant '{}' already exists", name));
    }
    let now = ic_cdk::api::time();
    let meta = TenantMetadata {
        label: args.label.unwrap_or_else(|| name.clone()), name: name.clone(),
        credits_canister: args.credits_canister,
        settlement_canister: args.settlement_canister, tier: tier.clone(),
        created_at: now, updated_at: now, active: true,
    };
    TENANTS.with(|t| t.borrow_mut().insert(name.clone(), meta.clone()));
    log_audit(&name, "register_tenant", &name, &format!("{{\"tier\":\"{}\"}}", tier));
    Ok(meta)
}

#[ic_cdk::query]
fn get_tenant(name: String) -> Option<TenantMetadata> {
    TENANTS.with(|t| t.borrow().get(&name))
}

#[ic_cdk::query]
fn list_tenants() -> Vec<TenantSummary> {
    TENANTS.with(|t| t.borrow().iter().map(|e| {
        let (_, v) = e.into_pair();
        TenantSummary {
            name: v.name, tier: v.tier,
            credits_id: v.credits_canister.map(|p| p.to_text()),
            settlement_id: v.settlement_canister.map(|p| p.to_text()),
            active: v.active, created_at: v.created_at, label: v.label,
        }
    }).collect())
}

#[ic_cdk::update]
fn update_tenant(name: String, args: UpdateTenantArg) -> Result<TenantMetadata, String> {
    require_role(Role::Operator)?;
    TENANTS.with(|t| {
        let mut map = t.borrow_mut();
        match map.get(&name) {
            Some(mut meta) => {
                if let Some(ref tier) = args.tier {
                    let t = tier.to_lowercase();
                    if !["starter","growth","enterprise"].contains(&t.as_str()) {
                        return Err(format!("Invalid tier '{}'", tier));
                    }
                    meta.tier = t;
                }
                if let Some(l) = args.label { meta.label = l; }
                if let Some(c) = args.credits_canister { meta.credits_canister = Some(c); }
                if let Some(c) = args.settlement_canister { meta.settlement_canister = Some(c); }
                meta.updated_at = ic_cdk::api::time();
                map.insert(name.clone(), meta.clone());
                log_audit(&name, "update_tenant", &name, "");
                Ok(meta)
            }
            None => Err(format!("Tenant '{}' not found", name)),
        }
    })
}

#[ic_cdk::update]
fn deactivate_tenant(name: String) -> Result<(), String> {
    require_role(Role::Operator)?;
    TENANTS.with(|t| {
        let mut map = t.borrow_mut();
        match map.get(&name) {
            Some(mut meta) => { meta.active = false; meta.updated_at = ic_cdk::api::time();
                map.insert(name.clone(), meta);
                log_audit(&name, "deactivate_tenant", &name, ""); Ok(()) }
            None => Err(format!("Tenant '{}' not found", name)),
        }
    })
}

#[ic_cdk::update]
fn activate_tenant(name: String) -> Result<(), String> {
    require_role(Role::Operator)?;
    TENANTS.with(|t| {
        let mut map = t.borrow_mut();
        match map.get(&name) {
            Some(mut meta) => { meta.active = true; meta.updated_at = ic_cdk::api::time();
                map.insert(name.clone(), meta);
                log_audit(&name, "activate_tenant", &name, ""); Ok(()) }
            None => Err(format!("Tenant '{}' not found", name)),
        }
    })
}

#[ic_cdk::query]
fn resolve_credits_canister(name: String) -> Option<Principal> {
    TENANTS.with(|t| t.borrow().get(&name).and_then(|m| m.credits_canister))
}

#[ic_cdk::query]
fn resolve_settlement_canister(name: String) -> Option<Principal> {
    TENANTS.with(|t| t.borrow().get(&name).and_then(|m| m.settlement_canister))
}

#[ic_cdk::query]
fn tenant_count() -> u64 { TENANTS.with(|t| t.borrow().len() as u64) }

// ── GENIUS Act Reserve Compliance ─────────────────────────────────

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

thread_local! {
    static RESERVE: RefCell<StableCell<ReserveState, DefaultMemoryImpl>> =
        RefCell::new(StableCell::init(
            DefaultMemoryImpl::default(), ReserveState {
                usdc_balance: 0, credits_issued: 0, credits_redeemed: 0,
                last_attestation: 0, reserve_ratio: 0.0, compliant: false,
            }
        ));
}

#[ic_cdk::update]
fn deposit_usdc(amount: u64) -> Result<(), String> {
    require_role(Role::Admin)?;
    RESERVE.with(|r| {
        let mut cell = r.borrow_mut();
        let mut s = cell.get().clone();
        s.usdc_balance += amount;
        s.last_attestation = ic_cdk::api::time();
        let net = s.credits_issued.checked_sub(s.credits_redeemed).unwrap_or(1);
        s.reserve_ratio = s.usdc_balance as f64 / net as f64;
        s.compliant = s.reserve_ratio >= 1.0;
        cell.set(s);
    });
    log_audit("system", "deposit_usdc", "reserve", &format!("{{\"amount\":{}}}", amount));
    Ok(())
}

#[ic_cdk::query]
fn get_reserve_state() -> ReserveState {
    RESERVE.with(|r| r.borrow().get().clone())
}

#[ic_cdk::update]
fn attest_reserves() -> String {
    let s = RESERVE.with(|r| r.borrow().get().clone());
    let att = format!(
        "{{\"usdc\":{},\"issued\":{},\"redeemed\":{},\"ratio\":{},\"compliant\":{},\"ts\":{}}}",
        s.usdc_balance, s.credits_issued, s.credits_redeemed,
        s.reserve_ratio, s.compliant, ic_cdk::api::time());
    log_audit("system", "attest_reserves", "reserve", &att);
    att
}

// ── Metrics ────────────────────────────────────────────────────────

#[derive(CandidType, Serialize, Deserialize, Clone)]
pub struct CanisterMetrics {
    pub tenant_count: u64, pub model_count: u64,
    pub audit_entry_count: u64, pub api_key_count: u64,
    pub inference_count: u64, pub error_count: u64,
}

#[ic_cdk::query]
fn get_metrics() -> CanisterMetrics {
    CanisterMetrics {
        tenant_count: TENANTS.with(|t| t.borrow().len() as u64),
        model_count: MODELS.with(|m| m.borrow().len() as u64),
        audit_entry_count: AUDIT_LOG.with(|l| l.borrow().len() as u64),
        api_key_count: API_KEYS.with(|k| k.borrow().len() as u64),
        inference_count: 0,
        error_count: 0,
    }
}

ic_cdk::export_candid!();
