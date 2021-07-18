from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
#from models import User, Course, Student, StaffMember, Semester, Requirement
import cv2
from datetime import datetime



app = Flask(__name__)
CORS(app, support_credentials=True)


camera = cv2.VideoCapture(1)

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/test',methods=['GET'])
def getStadiums():
    response = {'res':"there is data"}
    return jsonify(response)

@app.route('/video_feed')
def video_feed():
    print("in live feed")
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
