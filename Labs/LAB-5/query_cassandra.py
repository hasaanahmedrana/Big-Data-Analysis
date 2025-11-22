from cassandra.cluster import Cluster
import sys
import time # Import the time library

# --- 1. Configuration ---
CASSANDRA_HOST = 'localhost'
CASSANDRA_PORT = 9042
KEYSPACE_NAME = 'quickkart_keyspace'
TABLE_NAME = 'events_by_user'

# --- 2. Connect to Keyspace ---
try:
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect(KEYSPACE_NAME)
    print(f"Successfully connected to Cassandra keyspace '{KEYSPACE_NAME}'.\n")
except Exception as e:
    print(f"Error: Could not connect to Cassandra.")
    print(e)
    sys.exit(1)

# --- 3. Run READ Scenarios ---

print("--- 1. User History (Scenario 5.2.1) ---")
# GOAL: Show the latest 10 events of a specific user
try:
    user_to_find = 'user_5'
    query1 = f"SELECT * FROM {TABLE_NAME} WHERE user_id = %s LIMIT 10;"
    
    start_time = time.time() # Start timer
    rows = session.execute(query1, (user_to_find,))
    end_time = time.time()   # Stop timer
    
    list_of_rows = list(rows) # Consume the query results
    
    print(f"Showing {len(list_of_rows)} events for: {user_to_find}")
    print(f"** Query 1 Time Taken: {end_time - start_time:.6f} seconds **")
    print("RESULT: This query is fast because it uses the partition key.\n")

except Exception as e:
    print(f"Error running Query 1: {e}\n")


print("--- 2. Product Popularity (Scenario 5.2.2) ---")
# GOAL: Find how many times a specific product was purchased
try:
    product_to_find = 'prod_20'
    query2 = f"SELECT * FROM {TABLE_NAME} WHERE event_type = 'purchase' AND product_id = %s ALLOW FILTERING;"
    
    start_time = time.time() # Start timer
    rows = session.execute(query2, (product_to_find,))
    list_of_rows = list(rows) # Consume the query results
    end_time = time.time()   # Stop timer
    
    purchase_count = len(list_of_rows)
    
    print(f"Found {purchase_count} purchases for product: {product_to_find}")
    print(f"** Query 2 Time Taken: {end_time - start_time:.6f} seconds **")
    print("RESULT: This query is 'slow' (inefficient) because it requires ALLOW FILTERING.\n")

except Exception as e:
    print(f"Error running Query 2: {e}\n")


print("--- 3. City-wise Purchases (Scenario 5.2.3) ---")
# GOAL: Find how many purchases happened in each city
try:
    query3 = f"SELECT city, event_type FROM {TABLE_NAME} WHERE event_type = 'purchase' ALLOW FILTERING;"
    
    start_time = time.time() # Start timer
    rows = session.execute(query3)
    list_of_rows = list(rows) # Consume the query results
    end_time = time.time()   # Stop timer
    
    city_counts = {}
    for row in list_of_rows:
        city = row.city
        if city in city_counts:
            city_counts[city] += 1
        else:
            city_counts[city] = 1
            
    print("Purchase counts by city (from a full table scan):")
    for city, count in city_counts.items():
        print(f"  {city}: {count} purchases")
    
    print(f"** Query 3 Time Taken: {end_time - start_time:.6f} seconds **")
    print("RESULT: Also 'slow' (inefficient) design. Full scan + Python aggregation.\n")

except Exception as e:
    print(f"Error running Query 3: {e}\n")


# --- 4. Clean up ---
finally:
    session.shutdown()
    cluster.shutdown()
    print("Connection closed.")