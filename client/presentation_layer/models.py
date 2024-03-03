import uuid
from pydantic import BaseModel
from typing import Optional, Dict, List


# Base Models : For communication with APIs

class Credentials(BaseModel):
    username: str
    password: str


class DecisionPlModel(BaseModel):  # JSON de l'API
    order_number: int
    customer_id: int
    order_id: int
    email: str
    status: str
    decision: str


class Product(BaseModel):
    unit_price: float
    quantity_ordered: int
    tva_rate: float


class Quote(BaseModel):
    order_number: int
    customer_id: int
    order_id: int
    products: Dict[str, Product]
    total_price: float
