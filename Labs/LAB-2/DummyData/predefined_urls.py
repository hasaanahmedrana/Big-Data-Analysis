import subprocess
import requests
import os

bucket = "hasaan-lms-lab2"
key = "submissions/CS101/assignment1/2023001/assignment.pdf"
region = "ap-south-1"
local_filename = "download_using_url.pdf"

# 1. Generate presigned URL using AWS CLI
cmd = [
    "aws", "s3", "presign",
    f"s3://{bucket}/{key}",
    "--region", region,
    "--expires-in", "3600"
]

print("------------------------------------------------------------")
print(f"Bucket region: {region}")

try:
    presigned_url = subprocess.check_output(cmd, text=True).strip()
    print("Presigned URL:", presigned_url)
except subprocess.CalledProcessError as e:
    print("❌ Failed to generate presigned URL:", e)
    exit(1)

# 2. Download the file
resp = requests.get(presigned_url)
print("Status:", resp.status_code)

if resp.ok:
    with open(local_filename, "wb") as f:
        f.write(resp.content)
    print(f"✅ Downloaded and saved as {local_filename}")
    print(f"📂 Full path: {os.path.abspath(local_filename)}")
else:
    print("❌ Failed, response:", resp.text)
