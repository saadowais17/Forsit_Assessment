from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal 
from app.models import Product, Sale, Inventory, Category
import random
from datetime import datetime, timedelta

fake = Faker()

def populate_data():
    db = SessionLocal()
    try:
        # Add categories
        categories = ["Electronics", "Clothing", "Books"]
        for name in categories:
            db.add(Category(name=name))
        db.commit()

        # Add 20 products
        for _ in range(20):
            product = Product(
                name=fake.word().capitalize() + " " + fake.word().capitalize(),
                description=fake.sentence(),
                price=round(random.uniform(10, 500), 2),
                category_id=random.randint(1, 3)
            )
            db.add(product)
        db.commit()

        # Add inventory entries
        products = db.query(Product).all()
        for product in products:
            inventory = Inventory(
                product_id=product.id,
                current_stock=random.randint(0, 50)
            )
            db.add(inventory)
        db.commit()

        # Add 100 sales (spread over last 90 days)
        for _ in range(100):
            product = random.choice(products)
            sale_date = datetime.now() - timedelta(days=random.randint(0, 90))
            sale = Sale(
                product_id=product.id,
                quantity=random.randint(1, 5),
                unit_price=product.price,
                total_price=product.price * random.randint(1, 5),
                sale_date=sale_date
            )
            db.add(sale)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    populate_data()