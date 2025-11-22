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

# --- 3. Run UPDATE Scenarios ---

print("--- 1. Fix a Wrong City (Scenario 5.3.1) ---")
try:
    row_to_fix = session.execute(f"SELECT * FROM {TABLE_NAME} WHERE user_id = 'user_19' LIMIT 1").one()
    
    if row_to_fix:
        print(f"Found event to fix: user='{row_to_fix.user_id}', time='{row_to_fix.event_time}', city='{row_to_fix.city}'")
        
        query1 = f"UPDATE {TABLE_NAME} SET city = 'Sialkot' WHERE user_id = %s AND event_time = %s AND event_id = %s;"
        
        start_time = time.time()
        session.execute(query1, (row_to_fix.user_id, row_to_fix.event_time, row_to_fix.event_id))
        end_time = time.time()
        
        print("SUCCESS: Updated city to 'Sialkot'.")
        print(f"** Query 1 Time Taken: {end_time - start_time:.6f} seconds **")
        print("RESULT: This was very fast, but ONLY because we knew the full primary key.\n")
    else:
        print("Could not find an event for user_1 to fix.")

except Exception as e:
    print(f"Error running Query 1: {e}\n")


print("--- 2. Tag a Problem Session (Scenario 5.3.2) ---")
try:
    session_to_flag = 'session_1'
    print(f"Attempting to flag all events for session: {session_to_flag}")
    
    try: session.execute(f"ALTER TABLE {TABLE_NAME} ADD is_flagged boolean;")
    except Exception: pass # Ignore if column already exists
            
    start_time = time.time() # Start timer for the *whole operation*
    
    # 1. Read (inefficiently)
    query_find = f"SELECT * FROM {TABLE_NAME} WHERE session_id = %s ALLOW FILTERING;"
    rows = session.execute(query_find, (session_to_flag,))
    events_to_flag = list(rows)
    
    if events_to_flag:
        # 2. Update one-by-one
        query_update = f"UPDATE {TABLE_NAME} SET is_flagged = true WHERE user_id = %s AND event_time = %s AND event_id = %s;"
        for event in events_to_flag:
            session.execute(query_update, (event.user_id, event.event_time, event.event_id))
        
        end_time = time.time() # Stop timer
        
        print(f"SUCCESS: Found and flagged {len(events_to_flag)} events.")
        print(f"** Query 2 Time Taken: {end_time - start_time:.6f} seconds **")
        print("RESULT: This was extremely inefficient (full scan + N updates).\n")
    else:
        print(f"No events found for session '{session_to_flag}'.\n")

except Exception as e:
    print(f"Error running Query 2: {e}\n")


print("--- 3. Add a New Column (Scenario 5.3.3) ---")
try:
    try: session.execute(f"ALTER TABLE {TABLE_NAME} ADD payment_method text;")
    except Exception: pass # Ignore if column already exists

    print("Attempting to update all 'purchase' events...")
    
    start_time = time.time() # Start timer
    
    # 1. Read (inefficiently)
    query_find = f"SELECT * FROM {TABLE_NAME} WHERE event_type = 'purchase' ALLOW FILTERING;"
    rows = session.execute(query_find)
    purchase_events = list(rows)
    
    # 2. Update one-by-one
    query_update = f"UPDATE {TABLE_NAME} SET payment_method = 'card' WHERE user_id = %s AND event_time = %s AND event_id = %s;"
    
    for event in purchase_events:
        session.execute(query_update, (event.user_id, event.event_time, event.event_id))
    
    end_time = time.time() # Stop timer
    
    print(f"SUCCESS: Updated {len(purchase_events)} purchase events.")
    print(f"** Query 3 Time Taken: {end_time - start_time:.6f} seconds **")
    print("RESULT: Also very inefficient. Required a full scan and many individual updates.\n")

except Exception as e:
    print(f"Error running Query 3: {e}\n")


# --- 4. Clean up ---
finally:
    session.shutdown()
    cluster.shutdown()
    print("Connection closed.")