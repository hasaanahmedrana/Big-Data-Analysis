# BookBazaar Lab — Part A: Modeling & Validation

**Database:** bookbazaar\_db\
**Collections:** users, vendors, books, orders, reviews, inventory\_logs, sessions\
**Tools:** MongoDB Shell / Compass, Python bulk seeding script\
**Timestamps:** ISODate

---

## JSON Schema Validators

### Books Collection Validator

```js
db.runCommand({
  collMod: "books",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["title", "price", "vendorId", "stock", "authors"],
      properties: {
        title: { bsonType: "string" },
        price: { bsonType: "double" },
        vendorId: { bsonType: "objectId" },
        stock: { bsonType: "int", minimum: 0 },
        authors: { bsonType: "array", minItems: 1, items: { bsonType: "string" } }
      }
    }
  },
  validationLevel: "strict"
})
```

### Reviews Collection Validator

```js
db.runCommand({
  collMod: "reviews",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["bookId", "userId", "rating"],
      properties: {
        bookId: { bsonType: "objectId" },
        userId: { bsonType: "objectId" },
        rating: { bsonType: "int", minimum: 1, maximum: 5 }
      }
    }
  },
  validationLevel: "strict"
})
```
![](Screenshots\4.png)

---

##  Validator Rejection Examples

### Invalid Book Document

```js
db.books.insertOne({
  title: "Invalid Book",
  price: 2500.0
  // missing vendorId, stock, authors
})
```

**Expected Result:** MongoDB rejects insertion due to validator.\


### Invalid Review Document

```js
db.reviews.insertOne({
  bookId: ObjectId(),
  userId: ObjectId(),
  rating: 6 // invalid, should be 1–5
})
```

**Expected Result:** MongoDB rejects insertion due to validator.

![](Screenshots\5.png)



---

## Observations & Notes

- Validators enforce required fields and data types only for documents inserted **after validator creation**.
- Invalid documents are rejected immediately with detailed error messages.
- Bulk seeding using Python ensures consistent references between collections (e.g., orders reference valid users and books, inventory\_logs match stock changes).
- All timestamps are stored in **ISODate** format using `datetime.now(timezone.utc)` in Python.
- This setup ensures the database is ready for further lab tasks and queries.


