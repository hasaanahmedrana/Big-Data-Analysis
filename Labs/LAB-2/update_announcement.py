import boto3

bucket = "hasaan-lms-lab2"
region = "ap-south-1"
s3 = boto3.client("s3", region_name=region)

# 
key = "announcements/2025-09-25.txt"

# New content (overwrite old announcement)
new_text = b"CS101: Assignment 1 deadline extended to Oct 5,2025 11:59 PM.\nPlease check your emails for details.\n" 


s3.put_object(
    Bucket=bucket,
    Key=key,
    Body=new_text,
    ContentType="text/plain"
)
print(f"Updated announcement at {key}")

# Step 2: Fetch the latest content to confirm
resp = s3.get_object(Bucket=bucket, Key=key)
content = resp["Body"].read().decode("utf-8")
print("Current announcement content:")
print(content)
