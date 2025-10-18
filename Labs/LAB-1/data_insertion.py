"""
Data Generation and Insertion Script for University Database
------------------------------------------------------------
This script populates the University Database created in Part 1.

Steps:
1. Insert fixed Departments.
2. Generate random Teachers (100), assigned to Departments.
3. Generate random Courses (200), each assigned to a Teacher.
4. Generate Students (scalable: 1k, 10k, 100k, 1M).
5. Generate Enrollments: each student is enrolled in 5–10 random courses.

Libraries used:
- Faker: for generating realistic fake data (names, emails, etc.)
- psycopg2: for PostgreSQL database connection and queries
- random: to pick random department/course assignments
- tqdm: for progress bars during large insertions
"""

from faker import Faker
import psycopg2
from random import randint, sample
from tqdm import tqdm


def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="university_db",
        user="postgres",
        password="12345")
    return conn, conn.cursor()

def insert_departments(cursor, fake):
    """
    Inserts 10 fixed departments into the Departments table.

    Args:
        cursor: psycopg2 cursor object
        fake: Faker instance for generating building names
    """
    departments = [
        "Computer Science", "Data Science", "Mathematics", "Information Technology",
        "Artificial Intelligence", "Cyber Security", "Software Engineering", "Data Analytics",
        "Data Visualization", "Engineering",
    ]
    for dep in departments:
        cursor.execute(
            """
            INSERT INTO Departments (department_name, building)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
            """,
            (dep, fake.word().capitalize() + " Building")
        )


def insert_teachers(cursor, fake):
    """
    Inserts 100 teachers into the Teachers table.
    Each teacher belongs to a random department.

    Args:
        cursor: psycopg2 cursor object
        fake: Faker instance

    Returns:
        teacher_ids: list of inserted teacher_id values
    """
    teacher_ids = []
    for _ in range(100):
        cursor.execute(
            """
            INSERT INTO Teachers (first_name, last_name, email, department_id, hire_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING teacher_id;
            """,
            (
                fake.first_name(), fake.last_name(),
                fake.unique.email(),
                randint(1, 10),  # department_id between 1–10
                fake.date_between(start_date="-10y", end_date="today")
            )
        )
        teacher_ids.append(cursor.fetchone()[0])
    return teacher_ids


def insert_courses(cursor, fake, teacher_ids):
    """
    Inserts 200 courses into the Courses table.
    Each course is assigned to a random teacher.

    Args:
        cursor: psycopg2 cursor object
        fake: Faker instance
        teacher_ids: list of teacher_id values

    Returns:
        course_ids: list of inserted course_id values
    """
    course_ids = []
    for _ in range(200):
        cursor.execute(
            """
            INSERT INTO Courses (course_name, credits, teacher_id)
            VALUES (%s, %s, %s)
            RETURNING course_id;
            """,
            (
                fake.catch_phrase(),  # generates course-like names
                randint(2, 5),        # credits between 2–5
                sample(teacher_ids, 1)[0]  # pick a random teacher
            )
        )
        course_ids.append(cursor.fetchone()[0])
    return course_ids


def insert_students(cursor, fake, scale):
    """
    Inserts students into the Students table.

    Args:
        cursor: psycopg2 cursor object
        fake: Faker instance
        scale: number of students (e.g., 1000, 10000, 100000, 1000000)

    Returns:
        student_ids: list of inserted student_id values
    """
    student_ids = []
    for _ in tqdm(range(scale), desc=f"Inserting {scale} Students"):
        cursor.execute(
            """
            INSERT INTO Students (first_name, last_name, email, enrollment_date, date_of_birth)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING student_id;
            """,
            (
                fake.first_name(), fake.last_name(),
                fake.unique.email(),
                fake.date_between(start_date="-4y", end_date="today"),
                fake.date_of_birth(minimum_age=18, maximum_age=30)
            )
        )
        student_ids.append(cursor.fetchone()[0])
    return student_ids


def insert_enrollments(cursor, student_ids, course_ids):
    """
    Inserts enrollments into the Enrollments table.
    Each student is enrolled in 5–10 random courses.

    Args:
        cursor: psycopg2 cursor object
        student_ids: list of student_id values
        course_ids: list of course_id values
    """
    semesters = ["Fall 2023", "Spring 2024", "Fall 2024", "Spring 2025"]

    for student in tqdm(student_ids, desc="Inserting Enrollments"):
        enrolled_courses = sample(course_ids, randint(5, 10))
        for c in enrolled_courses:
            cursor.execute(
                """
                INSERT INTO Enrollments (student_id, course_id, semester, grade)
                VALUES (%s, %s, %s, %s);
                """,
                (
                    student,
                    c,
                    sample(semesters, 1)[0],
                    randint(50, 100)  # grade between 50–100
                )
            )


def main(scale=1000):
    conn, cursor = connect_db()
    fake = Faker()

    print("Inserting Departments...")
    insert_departments(cursor, fake)

    print("Inserting Teachers...")
    teacher_ids = insert_teachers(cursor, fake)

    print("Inserting Courses...")
    course_ids = insert_courses(cursor, fake, teacher_ids)

    print(f"Inserting {scale} Students...")
    student_ids = insert_students(cursor, fake, scale)

    print("Inserting Enrollments...")
    insert_enrollments(cursor, student_ids, course_ids)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Data insertion complete!")

def verify_insertion():
    conn, cursor = connect_db()

    tables = ["Departments", "Teachers", "Courses", "Students", "Enrollments"]
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]
        print(f"{table}: {count} rows")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main(scale=1000)
    verify_insertion()

