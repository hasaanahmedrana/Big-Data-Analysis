from cassandra.cluster import Cluster
import sys
import time
from datetime import datetime, timedelta

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

# --- 3. Run DELETE Scenarios ---

print("--- 1. Delete a Wrong Event (Scenario 5.4.1) ---")
# GOAL: Remove a single event added by mistake.
# This is fast, but we MUST know the full primary key.
try:
    # Let's find an event to delete (e.g., for user_2)
    row_to_delete = session.execute(f"SELECT * FROM {TABLE_NAME} WHERE user_id = 'user_33' LIMIT 1").one()
    
    if row_to_delete:
        print(f"Found event to delete: user='{row_to_delete.user_id}', time='{row_to_delete.event_time}'")
        
        query1 = f"DELETE FROM {TABLE_NAME} WHERE user_id = %s AND event_time = %s AND event_id = %s;"
        
        start_time = time.time()
        session.execute(query1, (row_to_delete.user_id, row_to_delete.event_time, row_to_delete.event_id))
        end_time = time.time()
        
        print("SUCCESS: Deleted the single event.")
        print(f"** Query 1 Time Taken: {end_time - start_time:.6f} seconds **")
    else:
        print("Could not find an event for user_2 to delete.")

except Exception as e:
    print(f"Error running Query 1: {e}\n")


print("--- 2. Delete Data for One User (Scenario 5.4.2) ---")
# GOAL: Remove all events for a user who requested deletion.
# This is EXTREMELY fast and efficient in Cassandra.
try:
    user_to_delete = 'user_19' # The user we deleted in MySQL
    print(f"Attempting to delete all data for: {user_to_delete}")
    
    # We are deleting by the PARTITION KEY. This is what Cassandra is built for.
    query2 = f"DELETE FROM {TABLE_NAME} WHERE user_id = %s;"
    
    start_time = time.time()
    session.execute(query2, (user_to_delete,))
    end_time = time.time()
    
    print(f"SUCCESS: Deleted all data for user '{user_to_delete}'.")
    print(f"** Query 2 Time Taken: {end_time - start_time:.6f} seconds **")

except Exception as e:
    print(f"Error running Query 2: {e}\n")


print("--- 3. Old Data Cleanup (Scenario 5.4.3) ---")
# GOAL: Remove events older than 6 months.
# This is VERY INEFFICIENT to do as a DELETE operation.
try:
    print("Attempting to delete events older than 180 days...")
    
    # This requires a full table scan, just like the bad UPDATEs.
    # 1. Find all events (scan)
    query_find = f"SELECT user_id, event_time, event_id FROM {TABLE_NAME};"
    rows = session.execute(query_find)
    
    # 2. Check them and delete one-by-one
    cutoff_date = datetime.now() - timedelta(days=180)
    events_to_delete = []
    
    for row in rows:
        # Convert Cassandra's datetime to a standard Python datetime
        row_time = row.event_time
        if row_time < cutoff_date:
            events_to_delete.append((row.user_id, row.event_time, row.event_id))

    start_time = time.time()
    if events_to_delete:
        query_delete = f"DELETE FROM {TABLE_NAME} WHERE user_id = %s AND event_time = %s AND event_id = %s;"
        for event in events_to_delete:
            session.execute(query_delete, event)
    end_time = time.time()

    print(f"SUCCESS: Found and deleted {len(events_to_delete)} old events.")
    print(f"** Query 3 Time Taken: {end_time - start_time:.6f} seconds **")
    print("NOTE: The 'correct' way in Cassandra is to set a TTL (Time-To-Live) on insert.\n")

except Exception as e:
    print(f"Error running Query 3: {e}\n")


# --- 4. Clean up ---
finally:
    session.shutdown()
    cluster.shutdown()
    print("Connection closed.")