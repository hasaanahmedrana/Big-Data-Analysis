## MongoDB Docker Lab — Step-by-Step Report


### Create Project Directory

Create a local folder for the lab:

```powershell
# Windows PowerShell
mkdir <mongo-db>
cd <mongo-db>
```

This will be your workspace for MongoDB lab files, scripts, and screenshots.

---

###  Run MongoDB in Docker

Start MongoDB container with root user credentials:

```powershell
docker run -d --name mongo-bookbazaar -p 27017:27017 -v mongo-bookbazaar-data:/data/db -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=StrongAdminPassword1! mongo:6.0
```

**Explanation:**

- `--name mongo-bookbazaar` → name of the container.
- `-p 27017:27017` → map container port 27017 to host.
- `-v mongo-bookbazaar-data:/data/db` → persistent storage.
- `-e MONGO_INITDB_ROOT_USERNAME=admin` → root username.
- `-e MONGO_INITDB_ROOT_PASSWORD=StrongAdminPassword1!` → root password.
- `mongo:6.0` → MongoDB version 6.0.

Check if the container is running:

```powershell
docker ps --filter name=mongo-bookbazaar
```

You should see `STATUS` as `Up` and port mapping `0.0.0.0:27017->27017/tcp`.

---

###  Install GUI for MongoDB (Mongo Express)

**Option 1: Mongo Express (Web GUI)** Run Mongo Express container linked to MongoDB:

```powershell
docker run -d --name mongo-express -p 8081:8081 -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin -e ME_CONFIG_MONGODB_ADMINPASSWORD=StrongAdminPassword1! -e ME_CONFIG_MONGODB_SERVER=mongo-bookbazaar --link mongo-bookbazaar:mongo mongo-express
```

- Exposes GUI at http://localhost:8081
- When you open the GUI, it asks for a **web login** (BasicAuth):
  - Username: `admin`
  - Password: `pass`
  - This login is for Mongo Express itself, not MongoDB.

**Option 2: MongoDB Compass (Desktop GUI)**

- Download: https://www.mongodb.com/try/download/compass
- Connect string:

```
mongodb://admin:StrongAdminPassword1!@localhost:27017/?authSource=admin
```

- Provides advanced visualizations, queries, and aggregation pipelines.

---

### Connect to MongoDB Shell (`mongosh`)

Open PowerShell and run:

```powershell
docker exec -it mongo-bookbazaar mongosh -u admin -p StrongAdminPassword1!
```

- Logs you in as the MongoDB admin user.
- You’ll see prompt like `test>` or `>`.

---

###  Create Database and Collection

**Option A: Using GUI (Mongo Express / Compass)**

1. Click **Create Database**.
2. Database Name: `bookbazaar_db`
3. First Collection Name: `books`

**Option B: Using MongoDB Shell**

```js
use bookbazaar_db   // switch/create database
db.createCollection("books")  // create first collection
```

- `{ "ok" : 1 }` indicates success.

---

###  Access MongoDB Shell Inside Docker (Quick Command)

Run this in PowerShell:

```powershell
docker exec -it mongo-bookbazaar mongosh -u admin -p StrongAdminPassword1!
```

- `docker exec -it mongo-bookbazaar` → enter the container interactively  
- `mongosh` → MongoDB shell  
- `-u admin -p StrongAdminPassword1!` → login as the admin user  

---

![](/Screenshots/1.png) 
![](/Screenshots/2.png) 
![](/Screenshots/3.png)