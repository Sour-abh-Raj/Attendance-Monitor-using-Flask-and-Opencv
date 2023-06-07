import os
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from flask import Flask, jsonify, render_template, Response, request
import vicinity_checker

app = Flask(__name__,static_folder='static')
app.template_folder = 'templates'

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def marker(name, attendance_file):
    with open(attendance_file, 'a+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.write(f'\n{name},{dtString}')
            
def resource_check():
    filename = "Attendance.csv"
    folder_name = "attendanceResources"
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, folder_name)
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("Name,Timestamp\n")
        print("Attendance file created.")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"'{folder_name}' created successfully.")
    else:
        pass

def mark_attendance(vicinity, csv_file):
    resource_check()
    path = 'attendanceResources'
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    cap = cv2.VideoCapture(0)
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    if vicinity_checker.check_location_in_vicinity(vicinity, csv_file):
        marked_attendance = set()  # Set to store the names of the faces already marked
        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    if name not in marked_attendance:
                        marker(name, 'Attendance.csv')
                        marked_attendance.add(name)
                    
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            ret, jpeg = cv2.imencode('.jpg', img)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        print('You are not in the vicinity of the location')
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n\r\n')

    
@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance_route():
    if request.method == 'GET':
        vicinity = 100
        csv_file = 'current_location_tag.csv'  # CSV file containing the geolocation tag
        return render_template('mark_attendance.html', vicinity=vicinity, csv_file=csv_file)

    elif request.method == 'POST':
        vicinity = int(request.form.get('vicinity'))
        csv_file = request.form.get('csv_file')
        mark_attendance(vicinity, csv_file)
        return jsonify(message="Attendance marked successfully.")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    vicinity = 100  # Default value
    csv_file = 'current_location_tag.csv'  # Default value

    if request.args.get('vicinity') and request.args.get('csv_file'):
        vicinity = int(request.args.get('vicinity'))
        csv_file = request.args.get('csv_file')

    return Response(mark_attendance(vicinity, csv_file), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)