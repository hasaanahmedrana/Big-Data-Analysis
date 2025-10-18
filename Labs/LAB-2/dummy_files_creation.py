from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import csv
import os
import traceback

# base directory for lab files
BASE_DIR = "DummyData"

try:
    os.makedirs(BASE_DIR, exist_ok=True)
    print(f"✓ Directory created/verified: {os.path.abspath(BASE_DIR)}")
except Exception as e:
    print(f"❌ Error creating directory: {e}")
    traceback.print_exc()
    exit(1)

def fullpath(rel):
    """Return full path inside BASE_DIR for a relative filename."""
    return os.path.join(BASE_DIR, rel)

# helper function to create PDFs
def make_pdf(rel_path, pages=2, title="Document"):
    try:
        path = fullpath(rel_path)
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        c = canvas.Canvas(path, pagesize=letter)
        for p in range(pages):
            c.drawString(100, 750, f"{title} - Page {p+1}")
            c.drawString(100, 730, "Dummy content for S3 lab testing...")
            c.showPage()
        c.save()
        print(f"✓ Created: {path}")
    except Exception as e:
        print(f"❌ Error creating {rel_path}: {e}")
        traceback.print_exc()

# ============ CS101 FILES ============
print("\n--- Creating CS101 files ---")
make_pdf("slides_CS101_week1.pdf", title="CS101 Lecture Slides")
make_pdf("slides_CS101_week2.pdf", title="CS101 Lecture Slides")

try:
    rows101 = [
        ["student_id", "marks", "attendance"],
        ["2023001", 85, 90],
        ["2023002", 78, 100]
    ]
    with open(fullpath("marks_CS101.csv"), "w", newline="", encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerows(rows101)
    print(f"✓ Created: {fullpath('marks_CS101.csv')}")
except Exception as e:
    print(f"❌ Error creating marks_CS101.csv: {e}")
    traceback.print_exc()

try:
    with open(fullpath("announcements-2025-09-25.txt"), "w", encoding="utf8") as f:
        f.write("📢 CS101: Assignment 1 deadline is Sept 30\n")
    print(f"✓ Created: {fullpath('announcements-2025-09-25.txt')}")
except Exception as e:
    print(f"❌ Error creating announcements: {e}")
    traceback.print_exc()

make_pdf("sub_CS101_2023001_assignment1.pdf", title="CS101 Assignment 1 Submission - 2023001")
make_pdf("sub_CS101_2023002_assignment1.pdf", title="CS101 Assignment 1 Submission - 2023002")

# ============ CS202 FILES ============
print("\n--- Creating CS202 files ---")
make_pdf("slides_CS202_week1.pdf", title="CS202 Lecture Slides")
make_pdf("slides_CS202_week2.pdf", title="CS202 Lecture Slides")

try:
    rows202 = [
        ["student_id", "marks", "attendance"],
        ["2023010", 92, 85],
        ["2023011", 74, 88]
    ]
    with open(fullpath("marks_CS202.csv"), "w", newline="", encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerows(rows202)
    print(f"✓ Created: {fullpath('marks_CS202.csv')}")
except Exception as e:
    print(f"❌ Error creating marks_CS202.csv: {e}")
    traceback.print_exc()

try:
    with open(fullpath("announcements-2025-09-26.txt"), "w", encoding="utf8") as f:
        f.write("📢 CS202: Midterm schedule will be announced soon\n")
    print(f"✓ Created: {fullpath('announcements-2025-09-26.txt')}")
except Exception as e:
    print(f"❌ Error creating announcements: {e}")
    traceback.print_exc()

make_pdf("sub_CS202_2023010_assignment1.pdf", title="CS202 Assignment 1 Submission - 2023010")
make_pdf("sub_CS202_2023011_assignment1.pdf", title="CS202 Assignment 1 Submission - 2023011")

print(f"\n✅ Script completed! Check folder: {os.path.abspath(BASE_DIR)}")
print(f"Files created: {len([f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))])}")