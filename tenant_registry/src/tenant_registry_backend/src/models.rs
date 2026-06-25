use crate::{require_role, log_audit, Role, MODELS, ModelRegistration};

#[ic_cdk::update]
pub fn register_model(m: ModelRegistration) -> Result<(), String> {
    require_role(Role::Admin)?;
    let id = m.model_id.clone();
    MODELS.with(|ms| ms.borrow_mut().insert(id.clone(), m));
    log_audit("system", "register_model", &id, "");
    Ok(())
}

#[ic_cdk::query]
pub fn list_models(provider: Option<String>, capability: Option<String>) -> Vec<ModelRegistration> {
    MODELS.with(|ms| {
        let ms = ms.borrow();
        let mut out: Vec<ModelRegistration> = ms.iter().map(|e| e.into_pair().1).collect();
        if let Some(ref p) = provider { out.retain(|m| &m.provider == p); }
        if let Some(ref c) = capability { out.retain(|m| m.capabilities.contains(c)); }
        out
    })
}

#[ic_cdk::update]
pub fn update_model_pricing(model_id: String, input_price: u64, output_price: u64) -> Result<(), String> {
    require_role(Role::Admin)?;
    MODELS.with(|ms| {
        let mut ms = ms.borrow_mut();
        match ms.get(&model_id) {
            Some(mut m) => {
                m.input_price = input_price; m.output_price = output_price;
                ms.insert(model_id.clone(), m);
                log_audit("system", "update_model_pricing", &model_id, "");
                Ok(())
            }
            None => Err(format!("Model '{}' not found", model_id)),
        }
    })
}
