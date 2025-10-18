import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="university_db",
    user="postgres",
    password="12345"
)
cursor = conn.cursor()

# Departments
cursor.execute('''
CREATE TABLE IF NOT EXISTS Departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100),
    building VARCHAR(50)
);
''')

# Teachers
cursor.execute("""
CREATE TABLE IF NOT EXISTS Teachers (
    teacher_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    department_id INT REFERENCES Departments(department_id),
    hire_date DATE
);
""")

# Courses
cursor.execute("""
CREATE TABLE IF NOT EXISTS Courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100),
    credits INT,
    teacher_id INT REFERENCES Teachers(teacher_id)
);
""")

# Students
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    enrollment_date DATE,
    date_of_birth DATE
);
""")

# Enrollments
cursor.execute("""
CREATE TABLE IF NOT EXISTS Enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES Students(student_id),
    course_id INT REFERENCES Courses(course_id),
    semester VARCHAR(20),
    grade INT
);
""")

conn.commit()
cursor.close()
conn.close()
print("All tables created successfully (if not already existing)!")
