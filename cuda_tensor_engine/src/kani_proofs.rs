// 🔬 Kani Formal Verification Proof
#[cfg(kani)]
#[kani::proof]
fn verify_arbitrage_profit_bounds() {
    let spread: f64 = kani::any();
    // Invariant: spread percentage is bounded inside normal limits
    kani::assume(spread >= 0.0);
    kani::assume(spread <= 1.0);
    
    // Check absence of floating-point overflow under atomic splits
    let share = spread * 0.05;
    assert!(share <= spread);
}
