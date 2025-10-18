# redis_cleanup_partb.py
# Deletes all keys EXCEPT those starting with "help:" for safe cleanup.

import redis, os, ssl
from dotenv import load_dotenv

# Load credentials
load_dotenv()
HOST = os.getenv("REDIS_HOST")
PORT = int(os.getenv("REDIS_PORT", 6379))
USER = os.getenv("REDIS_USER", "default")
PWD  = os.getenv("REDIS_PASSWORD")

# Redis connection (skip cert verify for lab)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

r = redis.Redis(
    host=HOST,
    port=PORT,
    username=USER,
    password=PWD,
    ssl=False,  # You can change to True if SSL works
    decode_responses=True
)

assert r.ping(), "Redis connection failed"
print("Connected to Redis Cloud!")

# Find all keys
all_keys = list(r.scan_iter())
print(f"Total keys found: {len(all_keys)}")

# Filter out help:* keys
keys_to_delete = [k for k in all_keys if not k.startswith("help:")]

print(f"Keys to delete (excluding 'help:*'): {len(keys_to_delete)}")

if keys_to_delete:
    r.delete(*keys_to_delete)
    print("All non-'help:' keys deleted successfully!")
else:
    print("No non-'help:' keys found to delete.")
