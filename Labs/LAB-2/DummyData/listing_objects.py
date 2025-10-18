import boto3

bucket = "hasaan-lms-lab2"
region = "ap-south-1"

s3 = boto3.client("s3", region_name=region)

def list_objects(prefix):
    print(f" Listing objects under: {prefix}\n")
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if "Contents" in resp:
        for obj in resp["Contents"]:
            print(" -", obj["Key"], f"({obj['Size']} bytes)")
    else:
        print("No objects found under this prefix.")

list_objects("courses/CS202/weeks/week02/")
