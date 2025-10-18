# Redis Helpdesk System - Lab 3

A comprehensive Redis-based helpdesk system demonstrating advanced Redis data structures and CRUD operations. This project implements a complete customer support system with users, agents, tickets, priority queues, and audit logging.

## 🚀 Features

- **User Management**: Customer registration with email indexing
- **Agent System**: Support agents with skill-based assignment
- **Ticket Management**: Priority-based ticket queuing and assignment
- **Audit Logging**: Complete ticket history tracking
- **Real-time Operations**: Efficient Redis data structures for fast queries
- **CRUD Operations**: Full Create, Read, Update, Delete functionality

## 📋 Prerequisites

- Python 3.10 or higher
- Redis Cloud account (or local Redis instance)
- Git
- Docker (optional, for Redis Insight GUI)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd LAB-3
```

### 2. Install Dependencies

Using `uv` (recommended):
```bash
uv sync
```

Or using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the project root:

```env
REDIS_HOST=your-redis-host
REDIS_PORT=your-redis-port
REDIS_USER=default
REDIS_PASSWORD=your-redis-password
```

**For Redis Cloud:**
1. Sign up at [Redis Cloud](https://redis.com/try-free/)
2. Create a new database
3. Copy the connection details to your `.env` file

**For Local Redis:**
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_USER=default
REDIS_PASSWORD=
```

## 🏗️ Project Structure

```
LAB-3/
├── config.py              # Redis connection configuration
├── part-b-model-setup.py  # Data model initialization
├── part-c-crud-ops.py     # CRUD operations implementation
├── delete.py              # Cleanup utilities
├── main.py                # Entry point
├── pyproject.toml         # Project dependencies
├── .env                   # Environment variables (create this)
└── Screenshots/           # Execution documentation
    ├── 1.png - 11.png
```

## 🚀 Usage

### Part A: Connection Setup

Test your Redis connection:

```bash
python config.py
```

Expected output:
```
🔌 Pinging Redis Cloud …
Response: True
Connected successfully via TLS!
```

### Part B: Data Model Setup

Initialize the helpdesk system with sample data:

```bash
python part-b-model-setup.py
```

This creates:
- 1 sample user (Alice Smith)
- 1 sample agent (Agent One)
- 1 sample ticket (Payment failed)
- Priority queue structure
- Audit logging system

### Part C: CRUD Operations

Run the complete CRUD operations demo:

```bash
python part-c-crud-ops.py
```

This demonstrates:
- **CREATE**: 5 users, 3 agents, 8 tickets with assignments
- **READ**: User lookup, priority queues, agent tickets, status counts
- **UPDATE**: Status changes, reassignments, SLA extensions
- **DELETE**: Ticket closure, data cleanup

### Cleanup

Remove non-helpdesk keys from Redis:

```bash
python delete.py
```

## 📊 Data Model

### Redis Data Structures Used

| Structure | Purpose | Example |
|-----------|---------|---------|
| **Hash** | User/Agent/Ticket data | `help:user:U001` |
| **String** | Email index | `help:idx:user_email:alice@example.com` |
| **Set** | Agent skills, open tickets | `help:agent:A001:skills` |
| **Sorted Set** | Priority queue | `help:queue:priority` |
| **List** | Ticket audit logs | `help:ticket:T001:log` |

### Key Naming Convention

```
help:user:{user_id}           # User information
help:agent:{agent_id}         # Agent information
help:ticket:{ticket_id}       # Ticket information
help:idx:user_email:{email}   # Email to user ID mapping
help:queue:priority           # Priority queue
help:agent:{agent_id}:skills  # Agent skills
help:agent:{agent_id}:open_tickets  # Agent's open tickets
help:ticket:{ticket_id}:log   # Ticket audit log
```

## 🖥️ Redis Insight (Optional)

Redis Insight is a powerful GUI tool for Redis that provides a visual interface to explore your data, monitor performance, and run commands.

### Using Redis Insight with Docker

1. **Start Redis Insight Container:**
```bash
docker run -d --name redisinsight -p 5540:5540 redis/redisinsight
```

