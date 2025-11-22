from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta, timezone

print("Starting CRUD operations...")


client = MongoClient("mongodb://bookbazaar_app:AppPassw0rd!@localhost:27017/bookbazaar_db?authSource=bookbazaar_db")
db = client.bookbazaar_db

# Fetchong sample IDs for use in queries
user_id = ObjectId(db.users.find_one({}, { "_id": 1 })["_id"])
vendor_id = ObjectId(db.vendors.find_one({}, { "_id": 1 })["_id"])
book_id = ObjectId(db.books.find_one({}, { "_id": 1 })["_id"])

# ----------------------------
# CREATE
# ----------------------------

# B1) Vendor adds a new book (initial stock + tags)
db.books.insert_one({
    "title": "Advanced Data Science",
    "subtitle": "Techniques and Tools",
    "authors": ["John Doe"],
    "publisher": "Tech Press",
    "publishedYear": 2025,
    "categories": ["Data Science"],
    "price": 50.0,
    "currency": "PKR",
    "isbn13": "978-0-123456-78-9",
    "pages": 350,
    "language": "English",
    "vendorId": vendor_id,
    "tags": ["New", "Bestseller"],
    "stock": 20,
    "description": "Introductory book for advanced Data Science.",
    "createdAt": datetime.now(timezone.utc)
})

# B2) Register a user with two addresses (role customer)
db.users.insert_one({
    "name": "Alice Smith",
    "email": "alice@example.com",
    "phone": "03001234567",
    "role": "customer",
    "addresses": [
        {"label": "Home", "address": "123 Main Street, Lahore"},
        {"label": "Office", "address": "456 Business Ave, Lahore"}
    ],
    "createdAt": datetime.now(timezone.utc)
})

# B3) Bulk insert 10 books for a vendor (same publisher, different titles)
bulk_books = []
for i in range(1, 11):
    bulk_books.append({
        "title": f"Data Science Volume {i}",
        "subtitle": "Comprehensive Guide",
        "authors": ["Jane Doe"],
        "publisher": "Tech Press",
        "publishedYear": 2025,
        "categories": ["Data Science"],
        "price": float(45 + i),
        "currency": "PKR",
        "isbn13": f"978-0-123456-8{i}-9",
        "pages": 300 + i*5,
        "language": "English",
        "vendorId": vendor_id,
        "tags": ["New"],
        "stock": 15,
        "description": f"Volume {i} of Data Science series",
        "createdAt": datetime.now(timezone.utc)
    })
db.books.insert_many(bulk_books)

# ----------------------------
# READ
# ----------------------------

print("Reading data...")
print('-'*30)
print("B4: Books in category 'Data Science' with 20 ≤ price ≤ 60; project title, price, vendorId, sort by price asc")
# B4) Books in category "Data Science" with 20 ≤ price ≤ 60; project title, price, vendorId, sort by price asc
for book in db.books.find({"categories": "Data Science", "price": {"$gte": 20, "$lte": 60}},
                          {"title": 1, "price": 1, "vendorId": 1, "_id": 0}).sort("price", 1):
    print(book)

print('-'*30)
print("B5: Top 5 newest books (publishedYear) with stock > 0")
# B5) Top 5 newest books (publishedYear) with stock > 0
for book in db.books.find({"stock": {"$gt": 0}}).sort("publishedYear", -1).limit(5):
    print(book)

print('-'*30)
print("B6: Last 3 orders for a userId with status, createdAt, itemCount")

# B6) For a userId, fetch last 3 orders with fields: status, createdAt, itemCount
user_id = user_id  # Replace with actual userId if needed
for order in db.orders.find({"userId": user_id}, {"status": 1, "createdAt": 1, "items": 1, "_id": 0}).sort("createdAt", -1).limit(3):
    print({
        "status": order["status"],
        "createdAt": order["createdAt"],
        "itemCount": len(order["items"])
    })

print('-'*30)
# ----------------------------
# UPDATE
# ----------------------------


# B7) Increase price by 5% for all books of a given publisher where price < 25
db.books.update_many({"publisher": "Tech Press", "price": {"$lt": 25}}, {"$mul": {"price": 1.05}})

# B8) Upsert review (if exists: update rating/body; else insert)
db.reviews.update_one(
    {"bookId": book_id, "userId": user_id},
    {"$set": {"rating": 5, "title": "Excellent", "body": "Updated review text", "createdAt": datetime.now(timezone.utc)}},
    upsert=True
)

# B9) Normalize city: change user address "Lahore" → "Lahore City" only where label: "Home"
db.users.update_many(
    {"addresses.address": {"$regex": "Lahore"}},
    {"$set": {"addresses.$[homeAddr].address": "Lahore City"}},
    array_filters=[{"homeAddr.label": "Home", "homeAddr.address": {"$regex": "Lahore"}}]
)

# ----------------------------
# DELETE
# ----------------------------

# B10) Delete orphan reviews (where bookId no longer exists)
existing_book_ids = [b["_id"] for b in db.books.find({}, {"_id": 1})]
db.reviews.delete_many({"bookId": {"$nin": existing_book_ids}})

# B11) Delete vendors with status: "SUSPENDED" and no books
vendors_with_books = [b["vendorId"] for b in db.books.find({}, {"vendorId": 1})]
db.vendors.delete_many({"status": "SUSPENDED", "_id": {"$nin": vendors_with_books}})

# B12) Delete sessions older than 7 days
seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
db.sessions.delete_many({"createdAt": {"$lt": seven_days_ago}})

print("All CRUD scenarios executed successfully!")
