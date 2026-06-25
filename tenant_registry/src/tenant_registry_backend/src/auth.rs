use crate::{require_role, log_audit, RBAC, Role, RoleAssignment, Session, OIDCClaims, SESSIONS};
use candid::Principal;

#[ic_cdk::update]
pub fn assign_role(p: Principal, role: Role, t: Option<String>) -> Result<(), String> {
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
pub fn remove_role(p: Principal) -> Result<(), String> {
    require_role(Role::Admin)?;
    RBAC.with(|s| s.borrow_mut().remove(&p));
    log_audit("system", "remove_role", &p.to_text(), "");
    Ok(())
}

#[ic_cdk::query]
pub fn get_role(p: Principal) -> Option<RoleAssignment> { RBAC.with(|s| s.borrow().get(&p)) }

#[ic_cdk::query]
pub fn list_roles() -> Vec<RoleAssignment> {
    RBAC.with(|s| s.borrow().iter().map(|e| e.into_pair().1).collect())
}

#[ic_cdk::update]
pub fn oidc_login(claims: OIDCClaims, ttl_secs: Option<u64>) -> Result<Principal, String> {
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
pub fn get_session(p: Principal) -> Option<Session> { SESSIONS.with(|s| s.borrow().get(&p)) }

#[ic_cdk::update]
pub fn oidc_logout() -> Result<(), String> {
    SESSIONS.with(|s| s.borrow_mut().remove(&ic_cdk::api::msg_caller()));
    Ok(())
}
