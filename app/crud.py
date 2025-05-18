from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from .models import Product, Sale, Inventory, InventoryHistory
from .database import get_db

# Product Operations
def create_product(db: Session, product_data):
    db_product = Product(**product_data.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Sales Operations
def create_sale(db: Session, sale_data):
    total_price = sale_data.quantity * sale_data.unit_price
    db_sale = Sale(**sale_data.dict(), total_price=total_price)
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sales(db: Session, start_date: str = None, end_date: str = None, product_id: int = None):
    query = db.query(Sale)
    if start_date and end_date:
        query = query.filter(Sale.sale_date.between(start_date, end_date))
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    return query.all()

def get_sales_by_category(db: Session, category_id: int):
    return db.query(Sale).join(Product).filter(Product.category_id == category_id).all()

def get_revenue_by_period(db: Session, period: str):
    today = datetime.now()
    if period == "daily":
        return db.query(
            func.date(Sale.sale_date).label("period"),
            func.sum(Sale.total_price).label("revenue")
        ).group_by(func.date(Sale.sale_date)).all()
    elif period == "weekly":
        return db.query(
            func.yearweek(Sale.sale_date).label("period"),
            func.sum(Sale.total_price).label("revenue")
        ).group_by(func.yearweek(Sale.sale_date)).all()
    elif period == "monthly":
        return db.query(
            func.extract('year', Sale.sale_date).label("year"),
            func.extract('month', Sale.sale_date).label("month"),
            func.sum(Sale.total_price).label("revenue")
        ).group_by("year", "month").all()
    elif period == "annual":
        return db.query(
            func.extract('year', Sale.sale_date).label("period"),
            func.sum(Sale.total_price).label("revenue")
        ).group_by("period").all()

# Inventory Operations
def update_inventory(db: Session, product_id: int, new_stock: int):
    db_inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if db_inventory:
        db.add(InventoryHistory(
            product_id=product_id,
            old_stock=db_inventory.current_stock,
            new_stock=new_stock
        ))
        db_inventory.current_stock = new_stock
        db.commit()
        return db_inventory
    return None

def get_low_stock_products(db: Session, threshold: int = 10):
    return db.query(Inventory).filter(Inventory.current_stock < threshold).all()