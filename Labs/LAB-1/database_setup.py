import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="12345" )
conn.autocommit = True
cursor = conn.cursor()
cursor.execute("CREATE DATABASE university_db;")


print("Database 'university_db' created successfully!")

cursor.close()
conn.close()
