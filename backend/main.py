from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

db_config = {
    "host": "mysql",
    "user": "root",
    "password": "rootpassword",
    "database": "studentsdb"
}

class Student(BaseModel):
    name: str
    email: str
    course: str
    year: int

@app.get("/students")
def get_students():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    result = cursor.fetchall()
    conn.close()
    return result

@app.post("/students")
def add_student(student: Student):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, email, course, year) VALUES (%s, %s, %s, %s)",
                   (student.name, student.email, student.course, student.year))
    conn.commit()
    conn.close()
    return {"message": "Student added successfully"}
