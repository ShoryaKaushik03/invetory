import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# MongoDB setup (use environment variable for connection string)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")  # Default to local MongoDB
client = MongoClient(MONGO_URI)
db = client["inventory_db"]
products_collection = db["products"]

class Product(BaseModel):
    name: str
    price: float
    quantity: int

@app.get("/health")
def health_check():
    try:
        client.admin.command('ping')
        return {"status": "success", "message": "MongoDB is connected!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get('/products')
def get_all_products():
    return [
        {"id": str(product["_id"]), "name": product["name"], "price": product["price"], "quantity": product["quantity"]}
        for product in products_collection.find()
    ]

@app.post('/products')
def create_product(product: Product):
    result = products_collection.insert_one(product.dict())
    return {"id": str(result.inserted_id), "name": product.name, "price": product.price, "quantity": product.quantity}

@app.get('/products/{product_id}')
def get_product(product_id: str):
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": str(product["_id"]), "name": product["name"], "price": product["price"], "quantity": product["quantity"]}