import pandas as pd
from sqlalchemy import create_engine
import time

# --- 1. Database Connection Configuration ---
# !! IMPORTANT: Change this password if you used a different one !!
PASSWORD = "hasaan"
HOST = "localhost"
PORT = "3307" 
DATABASE = "quickkart_db"
USER = "root"

# Create the connection string
connection_string = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

try:
    engine = create_engine(connection_string)
    print("Database connection successful.")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()

# --- 2. Read and Prepare Data ---
try:
    df = pd.read_csv("events.csv")
    print(f"Successfully read {len(df)} rows from events.csv")
    
    # IMPORTANT: Convert event_time string to datetime objects
    # This ensures MySQL saves it in the correct DATETIME format
    df['event_time'] = pd.to_datetime(df['event_time'])
    
    # Handle potential empty values (like product_id)
    # Pandas uses 'NaN' for empty, which SQL needs as 'None' (NULL)
    df = df.where(pd.notnull(df), None)

except FileNotFoundError:
    print("ERROR: events.csv not found.")
    print("Please make sure it's in the same directory as this script.")
    exit()
except Exception as e:
    print(f"Error processing CSV file: {e}")
    exit()

# --- 3. Load Data into MySQL ---
TABLE_NAME = "events"

print(f"Starting to load data into MySQL table '{TABLE_NAME}'...")
start_time = time.time()

try:
    # Use to_sql to load the dataframe into the SQL table
    # 'append' adds the data, 'replace' would drop the table first
    # 'if_exists='append'' is what we want.
    df.to_sql(TABLE_NAME, con=engine, if_exists='append', index=False)
    
    end_time = time.time()
    print(f"\n--- SUCCESS! ---")
    print(f"Successfully loaded {len(df)} events into MySQL.")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

except Exception as e:
    print(f"\n--- ERROR ---")
    print(f"An error occurred while loading data into MySQL: {e}")