use crate::{require_role, log_audit, Role, RESERVE, ReserveState};

#[ic_cdk::update]
pub fn deposit_usdc(amount: u64) -> Result<(), String> {
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
pub fn get_reserve_state() -> ReserveState {
    RESERVE.with(|r| r.borrow().get().clone())
}

#[ic_cdk::update]
pub fn attest_reserves() -> String {
    let s = RESERVE.with(|r| r.borrow().get().clone());
    let att = format!(
        "{{\"usdc\":{},\"issued\":{},\"redeemed\":{},\"ratio\":{},\"compliant\":{},\"ts\":{}}}",
        s.usdc_balance, s.credits_issued, s.credits_redeemed,
        s.reserve_ratio, s.compliant, ic_cdk::api::time());
    log_audit("system", "attest_reserves", "reserve", &att);
    att
}
