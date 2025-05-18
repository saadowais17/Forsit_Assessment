from pydantic import BaseModel
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class SaleCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class InventoryUpdate(BaseModel):
    current_stock: int

class SaleResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    sale_date: datetime

    class Config:
        orm_mode = True

class RevenueResponse(BaseModel):
    period: str
    revenue: float