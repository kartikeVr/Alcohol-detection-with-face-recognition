import socket
import sqlite3
from simple_facerec import SimpleFacerec
import face_recognition
import cv2
import os
import glob
import numpy as np
from datetime import datetime

now = datetime.now()
format = "%Y-%m-%d %H:%M:%S"  # Year-Month-Day Hour:Minute:Second
format_string = now.strftime(format)
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 81  # Port to listen on (default web server port)
name = ""
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")
conn = sqlite3.connect("sqlite.db")

known_face_encodings = []
known_face_names = []
frame_resizing = 0.20

arr1 = ["Kartike Verma", "bharat singh bhati", "Bhumika Kapoor", "Raj Singh Chauhan", "Utkarsh Ranjan"]
arr2 = [["\n\n Name: Kartike Verma", "Course: Btech CSE", "Batch: 2022-2026 ", "Enrollment No: A20405222069"],
        ["\n\n Name: Bharat Singh Bhati \n Course: Btech CSE \n Batch: 2022-2026 \n Enrollment No: A20405222072"],
        ["\n\n Name: Bhumika Kapoor \n Course: Btech BioTech. \n Batch: 2022-2026 \n Enrollment No: A2024122025"],
        ["\n\n Name: Ananya Pandey \n Course: Btech CSE \n Batch: 2022-2026 \n Enrollment No: A20405222061"],
        ["\n\n Name: Utkarsh Ranjan \n Course: B.Teh + M.Tech Dual \n Batch: 2019-2024 \n Enrollment No: A20422119002"]]
Name = ["kartike  ", "Bharat Singh Bhati", "Bhumika Kapoor", "Raj Singh Chauhan"]
Course = ["Btech  ", "Btech CSE", "Btech BioTech", "BTech CSE"]
Batch = ["2022-2026 ", "2022-2026", "2022-2026", "2022-2026"]
Enrollment_No = ["A20405222069 ", "A20405222069", "A2024122025", "A20405222110"]


def custom_datetime_format():
    now = datetime.now()
    # Define your custom format
    custom_format = "%Y-%m-%d %H:%M:%S"
    # Format the current date and time
    formatted_datetime = now.strftime(custom_format)
    # Print the formatted date and time
    return formatted_datetime
a=custom_datetime_format()

def load_encoding_images(images_path):
    """
    Load encoding images from path
    :param images_path:
    :return:
    """
    # Load Images
    images_path = glob.glob(os.path.join(images_path, "."))

    print("{} encoding images found.".format(len(images_path)))

    # Store image encoding and names
    for img_path in images_path:
        img = cv2.imread(img_path)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        basename = os.path.basename(img_path)
        (filename, ext) = os.path.splitext(basename)
        img_encoding = face_recognition.face_encodings(rgb_img)[0]
        known_face_encodings.append(img_encoding)
        known_face_names.append(filename)
    print("Encoding images loaded")


def parse_http_request(data):
    try:
        # Decode bytes to string (if not already done before calling this function)
        if isinstance(data, bytes):
            data = data.decode('utf-8')

        # Split request into lines
        request_lines = data.split("\r\n")

        # Find the index where the body starts (usually after an empty line)
        empty_line_index = request_lines.index('')

        # The body should be the next line after the empty line
        body = request_lines[empty_line_index + 1]
        return body
    except Exception as e:
        print(f"Failed to parse HTTP request: {e}")
        return None


def detect_known_faces(frame):
    small_frame = cv2.resize(frame, (0, 0), fx=40, fy=40)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)

    face_locations = np.array(face_locations)
    face_locations = face_locations / frame_resizing
    return face_locations.astype(int), face_names


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    con, addr = s.accept()
    with con:
        print('Connected by', addr)
        while True:
            data = con.recv(1024)  # Ensure you decode the received bytes to a string
            if not data:
                break

            message = parse_http_request(data)
            message = "HIGH_SIGNAL"
            if message == "HIGH_SIGNAL":  # Match the message sent by ESP32
                print("High signal detected! Running Python script...")
                while True:
                    cap = cv2.VideoCapture("http://192.168.66.235:81/stream")
                    ret, frame = cap.read()

                    # Detect Faces
                    face_locations, face_names = sfr.detect_known_faces(frame)
                    for face_loc, name in zip(face_locations, face_names):
                        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

                    cv2.imshow("Frame", frame)
                    if name in arr1:
                        x = arr1.index(name)
                        print(Name[x], Course[x], Batch[x], Enrollment_No[x],custom_datetime_format())
                        ch = f"""CREATE TABLE IF NOT EXISTS store2 (
                        Name VARCHAR(35),
                        Course VARCHAR(35),
                        Batch VARCHAR(35),
                        Enrollment_No VARCHAR(25) PRIMARY KEY,
                        Count INTEGER DEFAULT 1,
                        Time VARCHAR(35)
);
"""
                        a = f"""
                        INSERT INTO store2 (Name, Course, Batch, Enrollment_No,Time)
                        VALUES ("{Name[x]}", "{Course[x]}", "{Batch[x]}", "{Enrollment_No[x]}","{custom_datetime_format()}")
                        ON CONFLICT(Enrollment_No) DO UPDATE SET Count = Count + 1;
"""

                        cha = """create table if not exists store(Name VARCHAR(20),Course VARCHAR(20),Enrollment_No VARCHAR(20));"""
                        conn.execute(ch)
                        conn.execute(a)

                        conn.commit()
                        cap.release()
                        cv2.destroyAllWindows()
                        name = None
                    else:
                        print("Unknown User")

                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                break
                # (e.g., control hardware, send notifications)
            else:
                print("Unknown message received:", data.decode())

conn.close()
