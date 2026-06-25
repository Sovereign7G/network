use crate::{TENANTS, MODELS, AUDIT_LOG, API_KEYS, CanisterMetrics};

#[ic_cdk::query]
pub fn get_metrics() -> CanisterMetrics {
    CanisterMetrics {
        tenant_count: TENANTS.with(|t| t.borrow().len() as u64),
        model_count: MODELS.with(|m| m.borrow().len() as u64),
        audit_entry_count: AUDIT_LOG.with(|l| l.borrow().len() as u64),
        api_key_count: API_KEYS.with(|k| k.borrow().len() as u64),
        inference_count: 0,
        error_count: 0,
    }
}
