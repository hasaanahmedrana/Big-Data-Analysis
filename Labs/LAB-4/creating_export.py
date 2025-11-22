import os
import json
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

client = MongoClient("mongodb://bookbazaar_app:AppPassw0rd!@localhost:27017/bookbazaar_db?authSource=bookbazaar_db")
db = client.bookbazaar_db


export_dir = "./exports"
os.makedirs(export_dir, exist_ok=True)

collections = ["books", "orders", "reviews", "inventory_logs", "users", "sessions","vendors"]

def serialize_bson(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, list):
        return [serialize_bson(x) for x in obj]
    if isinstance(obj, dict):
        return {k: serialize_bson(v) for k, v in obj.items()}
    return obj

# -----------------------------
for coll_name in collections:
    coll = db[coll_name]
    docs = list(coll.find().limit(10))  # small export
    docs_serialized = [serialize_bson(doc) for doc in docs]

    with open(os.path.join(export_dir, f"{coll_name}.json"), "w", encoding="utf-8") as f:
        json.dump(docs_serialized, f, indent=4)
    
    print(f"Exported {len(docs_serialized)} documents from '{coll_name}' to {export_dir}/{coll_name}.json")

print("\n All exports completed successfully!")
