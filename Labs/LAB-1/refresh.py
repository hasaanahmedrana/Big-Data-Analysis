import psycopg2

def refresh():
    conn = psycopg2.connect(
        host="localhost",
        database="university_db",
        user="postgres",
        password="12345"
    )
    cursor = conn.cursor()
    cursor.execute("""
        TRUNCATE TABLE Enrollments, Students, Courses, Teachers, Departments 
        RESTART IDENTITY CASCADE;
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("🗑️ All tables truncated & IDs reset!")

