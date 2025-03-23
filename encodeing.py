import cv2
import face_recognition
import pickle
import os
import sqlite3

# Initialize SQLite database
conn = sqlite3.connect("student_data.db")
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Students (
    id TEXT PRIMARY KEY,
    name TEXT,
    major TEXT,
    starting_year INTEGER,
    total_attendance INTEGER,
    standing TEXT,
    year INTEGER,
    last_attendance_time TEXT
)
"""
)

# Importing student images
folderPath = "stundentFaces"
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

with open("EncodeFile.p", "wb") as file:
    pickle.dump(encodeListKnownWithIds, file)
print("File Saved")
