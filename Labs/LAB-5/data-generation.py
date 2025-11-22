import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# --- 1. Configuration ---
fake = Faker()

NUM_USERS = 100 # [cite: 25]
NUM_PRODUCTS = 250 # [cite: 26]
NUM_EVENTS = 4000 # [cite: 27]

EVENT_TYPES = ['open_app', 'view_product', 'add_to_cart', 'purchase', 'logout'] # [cite: 36]
CITIES = ['Lahore', 'Karachi', 'Islamabad', 'Rawalpindi', 'Faisalabad'] # [cite: 40]
DEVICES = ['web', 'android', 'ios'] # [cite: 41]
CATEGORIES = ['Electronics', 'Grocery', 'Clothing', 'Home & Kitchen', 'Sports'] # [cite: 38]

print("Starting data generation...")

# --- 2. Create Users and Products ---
users = [f'user_{i+1}' for i in range(NUM_USERS)]
products = []
for i in range(NUM_PRODUCTS):
    products.append({
        'product_id': f'prod_{i+1}',
        'category': random.choice(CATEGORIES),
        'price': round(random.uniform(5.0, 1000.0), 2)
    })

# --- 3. Generate Events ---
events = []
event_id_counter = 1
session_id_counter = 1

# We'll create events session by session to follow the logic rules
while len(events) < NUM_EVENTS:
    
    user_id = random.choice(users)
    session_id = f'session_{session_id_counter}'
    session_id_counter += 1
    
    device = random.choice(DEVICES)
    city = random.choice(CITIES)
    session_time = fake.date_time_between(start_date='-30d', end_date='now')
    
    # Rule: 'open_app' usually comes first [cite: 44]
    events.append({
        'event_id': event_id_counter,
        'user_id': user_id,
        'session_id': session_id,
        'event_time': session_time,
        'event_type': 'open_app',
        'product_id': None,
        'category': None,
        'price': None,
        'city': city,
        'device_type': device
    })
    event_id_counter += 1
    
    # Decide how many actions in this session (e.g., 1 to 15)
    actions_in_session = random.randint(1, 15)
    cart = [] # Keep track of items added to cart in this session
    
    for _ in range(actions_in_session):
        if len(events) >= NUM_EVENTS:
            break
            
        session_time += timedelta(minutes=random.randint(1, 10))
        
        # Choose a random product for this event
        product = random.choice(products)
        
        # Choose event type
        # Make 'view_product' most common
        event_type = random.choices(
            ['view_product', 'add_to_cart', 'purchase', 'logout'], 
            weights=[0.6, 0.2, 0.1, 0.1], 
            k=1
        )[0]
        
        # Rule: 'purchase' only after 'add_to_cart' [cite: 43]
        if event_type == 'purchase':
            if not cart: # If cart is empty, can't purchase. Change to 'view_product'
                event_type = 'view_product'
            else:
                # Purchase an item from the cart
                product = random.choice(cart)
                cart.remove(product) # Remove from cart after purchase
        
        if event_type == 'add_to_cart':
            cart.append(product)
            
        if event_type == 'logout':
            # End the session
            events.append({
                'event_id': event_id_counter,
                'user_id': user_id,
                'session_id': session_id,
                'event_time': session_time,
                'event_type': 'logout',
                'product_id': None,
                'category': None,
                'price': None,
                'city': city,
                'device_type': device
            })
            event_id_counter += 1
            break # Exit session loop
        
        # Add the event
        events.append({
            'event_id': event_id_counter,
            'user_id': user_id,
            'session_id': session_id,
            'event_time': session_time,
            'event_type': event_type,
            'product_id': product['product_id'],
            'category': product['category'],
            'price': product['price'],
            'city': city,
            'device_type': device
        })
        event_id_counter += 1

# --- 4. Save to CSV ---
df = pd.DataFrame(events)
# Ensure we have the exact 10 columns in the correct order
df = df[[
    'event_id', 'user_id', 'session_id', 'event_time', 'event_type', 
    'product_id', 'category', 'price', 'city', 'device_type'
]] # [cite: 31-41]

# Trim if we overshot the number of events
if len(df) > NUM_EVENTS:
    df = df.iloc[:NUM_EVENTS]

df.to_csv('events.csv', index=False)

print(f"Successfully generated {len(df)} events in 'events.csv'")
print("\nHere's a sample of your data:")
print(df.head())
