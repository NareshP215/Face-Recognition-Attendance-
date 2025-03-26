# 🎯 Face Recognition Attendance   

## 📌 Overview  
The **Face Recognition Attendance System** is an AI-powered application that automates attendance marking using **OpenCV** and the **face_recognition** library. It captures and recognizes student faces in real-time, recording attendance in an **Excel sheet** for easy tracking.  

## 🛠️ Features  
✔ **Real-time Face Detection & Recognition** using OpenCV and `face_recognition`  
✔ **Automatic Attendance Marking** with Name, Roll Number, Division, Date & Time  
✔ **Excel Sheet Storage** for easy data management (`.xlsx` format)  
✔ **Multiple Division Support** for organizing student records efficiently  
✔ **High Accuracy** with pre-trained facial recognition models  
✔ **User-friendly GUI** (if applicable) for smooth interaction  

## 🚀 Tech Stack  
🔹 **Python** – Core language  
🔹 **OpenCV** – Face detection & image processing  
🔹 **face_recognition** – Facial recognition library  
🔹 **NumPy & Pandas** – Data handling  
🔹 **Excel (openpyxl / pandas)** – Attendance storage  

## 📂 Project Structure  
┣ 📜 main.py # Main script for face recognition & attendance marking.
┣ 📜 encodeing.py # Script to encode known faces.
┣ 📜 database.py # Script for the Student information.
┣ 📜 README.md # Project documentation
┣ 📜 final.png # Main Background Image
┣ 📜 1.png # Show the Actvie State.
┣ 📜 2.png # Show a student information (ID card).
┣ 📜 3.png # Show the student marke attendance.
┣ 📜 4.png # Show the student is allready marked.


## 🎯 How It Works  
1️⃣ **Face Enrollment**: Store student images in the `dataset/` folder.  
2️⃣ **Encoding Faces**: Run `encodeing.py` to generate facial encodings.  
3️⃣ **Start Attendance System**: Run `main.py` to begin face recognition.  
4️⃣ **Attendance Logging**: Recognized faces are marked in an Excel file with a timestamp.  

## 📦 Installation & Setup  
```bash
# Clone the repository  
git clone https://github.com/NareshP215/Face-Recognition-Attendance.git  
cd Face-Recognition-Attendance  

# Install required dependencies  
pip install -r requirements.txt  

# Run the main script  
python main.py  
  
