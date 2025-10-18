import boto3
from botocore.exceptions import ClientError

bucket = "hasaan-lms-lab2"
region = "ap-south-1"
s3 = boto3.client("s3", region_name=region)

def delete_object(key):
    s3.delete_object(Bucket=bucket, Key=key)
    print(f"Deleted: {key}")

def verify_deleted(key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        print(f"Object still exists: {key}")

    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"Verified deleted: {key}")
        else:
            print(f"Unexpected error for {key}: {e}")
            

# Step 1: Delete a dataset file
delete_object("datasets/CS101/marks.csv")
verify_deleted("datasets/CS101/marks.csv")

# Step 2: Delete a student submission
delete_object("submissions/CS101/assignment1/2023002/assignment.pdf")
verify_deleted("submissions/CS101/assignment1/2023002/assignment.pdf")
