from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta, timezone
import calendar

client = MongoClient("mongodb://bookbazaar_app:AppPassw0rd!@localhost:27017/bookbazaar_db?authSource=bookbazaar_db")
db = client.bookbazaar_db

# Get the ID of the first book in the database (for C3)
target_book_id = ObjectId(db.books.find_one({}, { "_id": 1 })["_id"])

# ----------------------------
def c1_monthly_sales_by_category():
    """
    Rationale: Calculates total quantity sold and revenue for each book category
    per month over the last 6 months, helping the store track sales trends.
    """
    six_months_ago = datetime.now(timezone.utc) - timedelta(days=30*6)
    pipeline = [
        {"$unwind": "$items"},
        {"$lookup": {"from": "books", "localField": "items.bookId", "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$unwind": "$book.categories"},
        {"$match": {"createdAt": {"$gte": six_months_ago}}},
        {"$group": {"_id": {"month": {"$month": "$createdAt"}, "category": "$book.categories"},
                    "totalQty": {"$sum": "$items.qty"},
                    "totalRevenue": {"$sum": {"$multiply": ["$items.qty", "$items.priceAtPurchase"]}}}},
        {"$sort": {"_id.month": 1, "_id.category": 1}}
    ]
    print("C1) Monthly sales by category:")
    for doc in db.orders.aggregate(pipeline):
        month_num = doc['_id']['month']
        month_name = calendar.month_name[month_num]
        category = doc['_id']['category']
        total_qty = doc['totalQty']
        total_revenue = round(doc['totalRevenue'], 2)
        print(f"{month_name:<10} | Category: {category:<15} | Qty: {total_qty} | Revenue: {total_revenue}")
    print("-"*70)

# ----------------------------
def c2_top_10_bestsellers():
    """
    Rationale: Ranks books by quantity sold to determine the most popular books,
    assisting in marketing and inventory decisions.
    """
    pipeline = [
        {"$unwind": "$items"},
        {"$group": {"_id": "$items.bookId",
                    "totalQty": {"$sum": "$items.qty"},
                    "totalRevenue": {"$sum": {"$multiply": ["$items.qty", "$items.priceAtPurchase"]}}}},
        {"$lookup": {"from": "books", "localField": "_id", "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$project": {"bookId": "$_id", "title": "$book.title", "totalQty": 1, "totalRevenue": 1}},
        {"$sort": {"totalQty": -1}},
        {"$limit": 10}
    ]
    print("C2) Top 10 best-sellers:")
    for doc in db.orders.aggregate(pipeline):
        title = doc['title']
        total_qty = doc['totalQty']
        total_revenue = round(doc['totalRevenue'], 2)
        print(f"Title: {title:<35} | Qty Sold: {total_qty} | Revenue: {total_revenue}")
    print("-"*70)

# ----------------------------
def c3_also_bought():
    """
    Rationale: Identifies top 5 books frequently purchased together with a
    target book, useful for recommendation systems.
    """
    pipeline = [
        {"$match": {"items.bookId": target_book_id}},
        {"$unwind": "$items"},
        {"$match": {"items.bookId": {"$ne": target_book_id}}},
        {"$group": {"_id": "$items.bookId", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5},
        {"$lookup": {"from": "books", "localField": "_id", "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$project": {"bookId": "$_id", "title": "$book.title", "count": 1}}
    ]
    print("C3) Also-bought top 5:")
    for doc in db.orders.aggregate(pipeline):
        print(f"Title: {doc['title']:<35} | Co-purchased count: {doc['count']:>3}")
    print("-"*70)

# ----------------------------
def c4_vendor_dashboard():
    """
    Rationale: Provides key vendor metrics in one query: total sales in last
    30 days, average delivery time, and count of low stock books.
    """
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    pipeline = [
        {"$facet": {
            "salesLast30d": [
                {"$lookup": {"from": "orders", "localField": "_id", "foreignField": "items.bookId", "as": "orders"}},
                {"$unwind": "$orders"},
                {"$unwind": "$orders.items"},
                {"$match": {"orders.createdAt": {"$gte": thirty_days_ago}}},
                {"$group": {"_id": None, "revenue": {"$sum": {"$multiply": ["$orders.items.qty", "$orders.items.priceAtPurchase"]}}}}
            ],
            "avgDeliveryDays": [
                {"$match": {"deliveredAt": {"$exists": True}}},
                {"$project": {"diffDays": {"$divide": [{"$subtract": ["$deliveredAt", "$createdAt"]}, 1000*60*60*24]}}},
                {"$group": {"_id": None, "avgDeliveryDays": {"$avg": "$diffDays"}}}
            ],
            "lowStockCount": [
                {"$match": {"stock": {"$lt": 5}}},
                {"$count": "lowStockCount"}
            ]
        }}
    ]
    print("C4) Vendor dashboard:")
    for doc in db.books.aggregate(pipeline):
        sales = round(doc['salesLast30d'][0]['revenue'], 2) if doc['salesLast30d'] else 0
        avg_days = round(doc['avgDeliveryDays'][0]['avgDeliveryDays'], 2) if doc['avgDeliveryDays'] else 0
        low_stock = doc['lowStockCount'][0]['lowStockCount'] if doc['lowStockCount'] else 0
        print(f"Sales Last 30d: {sales:>10} | Avg Delivery Days: {avg_days:>6} | Low Stock Count: {low_stock:>3}")
    print("-"*70)

# ----------------------------
def c5_ratings_by_category():
    """
    Rationale: Computes average rating per category to evaluate customer
    satisfaction across different book categories.
    """
    pipeline = [
        {"$lookup": {"from": "books", "localField": "bookId", "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$unwind": "$book.categories"},
        {"$group": {"_id": "$book.categories", "avgRating": {"$avg": "$rating"}}}
    ]
    print("C5) Ratings by category:")
    for doc in db.reviews.aggregate(pipeline):
        print(f"Category: {doc['_id']:<15} | Avg Rating: {round(doc['avgRating'],2)}")
    print("-"*70)

# ----------------------------
def c6_author_leaderboard():
    """
    Rationale: Ranks authors in 'Programming' category by total revenue using
    window function to assign rank.
    """
    pipeline = [
        {"$unwind": "$items"},
        {"$lookup": {"from": "books", "localField": "items.bookId", "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$match": {"book.categories": "Programming"}},
        {"$group": {"_id": "$book.authors", "revenue": {"$sum": {"$multiply": ["$items.qty", "$items.priceAtPurchase"]}}}},
        {"$unwind": "$_id"},
        {"$setWindowFields": {"sortBy": {"revenue": -1}, "output": {"rank": {"$rank": {}}}}}
    ]
    print("C6) Author leaderboard (Programming):")
    for doc in db.orders.aggregate(pipeline):
        print(f"Author: {doc['_id']:<20} | Revenue: {round(doc['revenue'],2):>10} | Rank: {doc['rank']}")
    print("-"*70)

# ----------------------------
def c7_cohort_retention():
    """
    Rationale: Measures 60-day retention rate of users based on first order,
    indicating customer engagement and repeat purchase behavior.
    """
    pipeline = [
        {"$group": {"_id": "$userId", "firstOrder": {"$min": "$createdAt"}}},
        {"$lookup": {"from": "orders", "localField": "_id", "foreignField": "userId", "as": "orders"}},
        {"$project": {
            "firstOrder": 1,
            "retained": {"$size": {"$filter": {"input": "$orders", "cond": {"$and": [
                {"$gt": ["$$this.createdAt", "$firstOrder"]},
                {"$lte": ["$$this.createdAt", {"$add": ["$firstOrder", 1000*60*60*24*60]}]}
            ]}}}}
        }},
        {"$group": {"_id": None, "retentionRate": {"$avg": {"$cond": [{"$gt": ["$retained", 0]}, 1, 0]}}}}
    ]
    print("C7) Cohort retention (60-day):")
    for doc in db.orders.aggregate(pipeline):
        print(f"Retention Rate: {round(doc['retentionRate']*100,2)}%")
    print("-"*70)

# ----------------------------
def c8_inventory_anomalies():
    """
    Rationale: Detects mismatches between inventory logs and current stock,
    helping identify potential errors in stock management.
    """
    pipeline = [
        {"$group": {"_id": "$bookId", "deltaSum": {"$sum": "$delta"}}},
        {"$lookup": {"from": "books", "localField": "_id", "foreignField": "_id", "as": "book"}},
        {"$unwind": "$book"},
        {"$project": {"bookId": "$_id", "stock": "$book.stock", "deltaSum": 1, "diff": {"$subtract": ["$deltaSum", "$book.stock"]}}},
        {"$match": {"diff": {"$ne": 0}}}
    ]
    print("C8) Inventory anomalies:")
    for doc in db.inventory_logs.aggregate(pipeline):
        print(f"BookId: {str(doc['bookId'])[:6]}... | Stock: {doc['stock']} | Delta Sum: {doc['deltaSum']} | Diff: {doc['diff']}")
    print("-"*70)

# ----------------------------
def c9_price_buckets():
    """
    Rationale: Categorizes books into price buckets and computes average
    rating, useful for pricing analysis and customer insights.
    """
    pipeline = [
        {"$lookup": {"from": "reviews", "localField": "_id", "foreignField": "bookId", "as": "reviews"}},
        {"$project": {
            "title": 1,
            "priceBucket": {"$switch": {
                "branches": [
                    {"case": {"$lte": ["$price", 10]}, "then": "0-10"},
                    {"case": {"$lte": ["$price", 25]}, "then": "10-25"},
                    {"case": {"$lte": ["$price", 50]}, "then": "25-50"},
                    {"case": {"$lte": ["$price", 100]}, "then": "50-100"}
                ],
                "default": ">100"
            }},
            "avgRating": {"$avg": "$reviews.rating"}
        }}
    ]
    print("C9) Price buckets + avg rating:")
    for doc in db.books.aggregate(pipeline):
        print(f"Title: {doc['title']:<30} | Bucket: {doc['priceBucket']:<7} | Avg Rating: {round(doc['avgRating'],2) if doc['avgRating'] else 'N/A'}")
    print("-"*70)

# ----------------------------
def c10_text_search_recency():
    """
    Rationale: Performs text search for keywords with recency boost to return
    top relevant and recent books for search functionality.
    """
    db.books.create_index([("title", "text"), ("subtitle", "text"), ("description", "text")])
    pipeline = [
        {"$match": {"$text": {"$search": "machine learning deep learning"}}},
        {"$addFields": {"score": {"$meta": "textScore"}}},
        {"$sort": {"score": -1, "publishedYear": -1}},
        {"$limit": 10},
        {"$project": {"title": 1, "publishedYear": 1, "score": 1}}
    ]
    print("C10) Text search + recency boost:")
    for doc in db.books.aggregate(pipeline):
        print(f"Title: {doc['title']:<30} | Year: {doc['publishedYear']} | Score: {round(doc['score'],2)}")
    print("-"*70)

# ----------------------------
if __name__ == "__main__":
    all_objects = list(globals().items())

    print(" Docstrings of all aggregation functions:\n")
    for name, obj in all_objects:
        if callable(obj) and name.startswith('c'):  # filters c1..c10 functions
            print(f"{name}:\n{obj.__doc__}\n{'-'*70}\n")

    c1_monthly_sales_by_category()
    c2_top_10_bestsellers()
    c3_also_bought()
    c4_vendor_dashboard()
    c5_ratings_by_category()
    c6_author_leaderboard()
    c7_cohort_retention()
    c8_inventory_anomalies()
    c9_price_buckets()
    c10_text_search_recency()
    print("\n✅ All 10 aggregation pipelines executed successfully!")
