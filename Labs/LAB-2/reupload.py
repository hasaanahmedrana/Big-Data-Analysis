import boto3

bucket = "hasaan-lms-lab2"
region = "ap-south-1"
s3 = boto3.client("s3", region_name=region)
key = "courses/CS101/weeks/week01/slides.pdf"


s3.upload_file("DummyData/slides_CS101_week1.pdf", bucket, key, ExtraArgs={"ContentType": "application/pdf"})
print(f" Re-uploaded corrected slide to {key}")

# Step 2: List all versions for this object
print(" Listing versions for:", key)
resp = s3.list_object_versions(Bucket=bucket, Prefix=key)

if "Versions" in resp:
    for v in resp["Versions"]:
        print(f"- VersionId: {v['VersionId']} | IsLatest: {v['IsLatest']} | Size: {v['Size']} bytes | LastModified: {v['LastModified']}")
else:
    print(" No versions found.")
