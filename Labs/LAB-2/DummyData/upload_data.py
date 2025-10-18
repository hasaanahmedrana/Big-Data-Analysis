import boto3, os

# your bucket name
bucket = "hasaan-lms-lab2"
region = "ap-south-1"

s3 = boto3.client("s3", region_name=region)

# base path where dummy files are stored
base_path = "C:\\Users\\PMLS\\Desktop\\Sem-7\\BigDataAnalytics\\Labs\\LAB-2\\DummyData"

# helper function
def upload(local_file, key, content_type=None):
    extra = {}
    if content_type:
        extra["ContentType"] = content_type
    if extra:
        s3.upload_file(local_file, bucket, key, ExtraArgs=extra)
    else:
        s3.upload_file(local_file, bucket, key)
    print("✅ Uploaded:", key)

upload(os.path.join(base_path, "slides_CS101_week1.pdf"), "courses/CS101/weeks/week01/slides.pdf", "application/pdf")
upload(os.path.join(base_path, "slides_CS101_week2.pdf"), "courses/CS101/weeks/week02/slides.pdf", "application/pdf")
upload(os.path.join(base_path, "marks_CS101.csv"), "datasets/CS101/marks.csv", "text/csv")
upload(os.path.join(base_path, "announcements-2025-09-25.txt"), "announcements/2025-09-25.txt", "text/plain")
upload(os.path.join(base_path, "sub_CS101_2023001_assignment1.pdf"), "submissions/CS101/assignment1/2023001/assignment.pdf", "application/pdf")
upload(os.path.join(base_path, "sub_CS101_2023002_assignment1.pdf"), "submissions/CS101/assignment1/2023002/assignment.pdf", "application/pdf")



upload(os.path.join(base_path, "slides_CS202_week1.pdf"), "courses/CS202/weeks/week01/slides.pdf", "application/pdf")
upload(os.path.join(base_path, "slides_CS202_week2.pdf"), "courses/CS202/weeks/week02/slides.pdf", "application/pdf")
upload(os.path.join(base_path, "marks_CS202.csv"), "datasets/CS202/marks.csv", "text/csv")
upload(os.path.join(base_path, "announcements-2025-09-26.txt"), "announcements/2025-09-26.txt", "text/plain")
upload(os.path.join(base_path, "sub_CS202_2023010_assignment1.pdf"), "submissions/CS202/assignment1/2023010/assignment.pdf", "application/pdf")
upload(os.path.join(base_path, "sub_CS202_2023011_assignment1.pdf"), "submissions/CS202/assignment1/2023011/assignment.pdf", "application/pdf")
