use crate::{require_role, log_audit, gen_key, Role, API_KEYS, APIKey};

#[ic_cdk::update]
pub fn create_api_key(tenant: String, rate_limit: u64) -> Result<String, String> {
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
pub fn revoke_api_key(key_id: String) -> Result<(), String> {
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
pub fn list_api_keys(tenant: String) -> Vec<APIKey> {
    let t = tenant;
    API_KEYS.with(|m| m.borrow().iter()
        .filter(|e| e.value().tenant == t || t.is_empty())
        .map(|e| e.value().clone()).collect())
}
