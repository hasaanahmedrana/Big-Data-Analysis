import boto3
# Before running this script, ensure that you have configured your AWS credentials by running 'aws configure'
# Also, make sure you have the necessary permissions to modify S3 bucket settings or make by command line: aws s3 mb s3://hasaan-lms-lab2 --region ap-south-1
# Enable versioning on an S3 bucket


s3 = boto3.client('s3', region_name='ap-south-1')
bucket = "hasaan-lms-lab2"

s3.put_bucket_versioning(
    Bucket=bucket,
    VersioningConfiguration={'Status': 'Enabled'}
)
print("✅ Versioning enabled")

# Verify the versioning status
resp = s3.get_bucket_versioning(Bucket=bucket)
print(resp)


