import pandas as pd
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
from decimal import Decimal
import sys
import time

# --- 1. Configuration ---
CASSANDRA_HOST = 'localhost'
CASSANDRA_PORT = 9042
KEYSPACE_NAME = 'quickkart_keyspace'
TABLE_NAME = 'events_by_user'

# --- 2. Connect to Keyspace ---
try:
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect(KEYSPACE_NAME)
    print(f"Successfully connected to Cassandra keyspace '{KEYSPACE_NAME}'.")
except Exception as e:
    print(f"Error: Could not connect to Cassandra keyspace.")
    print(e)
    sys.exit(1)

# --- 3. Read and Prepare Data ---
try:
    df = pd.read_csv("events.csv")
    print(f"Successfully read {len(df)} rows from events.csv")
    
    # Convert event_time string to datetime objects
    df['event_time'] = pd.to_datetime(df['event_time'])
    
    # Replace Pandas' 'NaN' with 'None', which Cassandra understands as NULL
    df = df.where(pd.notnull(df), None)
    
    # Convert float prices to Decimal for Cassandra's decimal type
    # Use .astype(str) as an intermediate step to avoid float precision issues
    df['price'] = df['price'].apply(lambda x: Decimal(str(x)) if x is not None else None)

except FileNotFoundError:
    print("ERROR: events.csv not found.")
    sys.exit(1)
except Exception as e:
    print(f"Error processing CSV file: {e}")
    sys.exit(1)

# --- 4. Prepare the INSERT Statement ---
try:
    # This prepared statement is a template, which is much faster
    insert_query = session.prepare(f"""
        INSERT INTO {TABLE_NAME} (
            user_id, event_time, event_id, session_id, event_type,
            product_id, category, price, city, device_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """)
except Exception as e:
    print(f"Error preparing insert query: {e}")
    cluster.shutdown()
    sys.exit(1)

# --- 5. Load Data Row by Row ---
print(f"Starting to load {len(df)} events into Cassandra...")
start_time = time.time()

for index, row in df.iterrows():
    try:
        session.execute(
            insert_query,
            (
                row['user_id'],
                row['event_time'],
                row['event_id'],
                row['session_id'],
                row['event_type'],
                row['product_id'],
                row['category'],
                row['price'],
                row['city'],
                row['device_type']
            )
        )
        
        # Print a progress update every 500 rows
        if (index + 1) % 500 == 0:
            print(f"  ... inserted {index + 1} rows.")
            
    except Exception as e:
        print(f"Error inserting row {index}: {row.to_dict()}")
        print(e)
        break # Stop on error

# --- 6. Clean up ---
end_time = time.time()
print(f"\n--- SUCCESS! ---")
print(f"Successfully loaded {len(df)} events into Cassandra.")
print(f"Time taken: {end_time - start_time:.2f} seconds")

session.shutdown()
cluster.shutdown()
print("Connection closed.")