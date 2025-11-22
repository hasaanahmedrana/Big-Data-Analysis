# 04_indexing_simplified.md

## D1) Create 4 Indexes

### Books Collection – Single-field Index
```javascript
db.books.createIndex({ price: 1 })
```
**Reason:** Allows efficient range queries and sorting on book prices, improving query performance when filtering or sorting by price.

---

### 2Books Collection – Compound Index
```javascript
db.books.createIndex({ categories: 1, price: 1 })
```
**Reason:** Optimizes queries filtering by category and then sorting by price, e.g., “find all books in category X sorted by price ascending.”

---

###  Books Collection – Text Index
```javascript
db.books.createIndex({ title: "text", subtitle: "text", description: "text" })
```
**Reason:** Supports efficient text search across multiple fields (title, subtitle, description), useful for search features.

---

###  Orders Collection – Compound Index
```javascript
db.orders.createIndex({ userId: 1, createdAt: -1 })
```
**Reason:** Speeds up queries fetching a user's recent orders by allowing filtering on `userId` and sorting by `createdAt` descending.

---

```javascript
db.books.getIndexes()
db.orders.getIndexes()
```
![alt text](/Screenshots/16.png)
![alt text](/Screenshots/17.png)



## D2) Verify with explain("executionStats")

### Query A: Category + Price
```javascript
db.books.find({ categories: "Programming" }).sort({ price: 1 }).explain("executionStats")
```
**Predicted Index Usage:** Uses `{ categories: 1, price: 1 }` compound index.

**Interpretation:**
- `nReturned`: Number of documents returned.
- `totalDocsExamined`: Number of documents scanned. Ideally, `totalDocsExamined ≈ nReturned`, confirming efficient index use.


![](/Screenshots/18.png)

---

### Query B: User's Last 3 Orders
```javascript
db.orders.find({ userId: ObjectId("USER_ID_HERE") }).sort({ createdAt: -1 }).limit(3).explain("executionStats")
```
**Predicted Index Usage:** Uses `{ userId: 1, createdAt: -1 }` compound index.

**Interpretation:**
- Index allows quick retrieval of recent orders for a user.
- Compare `totalDocsExamined` with `nReturned` to verify efficiency.

![](/Screenshots/19.png)

---

### Query C: Text Search
```javascript
db.books.find({ $text: { $search: "machine learning" } }).explain("executionStats")
```
**Predicted Index Usage:** Uses text index on `title, subtitle, description`.

**Interpretation:**
- Text index avoids full collection scan.
- `nReturned` shows matching documents; `totalDocsExamined` should be lower than total docs, confirming index use.

![](/Screenshots/20.png)

## D3) Maintenance

###  Drop a Non-_id_ Index
```javascript
db.books.dropIndex({ price: 1 })
```

###  Recreate the Dropped Index
```javascript
db.books.createIndex({ price: 1 })
```

![](/Screenshots/21.png)

### Best Practices
- Create indexes based on frequently used queries and filters.
- Prefer **compound indexes** for queries that filter and sort together.
- Use **text indexes** only for search-heavy fields.
- Avoid over-indexing; each index increases write overhead.
- Periodically review `totalDocsExamined` using `explain()`.
- Drop unused indexes to save storage and improve write performance.
- Consider **multikey indexes** for array fields if queries filter on array elements.

### Optional +3%: Multikey Index
```javascript
db.books.createIndex({ authors: 1 })
```
**Benefiting Query:**
```javascript
db.books.find({ authors: "John Doe" }).explain("executionStats")
```
**Summary:** Index allows fast retrieval of all books by a specific author in the authors array.

