import psycopg2

def create_indexes():
    conn = psycopg2.connect(
        host="localhost",
        database="university_db",
        user="postgres",
        password="12345"
    )
    cursor = conn.cursor()

    indexes = [
        # Q1
        "CREATE INDEX IF NOT EXISTS idx_students_enrollment_date ON Students(enrollment_date);",

        # Q2
        "CREATE INDEX IF NOT EXISTS idx_enrollments_student ON Enrollments(student_id);",
        "CREATE INDEX IF NOT EXISTS idx_enrollments_course ON Enrollments(course_id);",
        "CREATE INDEX IF NOT EXISTS idx_courses_teacher ON Courses(teacher_id);",

        # Q3
        "CREATE INDEX IF NOT EXISTS idx_courses_name ON Courses(course_name text_pattern_ops);",

        # Q4
        "CREATE INDEX IF NOT EXISTS idx_teachers_department ON Teachers(department_id);",

        # Q5
        "CREATE INDEX IF NOT EXISTS idx_enrollments_semester ON Enrollments(semester);"
    ]

    for idx in indexes:
        print(f"Creating: {idx}")
        cursor.execute(idx)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ All indexes created successfully!")

if __name__ == "__main__":
    create_indexes()
