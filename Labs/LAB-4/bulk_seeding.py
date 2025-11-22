from pymongo import MongoClient
from faker import Faker
from random import randint, choice, sample
from datetime import datetime, timedelta, timezone
from bson import ObjectId
import uuid

fake = Faker()

# Connect to MongoDB using app user
client = MongoClient("mongodb://bookbazaar_app:AppPassw0rd!@localhost:27017/bookbazaar_db?authSource=bookbazaar_db")
db = client.bookbazaar_db

# Clear collections if already exist
for coll in ["users", "vendors", "books", "orders", "reviews", "inventory_logs", "sessions"]:
    db[coll].delete_many({})

# 1️⃣ Users (>=12)
users = []
roles = ["customer", "vendor", "admin"]
for _ in range(12):
    users.append({
        "_id": ObjectId(),
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "role": choice(roles),
        "addresses": [fake.address()],
        "createdAt": datetime.now(timezone.utc)
    })
db.users.insert_many(users)

# 2️⃣ Vendors (>=5)
vendors = []
statuses = ["ACTIVE", "SUSPENDED"]
for _ in range(5):
    vendors.append({
        "_id": ObjectId(),
        "name": fake.company(),
        "legalName": fake.company_suffix(),
        "city": fake.city(),
        "tags": sample(["Books", "Education", "AI", "Fiction", "Science"], 2),
        "rating": round(randint(10, 50)/10, 1),
        "status": choice(statuses),
        "createdAt": datetime.now(timezone.utc)
    })
db.vendors.insert_many(vendors)

# 3️⃣ Books (>=60)
categories_list = ["AI", "Fiction", "Science", "Math", "History", "Programming"]
books = []
for _ in range(60):
    books.append({
        "_id": ObjectId(),
        "title": fake.sentence(nb_words=4),
        "subtitle": fake.sentence(nb_words=6),
        "authors": [fake.name() for _ in range(randint(1,2))],
        "publisher": fake.company(),
        "publishedYear": randint(2000,2025),
        "categories": sample(categories_list, randint(1,2)),
        "price": round(randint(500, 5000)/10, 2),
        "currency": "PKR",
        "isbn13": fake.isbn13(),
        "pages": randint(100, 1000),
        "language": "English",
        "vendorId": choice(vendors)["_id"],
        "tags": sample(["New", "Bestseller", "Discount", "Limited"], randint(1,2)),
        "stock": randint(1,50),
        "description": fake.paragraph()
    })
db.books.insert_many(books)

# 4️⃣ Orders (>=80)
statuses = ["PLACED","PAID","SHIPPED","DELIVERED","CANCELLED"]
payment_methods = ["Credit Card","Cash","PayPal"]
orders = []
for _ in range(80):
    user = choice(users)
    order_items = []
    for _ in range(randint(1,3)):
        book = choice(books)
        order_items.append({
            "bookId": book["_id"],
            "qty": randint(1,3),
            "priceAtPurchase": book["price"]
        })
    created_at = datetime.now(timezone.utc) - timedelta(days=randint(0,30))
    delivered_at = created_at + timedelta(days=randint(1,10)) if choice([True, False]) else None
    orders.append({
        "_id": ObjectId(),
        "userId": user["_id"],
        "items": order_items,
        "status": choice(statuses),
        "shippingAddress": user["addresses"][0],
        "payment": {"method": choice(payment_methods), "paidAt": created_at if choice([True, False]) else None},
        "createdAt": created_at,
        "deliveredAt": delivered_at
    })
db.orders.insert_many(orders)

# 5️⃣ Reviews (>=120)
reviews = []
for _ in range(120):
    reviews.append({
        "_id": ObjectId(),
        "bookId": choice(books)["_id"],
        "userId": choice(users)["_id"],
        "rating": randint(1,5),
        "title": fake.sentence(nb_words=4),
        "body": fake.paragraph(),
        "createdAt": datetime.now(timezone.utc)
    })
db.reviews.insert_many(reviews)

# 6️⃣ Inventory Logs (>=150)
reasons = ["restock","sale","return","adjustment"]
inventory_logs = []
for _ in range(150):
    book = choice(books)
    vendor = choice(vendors)
    delta = randint(-5,10)
    inventory_logs.append({
        "_id": ObjectId(),
        "bookId": book["_id"],
        "vendorId": vendor["_id"],
        "delta": delta,
        "reason": choice(reasons),
        "createdAt": datetime.now(timezone.utc)
    })
db.inventory_logs.insert_many(inventory_logs)

# 7️⃣ Sessions (>=10)
sessions = []
for _ in range(10):
    sessions.append({
        "_id": ObjectId(),
        "userId": choice(users)["_id"],
        "token": uuid.uuid4().hex,
        "createdAt": datetime.now(timezone.utc)
    })
db.sessions.insert_many(sessions)

print("✅ Bulk seeding completed successfully!")
