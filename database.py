import sqlite3
import os

# Initialize SQLite database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Students (
    enrollment_number INTEGER PRIMARY KEY,
    name TEXT,
    branch TEXT,
    starting_year INTEGER,
    total_attendance INTEGER,
    batch TEXT,
    year INTEGER,
    last_attendance_time TEXT,
    image BLOB
)
"""
)

print("Starting to add the data into database ...")


# Function to convert image to binary
def convert_to_binary(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found -> {file_path}")
        return None
    with open(file_path, "rb") as file:
        return file.read()


# Student data
data = {
    23002171310132: {
        "name": "Naresh Prajapati",
        "branch": "CST",
        "starting_year": 2023,
        "total_attendance": 10,
        "batch": "D3",
        "year": 2,
        "last_attendance_time": "2025-02-14 08:30:00",
        "image_path": "23002171310132.jpg",
    },
    23002171310167: {
        "name": "Vansh Somani",
        "branch": "CST",
        "starting_year": 2023,
        "total_attendance": 9,
        "batch": "D3",
        "year": 2,
        "last_attendance_time": "2025-02-11 08:45:34",
        "image_path": "23002171310167.jpg",
    },
    23002171310178: {
        "name": "Vedant Hingu",
        "branch": "CSE",
        "starting_year": 2023,
        "total_attendance": 8,
        "batch": "D3",
        "year": 2,
        "last_attendance_time": "2025-02-13 08:30:34",
        "image_path": "23002171310178.jpg",
    },
}

# Insert data into the database
for key, value in data.items():
    image_binary = convert_to_binary(value["image_path"])
    if image_binary is None:
        continue
    cursor.execute(
        """
    INSERT OR REPLACE INTO Students (enrollment_number, name, branch, starting_year, total_attendance, batch, year, last_attendance_time, image)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            key,
            value["name"],
            value["branch"],
            value["starting_year"],
            value["total_attendance"],
            value["batch"],
            value["year"],
            value["last_attendance_time"],
            image_binary,
        ),
    )

conn.commit()
conn.close()

print("Data added to SQLite database successfully.")
