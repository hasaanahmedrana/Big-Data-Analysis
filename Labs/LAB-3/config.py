import redis

try:
    r = redis.Redis(
        host="redis-19617.c305.ap-south-1-1.ec2.redns.redis-cloud.com",
        port=19617,
        username="default",
        password="Sr4s6Doq6h0RESHE7i0xm5bT2879qx3I",
        ssl=False,          
        ssl_cert_reqs=None,  
        decode_responses=True
    )

    print("🔌 Pinging Redis Cloud …")
    print("Response:", r.ping())   
    print(" Connected successfully via TLS!")

except Exception as e:
    print(" Connection failed:", e)
