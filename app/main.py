import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, get_db  # Relative imports
from .models import Base
from .schemas import ProductCreate, SaleCreate, InventoryUpdate, SaleResponse
from .crud import create_product, create_sale, get_sales, update_inventory, get_sales_by_category, get_revenue_by_period, get_low_stock_products

app = FastAPI()
Base.metadata.create_all(bind=engine)  

from typing import List

# Product Endpoints
@app.post("/products")
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

# Sales Endpoints
@app.post("/sales")
def add_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    return create_sale(db, sale)

@app.get("/sales", response_model=List[SaleResponse])
def list_sales(
    start_date: str = None,
    end_date: str = None,
    product_id: int = None,
    db: Session = Depends(get_db)
):
    return get_sales(db, start_date, end_date, product_id)

@app.get("/sales/category/{category_id}", response_model=List[SaleResponse])
def sales_by_category(category_id: int, db: Session = Depends(get_db)):
    return get_sales_by_category(db, category_id)

@app.get("/revenue/{period}", response_model=List[dict])
def revenue_by_period(period: str, db: Session = Depends(get_db)):
    if period not in ["daily", "weekly", "monthly", "annual"]:
        raise HTTPException(status_code=400, detail="Invalid period. Use: daily, weekly, monthly, annual")
    return get_revenue_by_period(db, period)

# Inventory Endpoints
@app.patch("/inventory/{product_id}")
def update_stock(product_id: int, stock: InventoryUpdate, db: Session = Depends(get_db)):
    updated = update_inventory(db, product_id, stock.current_stock)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@app.get("/inventory/low-stock")
def list_low_stock(db: Session = Depends(get_db), threshold: int = 10):
    return get_low_stock_products(db, threshold)