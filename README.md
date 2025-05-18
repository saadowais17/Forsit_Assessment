# E-commerce Admin API

## Features
- **Sales Analytics**
  - Filter sales by date range, product, or category
  - Revenue reports (daily/weekly/monthly/annual)
- **Inventory Management**
  - Real-time stock level tracking
  - Low-stock alerts
  - Inventory change history
- **Product Management**
  - Add new products with categories
  - Update product details

## Technologies
- **Backend**: Python 3.10, FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/saadowais17/Forsit_Assessment.git
   cd Forsit_Assessment

2. Set up virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Database setup:
   Create database using db_queries.sql
   Populate sample data:
   ```bash
   python scripts/demo_data.py

5. Configure environment variables:
   Create .env file:
   ```bash
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=ecommerce_db

5. Run the Application:
   uvicorn app.main:app --reload


## API Endpoints


| HTTP Method | Endpoint                         | Description                                              | Request Body             | Query Parameters                         | Response                         |
|-------------|----------------------------------|----------------------------------------------------------|--------------------------|-------------------------------------------|----------------------------------|
| POST        | `/products`                      | Add a new product                                        | `ProductCreate`          | -                                         | Product object                   |
| POST        | `/sales`                         | Add a new sale record                                    | `SaleCreate`             | -                                         | Sale object                      |
| GET         | `/sales`                         | List sales with optional filters                         | -                        | `start_date`, `end_date`, `product_id`   | List of `SaleResponse`          |
| GET         | `/sales/category/{category_id}`  | Get sales by product category                            | -                        | `category_id` (path param)                | List of `SaleResponse`          |
| GET         | `/revenue/{period}`              | Get revenue grouped by time period                       | -                        | `period` (path param: daily/weekly/...)   | List of revenue dicts           |
| PATCH       | `/inventory/{product_id}`        | Update stock quantity of a product                       | `InventoryUpdate`        | `product_id` (path param)                | Updated product or 404 error    |
| GET         | `/inventory/low-stock`           | List products with stock below the given threshold       | -                        | `threshold` (default = 10)                | List of low-stock products      |
