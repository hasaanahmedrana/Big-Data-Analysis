from cassandra.cluster import Cluster
import sys

# --- 1. Configuration ---
CASSANDRA_HOST = 'localhost' # This is your host machine
CASSANDRA_PORT = 9042         # The port from your docker-compose
KEYSPACE_NAME = 'quickkart_keyspace'

# --- 2. Create Connection ---
try:
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect()
    print("Successfully connected to Cassandra cluster.")
except Exception as e:
    print(f"Error: Could not connect to Cassandra at {CASSANDRA_HOST}:{CASSANDRA_PORT}")
    print(e)
    sys.exit(1) # Exit the script if we can't connect

# --- 3. Create Keyspace (like a 'database') ---
try:
    print(f"Creating keyspace '{KEYSPACE_NAME}'...")
    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {KEYSPACE_NAME}
        WITH REPLICATION = {{ 'class' : 'SimpleStrategy', 'replication_factor' : 1 }};
    """)
    print("Keyspace created successfully (or already exists).")
except Exception as e:
    print(f"Error creating keyspace: {e}")
    cluster.shutdown()
    sys.exit(1)

# --- 4. Switch to the new Keyspace ---
try:
    session.set_keyspace(KEYSPACE_NAME)
    print(f"Switched to keyspace '{KEYSPACE_NAME}'.")
except Exception as e:
    print(f"Error switching to keyspace: {e}")
    cluster.shutdown()
    sys.exit(1)

# --- 5. Create the Table (The "Query-First" Design) ---
# This table is DESIGNED for the query: "Get recent events for one user"
TABLE_NAME = "events_by_user"
try:
    print(f"Creating table '{TABLE_NAME}'...")
    session.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id text,
        event_time timestamp,
        event_id int,
        
        -- All other data we want to retrieve
        session_id text,
        event_type text,
        product_id text,
        category text,
        price decimal,
        city text,
        device_type text,
        
        -- PRIMARY KEY (PartitionKey, ClusteringKey1, ClusteringKey2...)
        -- Partition by user_id, cluster by event_time (descending)
        PRIMARY KEY (user_id, event_time, event_id)
    ) WITH CLUSTERING ORDER BY (event_time DESC, event_id ASC);
    """)
    print("Table created successfully (or already exists).")
except Exception as e:
    print(f"Error creating table: {e}")

# --- 6. Clean up ---
finally:
    session.shutdown()
    cluster.shutdown()
    print("Connection closed.")