2. **Access Redis Insight:**
   - Open your browser and go to: `http://localhost:5540`
   - You'll see the Redis Insight welcome screen

3. **Connect to Your Redis Database:**
   - Click "Add Redis Database"
   - Enter your connection details:
     - **Host**: Your Redis host (from .env file)
     - **Port**: Your Redis port (from .env file)
     - **Username**: Your Redis username (usually "default")
     - **Password**: Your Redis password
   - Click "Add Redis Database"

4. **Explore Your Data:**
   - Browse keys with the `help:*` pattern
   - View data structures (Hash, Set, Sorted Set, List)
   - Run Redis commands in the CLI
   - Monitor real-time operations

### Useful Redis Insight Features

- **Key Browser**: Navigate through your helpdesk data
- **Data Visualization**: See your Hash, Set, and Sorted Set structures
- **Command Line**: Execute Redis commands directly
- **Memory Analysis**: Monitor memory usage
- **Performance Metrics**: Track operations and latency

### Stopping Redis Insight

```bash
# Stop the container
docker stop redisinsight

# Remove the container
docker rm redisinsight

# Or stop and remove in one command
docker rm -f redisinsight
```

### Alternative: Redis Insight Desktop App

You can also download the desktop version from [Redis Insight Downloads](https://redis.com/redis-enterprise/redis-insight/).

## 🔍 Key Operations

### User Management
```python
# Create user
r.hset("help:user:U001", mapping={
    "name": "Alice Smith",
    "email": "alice@example.com",
    "phone": "111-1111",
    "joined_at": "2025-10-05T08:00Z"
})

# Email index for fast lookup
r.set("help:idx:user_email:alice@example.com", "U001")
```

### Ticket Priority Queue
```python
# Add ticket to priority queue
r.zadd("help:queue:priority", {"help:ticket:T001": 20})

# Get top 3 highest priority tickets
top_tickets = r.zrevrange("help:queue:priority", 0, 2, withscores=True)
```

### Agent Assignment
```python
# Assign ticket to agent
r.hset("help:ticket:T001", "assigned_agent", "A001")
r.sadd("help:agent:A001:open_tickets", "help:ticket:T001")
r.hincrby("help:agent:A001", "load", 1)
```

## 📸 Screenshots

The `Screenshots/` directory contains 11 images documenting:
- Connection establishment
- Part B execution results
- Part C CRUD operations
- Query results and system verification

## 🧪 Testing

### Verify Installation
```bash
python -c "import redis; print('Redis module installed successfully')"
```

### Test Connection
```bash
python config.py
```

### Run Full Demo
```bash
python part-c-crud-ops.py
```

## 🔧 Troubleshooting

### Connection Issues
- Verify your `.env` file has correct credentials
- Check Redis Cloud database is active
- Ensure firewall allows Redis port access

### Import Errors
```bash
# Reinstall dependencies
uv sync --reinstall
# or
pip install --upgrade redis python-dotenv
```

### SSL Issues
If you encounter SSL certificate issues, the code is configured to handle this automatically with:
```python
ssl=False  # Set to True for production with proper certificates
```

### Visual Data Exploration
If you want to visually explore your Redis data:
1. Start Redis Insight: `docker run -d --name redisinsight -p 5540:5540 redis/redisinsight`
2. Open `http://localhost:5540` in your browser
3. Connect using your Redis credentials from `.env`
4. Browse keys with pattern `help:*` to see all helpdesk data

## 📚 Learning Objectives

This project demonstrates:
- Redis data structure selection and usage
- Real-world application design patterns
- CRUD operations with Redis
- Data modeling for scalable systems
- Priority queue implementation
- Audit logging and data integrity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of a Big Data Analytics course lab assignment.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the screenshots for expected output
3. Verify your Redis connection and credentials
4. Ensure all dependencies are installed correctly

---

**Happy Coding! 🎉**

*This helpdesk system showcases the power of Redis for building fast, scalable applications with complex data relationships.*
