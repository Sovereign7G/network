from pydantic import BaseModel, EmailStr
from typing import Optional, List

class CustomerCreate(BaseModel):
    name: str
    email: str

class CreditGrant(BaseModel):
    amount: float
