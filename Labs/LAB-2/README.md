# Big Data Analytics - Lab 2: AWS S3 Learning Management System

## 📋 Project Overview

This project demonstrates comprehensive AWS S3 operations for a Learning Management System (LMS) using Python and Boto3. The lab covers essential S3 functionalities including file uploads, downloads, versioning, object listing, and presigned URL generation.

## 🎯 Learning Objectives

- **S3 Bucket Management**: Create and configure S3 buckets with versioning
- **File Operations**: Upload, download, delete, and list objects in S3
- **Content Management**: Organize educational content with proper folder structure
- **Version Control**: Implement S3 versioning for file management
- **Security**: Generate presigned URLs for secure file access
- **Data Organization**: Structure data for courses, submissions, and announcements

## 🏗️ Project Structure

```
LAB-2/
├── DummyData/                          # Generated test data
│   ├── announcements-2025-09-25.txt   # Course announcements
│   ├── announcements-2025-09-26.txt
│   ├── marks_CS101.csv                # Student marks data
│   ├── marks_CS202.csv
│   ├── slides_CS101_week1.pdf         # Lecture slides
│   ├── slides_CS101_week2.pdf
│   ├── slides_CS202_week1.pdf
│   ├── slides_CS202_week2.pdf
│   ├── sub_CS101_2023001_assignment1.pdf  # Student submissions
│   ├── sub_CS101_2023002_assignment1.pdf
│   ├── sub_CS202_2023010_assignment1.pdf
│   ├── sub_CS202_2023011_assignment1.pdf
│   ├── listing_objects.py             # Object listing utilities
│   ├── predefined_urls.py             # Presigned URL generation
│   └── upload_data.py                 # Data upload script
├── Screenshots/                        # Lab demonstration screenshots
├── dummy_files_creation.py            # Generate test data
├── enable-versioning.py               # Enable S3 bucket versioning
├── upload_data.py                     # Upload files to S3
├── delete_and_verify.py               # Delete objects and verify
├── reupload.py                        # Re-upload with versioning
├── update_announcement.py             # Update announcement content
├── main.py                           # Main entry point
├── pyproject.toml                     # Project dependencies
└── Report.docx                        # Lab report
```

## 🚀 Prerequisites

- **Python 3.10+**
- **AWS CLI** configured with appropriate credentials
- **AWS Account** with S3 permissions
- **Required Python packages** (see `pyproject.toml`)

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd LAB-2
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   # or
   uv sync  # if using uv package manager
   ```

3. **Configure AWS credentials**:
   ```bash
   aws configure
   ```
   Enter your AWS Access Key ID, Secret Access Key, and preferred region.

4. **Create S3 bucket** (if not exists):
   ```bash
   aws s3 mb s3://hasaan-lms-lab2 --region ap-south-1
   ```

## 🛠️ Usage

### 1. Generate Test Data

Create dummy files for testing:

```bash
python dummy_files_creation.py
```

This script generates:
- PDF lecture slides for CS101 and CS202 courses
- CSV files with student marks and attendance
- Text files with course announcements
- PDF files with student assignment submissions

### 2. Enable S3 Versioning

Enable versioning on your S3 bucket:

```bash
python enable-versioning.py
```

### 3. Upload Data to S3

Upload all generated files to S3 with organized folder structure:

```bash
python DummyData/upload_data.py
```

**S3 Folder Structure**:
```
s3://hasaan-lms-lab2/
├── courses/
│   ├── CS101/weeks/week01/slides.pdf
│   ├── CS101/weeks/week02/slides.pdf
│   ├── CS202/weeks/week01/slides.pdf
│   └── CS202/weeks/week02/slides.pdf
├── datasets/
│   ├── CS101/marks.csv
│   └── CS202/marks.csv
├── announcements/
│   ├── 2025-09-25.txt
│   └── 2025-09-26.txt
└── submissions/
    ├── CS101/assignment1/2023001/assignment.pdf
    ├── CS101/assignment1/2023002/assignment.pdf
    ├── CS202/assignment1/2023010/assignment.pdf
    └── CS202/assignment1/2023011/assignment.pdf
```

### 4. List Objects

List objects in specific S3 prefixes:

```bash
python DummyData/listing_objects.py
```

### 5. Generate Presigned URLs

Create presigned URLs for secure file downloads:

```bash
python DummyData/predefined_urls.py
```

### 6. Update Content

Update announcement content:

```bash
python update_announcement.py
```

### 7. Re-upload with Versioning

Demonstrate S3 versioning by re-uploading files:

```bash
python reupload.py
```

### 8. Delete and Verify

Delete objects and verify deletion:

```bash
python delete_and_verify.py
```

## 🔧 Key Features

### S3 Operations Demonstrated

1. **Bucket Management**
   - Create S3 buckets
   - Enable versioning
   - Configure bucket settings

2. **File Operations**
   - Upload files with proper content types
   - Download files using presigned URLs
   - Delete objects with verification
   - List objects with pagination

3. **Version Control**
   - Enable bucket versioning
   - Upload new versions of files
   - List all versions of objects
   - Track version history

4. **Content Management**
   - Organize files in logical folder structure
   - Set appropriate content types (PDF, CSV, TXT)
   - Manage course materials, submissions, and announcements

5. **Security**
   - Generate presigned URLs for temporary access
   - Configure proper permissions
   - Secure file downloads

## 📊 Data Structure

### Course Materials
- **Lecture Slides**: PDF files organized by course and week
- **Student Marks**: CSV files with student performance data
- **Announcements**: Text files with course updates

### Student Submissions
- **Assignment Files**: PDF submissions organized by course, assignment, and student ID
- **Version Control**: Track submission history and updates

## 🎓 Educational Context

This lab simulates a real-world Learning Management System where:

- **Instructors** upload course materials and announcements
- **Students** submit assignments and access course content
- **Administrators** manage data organization and version control
- **System** provides secure access through presigned URLs

## 📸 Screenshots

The `Screenshots/` directory contains visual demonstrations of:
1. S3 bucket creation and configuration
2. File upload operations
3. Versioning implementation
4. Object listing and management
5. Presigned URL generation
6. Content organization
7. Deletion and verification
8. Lab completion verification

## 🔍 Troubleshooting

### Common Issues

1. **AWS Credentials Not Configured**
   ```bash
   aws configure
   ```

2. **Bucket Already Exists**
   - Use a different bucket name or delete existing bucket

3. **Permission Denied**
   - Ensure your AWS user has S3 permissions
   - Check bucket policy and IAM roles

4. **File Not Found**
   - Run `dummy_files_creation.py` first
   - Check file paths in upload scripts

## 📝 Dependencies

- `boto3>=1.40.45` - AWS SDK for Python
- `botocore>=1.40.45` - Low-level AWS service access
- `awscli>=1.42.45` - AWS Command Line Interface
- `fpdf>=1.7.2` - PDF generation
- `reportlab>=4.4.4` - Advanced PDF creation
- `requests>=2.32.5` - HTTP library for downloads

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of Big Data Analytics coursework and is intended for educational purposes.

## 👨‍💻 Author

**Hasaan** - Big Data Analytics Lab 2

---

*This lab demonstrates practical AWS S3 operations for managing educational content in a scalable cloud environment.*
