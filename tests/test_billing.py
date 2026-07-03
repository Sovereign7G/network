import os
import pytest
from gateway.billing import BillingDB

def test_billing_db_init():
    db_path = "test_billing.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    db = BillingDB(db_path)
    assert os.path.exists(db_path)
    
    # Test customer and key creation
    cust_id, api_key = db.create_customer("Alice", "alice@example.com")
    assert cust_id is not None
    assert api_key is not None
    
    # Test key lookup
    assert db.get_customer_by_key(api_key) == cust_id
    assert db.get_customer_by_key("invalid_key") is None
    
    # Test balance checking and credit granting
    assert db.check_balance(cust_id) == 0.0
    db.grant_credits(cust_id, 10.0)
    assert db.check_balance(cust_id) == 10.0
    
    # Test usage deduction
    assert db.deduct_usage(cust_id, "req-1", 500, 2.5) is True
    assert db.check_balance(cust_id) == 7.5
    
    # Test deduction with insufficient balance
    assert db.deduct_usage(cust_id, "req-2", 5000, 10.0) is False
    assert db.check_balance(cust_id) == 7.5

    # Clean up
    db.close()
    os.remove(db_path)
