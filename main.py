import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import sqlite3
from datetime import datetime
import pandas as pd

conn = sqlite3.connect("students.db")
cursor = conn.cursor()


# Directory to save fetched images
output_dir = "retrievedImages"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("final.png")

# Importing the modes images into a list.
folderModePath = "Modes"
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Load the encoding file.
print("Loading Encode File ...")
with open("EncodeFile.p", "rb") as file:
    encodeListKnown, studentIds = pickle.load(file)
print("Encode File Loaded ...")


frame_counter = 0
modeType = 0
counter = 0
id = -1


# Function to mark attendance
def mark_attendance(student_name):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    try:
        df = pd.read_excel(file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "Date", "Time"])
    new_record_df = pd.DataFrame(
        {"Name": [student_name], "Date": [current_date], "Time": [current_time]}
    )
    df = pd.concat([df, new_record_df], ignore_index=True)
    df.to_excel(file, index=False)


while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162 : 162 + 480, 55 : 55 + 640] = img
    imgBackground[48 : 48 + 633, 812 : 812 + 414] = imgModeList[modeType]

    if faceCurFrame:

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:

                # print("Known Face Detected")
                # print(studentIds[matchIndex])1

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = (55 + x1, 162 + y1, x2 - x1, y2 - y1)

                # bbox -> bounding box, rt -> rectagle tickness
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]

                if counter == 0:
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:

                # get the Data
                cursor.execute(
                    "SELECT * FROM Students WHERE enrollment_number = ?", (id,)
                )
                studentInfo = cursor.fetchone()

                # get the image
                if studentInfo and studentInfo[8]:
                    
                    # Convert BLOB data to numpy array and then to image
                    image_array = np.frombuffer(studentInfo[8], dtype=np.uint8)
                    imgStudent = cv2.imdecode(image_array, cv2.COLOR_BGRA2BGR)

                    imagePath = os.path.join(output_dir, f"{studentInfo[0]}.jpg")
                    with open(imagePath, "wb") as img_file:
                        img_file.write(imgStudent)
                else:
                    print("No image found for the given enrollment number.")

                # update data of attendance
                datetimeObject = datetime.strptime(studentInfo[7], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()

                if secondsElapsed > 30:
                    cursor.execute(
                        "UPDATE Students SET total_attendance = ?, last_attendance_time = ? WHERE enrollment_number = ?",
                        (
                            studentInfo[4] + 1,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            studentInfo[0],
                        ),
                    )
                    conn.commit()
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44 : 44 + 633, 808 : 808 + 414] = imgModeList[
                        modeType
                    ]

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44 : 44 + 633, 808 : 808 + 414] = imgModeList[modeType]

                if counter <= 10:

                    # total Attendance
                    cv2.putText(
                        imgBackground,
                        str(studentInfo[4]),
                        (851, 130),
                        cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (255, 255, 255),
                        1,
                    )

                    # enrollment number
                    cv2.putText(
                        imgBackground,
                        str(studentInfo[0]),
                        (990, 509),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.5,
                        (255, 255, 255),
                        1,
                    )

                    # branch
                    cv2.putText(
                        imgBackground,
                        str(studentInfo[2]),
                        (1007, 575),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.5,
                        (255, 255, 255),
                        1,
                    )

                    # year
                    cv2.putText(
                        imgBackground,
                        str(studentInfo[6]),
                        (950, 645),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.6,
                        (100, 100, 100),
                        1,
                    )

                    # batch
                    cv2.putText(
                        imgBackground,
                        str(studentInfo[5]),
                        (1040, 645),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.6,
                        (100, 100, 100),
                        1,
                    )

                    # starting year
                    cv2.putText(
                        imgBackground,
                        str(studentInfo[3]),
                        (1135, 645),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.6,
                        (100, 100, 100),
                        1,
                    )

                    (w, h), _ = cv2.getTextSize(
                        studentInfo[1], cv2.FONT_HERSHEY_COMPLEX, 1, 1
                    )

                    offset = (414 - w) // 2

                    # name
                    cv2.putText(
                        imgBackground,
                        str(studentInfo[1]),
                        (820 + offset, 445),
                        cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (100, 100, 100),
                        1,
                    )

                    imgBackground[175 : 175 + 216, 909 : 909 + 216] = imgStudent

                counter += 1
                # mark_attendance(studentInfo[1])

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44 : 44 + 633, 808 : 808 + 414] = imgModeList[
                        modeType
                    ]

    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Recognition Attendance", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord(" "):
        break

cap.release()
cv2.destroyAllWindows()
