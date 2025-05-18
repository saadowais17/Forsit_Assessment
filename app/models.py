from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base 

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(500))
    price = Column(DECIMAL(10, 2))
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="products")
    sales = relationship("Sale", back_populates="product")
    inventory = relationship("Inventory", back_populates="product", uselist=False)

class Sale(Base):
    __tablename__ = "sale"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)
    unit_price = Column(DECIMAL(10, 2))
    total_price = Column(DECIMAL(10, 2))
    sale_date = Column(TIMESTAMP, default=datetime.utcnow)
    product = relationship("Product", back_populates="sales")

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    current_stock = Column(Integer)
    low_stock_threshold = Column(Integer, default=10)
    last_updated = Column(TIMESTAMP, default=datetime.utcnow)
    product = relationship("Product", back_populates="inventory")

class InventoryHistory(Base):
    __tablename__ = "inventory_history"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    old_stock = Column(Integer)
    new_stock = Column(Integer)
    change_date = Column(TIMESTAMP, default=datetime.utcnow)