import redis, os, ssl
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("REDIS_HOST")
PORT = int(os.getenv("REDIS_PORT", 6379))
USER = os.getenv("REDIS_USER", "default")
PWD  = os.getenv("REDIS_PASSWORD")


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
r = redis.Redis(host=HOST, port=PORT, username=USER, password=PWD, ssl=False, decode_responses=True)

assert r.ping(), "Redis connection failed"
print("Connected to Redis Cloud!")

# --- USERS ---
r.hset("help:user:U001", mapping={
    "name": "Alice Smith",
    "email": "alice@example.com",
    "phone": "111-1111",
    "joined_at": "2025-10-05T08:00Z"
})
r.set("help:idx:user_email:alice@example.com", "U001")

# --- AGENT ---
r.hset("help:agent:A001", mapping={
    "name": "Agent One",
    "email": "a1@support.com",
    "load": 0
})
r.sadd("help:agent:A001:skills", "returns", "billing")

# --- TICKET ---
r.hset("help:ticket:T001", mapping={
    "user_id": "U001",
    "subject": "Payment failed",
    "status": "open",
    "priority": 20,
    "created_at": "2025-10-05T08:05Z",
    "assigned_agent": "A001",
    "sla_due_at": "2025-10-08T08:05Z"
})

# --- TICKET LOG ---
r.rpush("help:ticket:T001:log", "2025-10-05T08:06Z: created")

# --- PRIORITY QUEUE ---
r.zadd("help:queue:priority", {"help:ticket:T001": 20})

# --- AGENT OPEN TICKETS ---
r.sadd("help:agent:A001:open_tickets", "help:ticket:T001")

# --- ID COUNTERS ---
r.mset({
    "help:seq:users": 1,
    "help:seq:agents": 1,
    "help:seq:tickets": 1
})

print("Part B entities successfully created!")

# Optional verification
for key in [
    "help:user:U001",
    "help:idx:user_email:alice@example.com",
    "help:agent:A001",
    "help:agent:A001:skills",
    "help:ticket:T001",
    "help:ticket:T001:log",
    "help:queue:priority",
    "help:agent:A001:open_tickets"
]:
    print(f"{key:<40} -> {r.type(key)}")
