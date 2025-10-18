import psycopg2
import time
import statistics
import csv
from pathlib import Path
from data_insertion import main as insert_data, verify_insertion
from refresh import refresh


def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="university_db",
        user="postgres",
        password="12345"
    )
    return conn, conn.cursor()


QUERIES = {
    "Q1_Simple_Filter": """
        SELECT * FROM Students
        WHERE EXTRACT(YEAR FROM enrollment_date) = 2023;
    """,

    "Q2_Simple_Join_Filter": """
        SELECT DISTINCT s.email
        FROM Students s
        JOIN Enrollments e ON s.student_id = e.student_id
        JOIN Courses c ON e.course_id = c.course_id
        WHERE c.teacher_id = 50;
    """,

    "Q3_MultiJoin_TextSearch": """
        SELECT DISTINCT t.first_name || ' ' || t.last_name AS teacher_name
        FROM Teachers t
        JOIN Courses c ON t.teacher_id = c.teacher_id
        WHERE c.course_name ILIKE '%Advanced%';
    """,

    "Q4_Join_Aggregation": """
        SELECT d.department_name, COUNT(c.course_id) AS course_count
        FROM Departments d
        JOIN Teachers t ON d.department_id = t.department_id
        JOIN Courses c ON t.teacher_id = c.teacher_id
        GROUP BY d.department_name;
    """,

    "Q5_Complex_Top10": """
        SELECT s.first_name || ' ' || s.last_name AS student_name,
               AVG(e.grade) AS avg_grade
        FROM Students s
        JOIN Enrollments e ON s.student_id = e.student_id
        WHERE e.semester = 'Spring 2025'
        GROUP BY s.student_id, s.first_name, s.last_name
        ORDER BY avg_grade DESC
        LIMIT 10;
    """
}


def benchmark_query(cursor, query, runs=3):
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        cursor.execute(query)
        cursor.fetchall()
        end = time.perf_counter()
        times.append((end - start) * 1000)  # ms
    return statistics.mean(times)


def run_benchmarks(runs=3):
    conn, cursor = connect_db()
    results = {}

    for qname, qtext in QUERIES.items():
        avg_time = benchmark_query(cursor, qtext, runs)
        results[qname] = round(avg_time, 2)
        print(f"{qname}: {avg_time:.2f} ms (avg over {runs} runs)")

    cursor.close()
    conn.close()
    return results


def save_results_to_csv(results, scale, filename="query_results.csv"):
    file_exists = Path(filename).is_file()

    with open(filename, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            header = ["Scale"] + list(results.keys())
            writer.writerow(header)
        row = [scale] + list(results.values())
        writer.writerow(row)

if __name__ == "__main__":
    all_results = []
    scales = [1000, 10000, 100000, 1000000]

    # for scale in scales:
    #     print(f"\n=== Running experiment for {scale} students ===")
    #     refresh()
    #     print(f"Inserting {scale} students...")
    #     insert_data(scale=scale)
    #     print("Verifying insertion...")
    #     verify_insertion()
    #     print("Running benchmarks...")
    #     results = run_benchmarks(runs=3)
    #     row = {"Scale": scale}
    #     row.update(results)
    #     all_results.append(row)

    import pandas as pd

    df = pd.DataFrame(all_results)
    print("\nFinal Results:")
    print(df)
    df.to_csv("query_results.csv", index=False)
    df.to_excel("query_results.xlsx", index=False)
    import pandas as pd

    # Create the DataFrame with Scale as a regular column
    data = {
        'Scale': [1000, 10000, 100000, 1000000],
        'Q1_simple_Filter': [1.19, 6.40, 69.71, 756.10],
        'Q2_simple_Join_Filter': [2.02, 1.69, 191.07, 4634.75],
        'Q3_MultiJoin_TextSearch': [1.27, 1.31, 24.18, 65.14],
        'Q4_Join_Aggregation': [0.71, 1.24, 3.20, 6.96],
        'Q5_Complex_Top10': [2.70, 22.34, 229.22, 3957.74]
    }

    df = pd.DataFrame(data)

    # Save to Excel file
    excel_filename = 'query_performance_results.xlsx'
    df.to_excel(excel_filename, sheet_name='Performance Results', index=False)

    print(f"DataFrame created successfully!")
    print(df)
    print(f"\nData saved to '{excel_filename}'")