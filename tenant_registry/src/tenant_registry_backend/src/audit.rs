use crate::{AUDIT_LOG, AuditEntry};
use hex;
use sha2::{Digest, Sha256};

#[ic_cdk::query]
pub fn get_audit_log(tenant: String, start: u64, limit: u64) -> Vec<AuditEntry> {
    let limit = limit.min(100);
    let t = tenant;
    AUDIT_LOG.with(|l| l.borrow().iter()
        .filter(|e| e.value().tenant == t || t.is_empty())
        .skip(start as usize).take(limit as usize)
        .map(|e| e.value().clone()).collect())
}

#[ic_cdk::query]
pub fn verify_audit_integrity() -> bool {
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
