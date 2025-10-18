import redis, os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# ---------- CONFIG ----------
load_dotenv()
HOST = os.getenv("REDIS_HOST")
PORT = int(os.getenv("REDIS_PORT", 6379))
USER = os.getenv("REDIS_USER", "default")
PWD  = os.getenv("REDIS_PASSWORD")

r = redis.Redis(
    host=HOST, port=PORT, username=USER, password=PWD,
    ssl=False, decode_responses=True
)

def now(): return datetime.utcnow().isoformat()

# ---------- CREATE ----------
def create_data():
    print("\n=== CREATE TASKS ===")

    # 1. Users
    users = {
        "U002": ("Bilal Shah", "bilal@example.com", "111-2222"),
        "U003": ("Fatima Noor", "fatima@example.com", "111-3333"),
        "U004": ("Omar Qureshi", "omar@example.com", "111-4444"),
        "U005": ("Sara Iqbal", "sara@example.com", "111-5555"),
        "U006": ("Hassan Ahmed", "hassan@example.com", "111-6666")
    }
    for uid, (name, email, phone) in users.items():
        r.hset(f"help:user:{uid}", mapping={
            "name": name, "email": email, "phone": phone, "joined_at": now()
        })
        r.set(f"help:idx:user_email:{email}", uid)
    print("✅ 5 Users + Email Index created")

    # 2. Agents + Skills
    agents = {
        "A002": ("Ayesha", ["returns", "billing"]),
        "A003": ("Usman", ["technical", "orders"]),
        "A004": ("Bilal Agent", ["shipping", "returns"])
    }
    for aid, (name, skills) in agents.items():
        r.hset(f"help:agent:{aid}", mapping={"name": name, "load": 0})
        r.sadd(f"help:agent:{aid}:skills", *skills)
    print("✅ 3 Agents + Skills created")

    # 3. Tickets with mixed priorities
    tickets = {
        "T002": ( "U002", "Refund request", 5),
        "T003": ( "U003", "App crashes on checkout", 10),
        "T004": ( "U004", "Urgent: account hacked", 20),
        "T005": ( "U005", "Wrong item delivered", 5),
        "T006": ( "U006", "Payment failed", 1),
        "T007": ( "U002", "Shipping delay", 10),
        "T008": ( "U003", "Account locked", 20),
        "T009": ( "U004", "Change address", 1)
    }
    for tid, (uid, subject, prio) in tickets.items():
        key = f"help:ticket:{tid}"
        r.hset(key, mapping={
            "user_id": uid, "subject": subject, "status": "open",
            "priority": prio, "created_at": now(), "assigned_agent": "",
            "sla_due_at": (datetime.utcnow() + timedelta(hours=24)).isoformat()
        })
        r.zadd("help:queue:priority", {key: prio})
    print("✅ 8 Tickets created")

    # 4. Assign 3 tickets
    assigns = [("T002", "A002"), ("T003", "A003"), ("T004", "A002")]
    for tid, aid in assigns:
        r.hset(f"help:ticket:{tid}", "assigned_agent", aid)
        r.sadd(f"help:agent:{aid}:open_tickets", f"help:ticket:{tid}")
        r.hincrby(f"help:agent:{aid}", "load", 1)
    print("✅ 3 Tickets assigned")

    # 5. Push ≥2 log entries per ticket
    for tid in tickets.keys():
        r.rpush(f"help:ticket:{tid}:log", f"{now()}: created", f"{now()}: awaiting agent")
    print("✅ Logs pushed\n")

# ---------- READ ----------
def read_tasks():
    print("\n=== READ TASKS ===")

    # 1. Resolve user by email
    uid = r.get("help:idx:user_email:fatima@example.com")
    print("User ID via email:", uid)
    print("User HASH:", r.hgetall(f"help:user:{uid}"))

    # 2. Top-3 priority
    print("\nTop-3 highest priority tickets:")
    print(r.zrevrange("help:queue:priority", 0, 2, withscores=True))

    # 3. Agent’s open tickets
    print("\nAgent A002 open tickets:")
    for t in r.smembers("help:agent:A002:open_tickets"):
        print(t, "=>", r.hget(t, "subject"))

    # 4. Ticket log
    print("\nTicket:T004 log entries:", r.lrange("help:ticket:T004:log", 0, -1))

    # 5. Count tickets by status
    statuses = {}
    for k in r.scan_iter(match="help:ticket:*"):
        if k.count(":") == 2:
            s = r.hget(k, "status")
            statuses[s] = statuses.get(s, 0) + 1
    print("\nTicket counts by status:", statuses)

    # 6. Agents covering "returns"
    print("\nAgents with 'returns' skill:")
    for aid in ["A002", "A003", "A004"]:
        if r.sismember(f"help:agent:{aid}:skills", "returns"):
            print(aid, "->", r.hget(f"help:agent:{aid}", "name"))

# ---------- UPDATE ----------
def update_tasks():
    print("\n=== UPDATE TASKS ===")

    # 1. open → in_progress
    r.hset("help:ticket:T002", "status", "in_progress")
    r.rpush("help:ticket:T002:log", f"{now()}: in_progress")

    # 2. in_progress → on_hold
    r.hset("help:ticket:T002", "status", "on_hold")
    r.rpush("help:ticket:T002:log", f"{now()}: on_hold")

    # 3. Reassign ticket T004 A002 → A003
    r.hset("help:ticket:T004", "assigned_agent", "A003")
    r.srem("help:agent:A002:open_tickets", "help:ticket:T004")
    r.sadd("help:agent:A003:open_tickets", "help:ticket:T004")
    r.hincrby("help:agent:A002", "load", -1)
    r.hincrby("help:agent:A003", "load", 1)
    r.rpush("help:ticket:T004:log", f"{now()}: reassigned A002→A003")

    # 4. Extend sla_due_at
    r.hset("help:ticket:T002", "sla_due_at", (datetime.utcnow()+timedelta(days=3)).isoformat())

    # 5. Verify load
    print("Agent loads:",
          r.hget("help:agent:A002","load"),
          r.hget("help:agent:A003","load"))

    # 6. Fix subject typo
    r.hset("help:ticket:T002", "subject", "Refund request (updated)")

    print("✅ Update tasks completed.\n")

# ---------- DELETE ----------
def delete_tasks():
    print("\n=== DELETE TASKS ===")

    # 1. Close ticket
    r.hset("help:ticket:T003", "status", "closed")
    r.zrem("help:queue:priority", "help:ticket:T003")
    r.srem("help:agent:A003:open_tickets", "help:ticket:T003")
    r.hincrby("help:agent:A003", "load", -1)
    r.rpush("help:ticket:T003:log", f"{now()}: closed")

    # 2. Hard delete one demo ticket
    r.delete("help:ticket:T005", "help:ticket:T005:log")
    r.zrem("help:queue:priority", "help:ticket:T005")

    # 3. Delete a user & its index
    r.delete("help:user:U005", "help:idx:user_email:sara@example.com")

    # 4. Cleanup (optional)
    # for k in r.scan_iter(match="help:*"): r.delete(k)

    print("✅ Delete tasks executed.\n")

# ---------- MAIN ----------
if __name__ == "__main__":
    print("Connecting to Redis Cloud ...")
    print("PING ->", r.ping())

    create_data()
    read_tasks()
    update_tasks()
    delete_tasks()

    print("\n🎯 All Part-C operations complete!")
