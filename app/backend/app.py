from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
#from models import User, Course, Student, StaffMember, Semester, Requirement
import cv2
from datetime import datetime

from extendedLBPH_test import *
from extendedLBPH_train import *

feed = False

app = Flask(__name__)
CORS(app, support_credentials=True)

cameraIndx=0

def gen_frames():
    camera = cv2.VideoCapture(cameraIndx)  
    while feed:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()

@app.route('/test',methods=['GET'])
def getStadiums():
    response = {'res':"there is data"}
    return jsonify(response)

@app.route('/stop_feed',methods=['GET'])
def stop_feed():
    print("in stop request")
    global feed
    feed = False
    response = {'res':"sucess"}
    return jsonify(response)

@app.route('/video_feed')
def video_feed():
    print("in live feed")
    global feed 
    feed = True
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/find_object')
def find_object():
    camera = cv2.VideoCapture(cameraIndx)
    
    success, frame = camera.read()  # read the camera frame
    image = cv2.imread('404-error.jpg',cv2.IMREAD_COLOR)
    camera.release()
    frame = image
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    var = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    return Response(var, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/track_object')
def track_object():
    image = cv2.imread('404-error.jpg',cv2.IMREAD_COLOR)
    frame = image
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    var = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    return Response(var, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/track_coords',methods=['POST'])
def take_track_coords():
    coords = request.get_json()
    print(coords)
    x1 = coords.get('x1')
    y1 = coords.get('y1')
    x2 = coords.get('x2')
    y2 = coords.get('y2')
    response = {'res':"success"}
    return jsonify(response)

person_faces = []
person_name=''
@app.route('/take_photo',methods=['GET'])
def take_photo():
    print("in take photo")
    camera = cv2.VideoCapture(cameraIndx)
    success, frame = camera.read()  # read the camera frame
    camera.release()
    global person_faces
    person_faces.append(frame)
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    var = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    print("finish take photo")
    return Response(var, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_photo2',methods=['GET'])
def take_photo2():
    print("in take photo")
    camera = cv2.VideoCapture(cameraIndx)
    success, frame = camera.read()  # read the camera frame
    camera.release()
    global person_faces
    person_faces.append(frame)
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    var = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    print("finish take photo")
    return Response(var, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_photo3',methods=['GET'])
def take_photo3():
    print("in take photo")
    camera = cv2.VideoCapture(cameraIndx)
    success, frame = camera.read()  # read the camera frame
    camera.release()
    global person_faces
    person_faces.append(frame)
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    var = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    print("finish take photo")
    return Response(var, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_photo4',methods=['GET'])
def take_photo4():
    print("in take photo")
    camera = cv2.VideoCapture(cameraIndx)
    success, frame = camera.read()  # read the camera frame
    camera.release()
    global person_faces
    person_faces.append(frame)
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    var = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    print("finish take photo")
    return Response(var, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_photo5',methods=['GET'])
def take_photo5():
    print("in take photo")
    camera = cv2.VideoCapture(cameraIndx)
    success, frame = camera.read()  # read the camera frame
    camera.release()
    global person_faces
    person_faces.append(frame)
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    var = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    print("finish take photo")
    return Response(var, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_photo6',methods=['GET'])
def take_photo6():
    print("in take photo")
    camera = cv2.VideoCapture(cameraIndx)
    success, frame = camera.read()  # read the camera frame
    camera.release()
    global person_faces
    global person_name
    person_faces.append(frame)
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    var = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    return Response(var, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_train',methods=['GET'])
def start_train():
    global person_faces
    global person_name
    print("train started")
    train_faces(label=person_name,images=person_faces)
    person_faces=[]
    person_name=""
    res=""
    print("train finished")
    return Response(res)

@app.route('/cancel_faces',methods=['GET'])
def cancel_faces():
    global person_faces
    global person_name
    person_faces=[]
    person_name=''
    res=""
    print("caaancceeeellll")
    return Response(res)

@app.route('/save_name',methods=['POST'])
def save_name():
    global person_name
    json = request.get_json()
    person_name=json.get('Name')
    print(person_name)
    res=""
    return jsonify(res)

settings=[True, False]
@app.route('/current_settings',methods=['GET'])
def current_settings():
    return jsonify(settings)

@app.route('/update_settings',methods=['POST'])
def update_settings():
    global settings
    json = request.get_json()
    settings=json.get('Current_Settings')
    print(settings)
    res=""
    return jsonify(res)

@app.route('/get_faces',methods=['GET'])
def get_faces():
    labels = readLabeslFromFile('labels1.txt')
    labels += readLabeslFromFile('labels2.txt')
    labels = list(set(labels))
    return jsonify(labels)

