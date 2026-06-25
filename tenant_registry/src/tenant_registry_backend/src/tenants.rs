use crate::{require_role, log_audit, Role, TENANTS, TenantMetadata, TenantSummary, RegisterTenantArg, UpdateTenantArg};
use candid::Principal;

#[ic_cdk::update]
pub fn register_tenant(args: RegisterTenantArg) -> Result<TenantMetadata, String> {
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
pub fn get_tenant(name: String) -> Option<TenantMetadata> {
    TENANTS.with(|t| t.borrow().get(&name))
}

#[ic_cdk::query]
pub fn list_tenants() -> Vec<TenantSummary> {
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
pub fn update_tenant(name: String, args: UpdateTenantArg) -> Result<TenantMetadata, String> {
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
pub fn deactivate_tenant(name: String) -> Result<(), String> {
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
pub fn activate_tenant(name: String) -> Result<(), String> {
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
pub fn resolve_credits_canister(name: String) -> Option<Principal> {
    TENANTS.with(|t| t.borrow().get(&name).and_then(|m| m.credits_canister))
}

#[ic_cdk::query]
pub fn resolve_settlement_canister(name: String) -> Option<Principal> {
    TENANTS.with(|t| t.borrow().get(&name).and_then(|m| m.settlement_canister))
}

#[ic_cdk::query]
pub fn tenant_count() -> u64 { TENANTS.with(|t| t.borrow().len() as u64) }
