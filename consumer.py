import os
import time
from pymongo import MongoClient
from bson import ObjectId

# MongoDB setup (use environment variable for connection string)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")  # Default to local MongoDB
client = MongoClient(MONGO_URI)
db = client["inventory_db"]
products_collection = db["products"]
orders_collection = db["orders"]

while True:
    # Poll MongoDB for pending orders
    pending_orders = orders_collection.find({"status": "pending"})

    for order in pending_orders:
        product_id = order['product_id']
        quantity_ordered = order['quantity']

        # Fetch the product from MongoDB
        product = products_collection.find_one({"_id": ObjectId(product_id)})

        if product and product["quantity"] >= quantity_ordered:
            # Update product quantity
            new_quantity = product["quantity"] - quantity_ordered
            products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": {"quantity": new_quantity}})

            # Mark order as completed
            orders_collection.update_one({"_id": order["_id"]}, {"$set": {"status": "completed"}})
        else:
            # Handle refund logic if the product is unavailable
            orders_collection.update_one({"_id": order["_id"]}, {"$set": {"status": "refunded"}})

    # Delay to simulate polling
    time.sleep(5)
