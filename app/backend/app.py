from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
#from models import User, Course, Student, StaffMember, Semester, Requirement
import cv2
from datetime import datetime
feed = False

app = Flask(__name__)
CORS(app, support_credentials=True)



def gen_frames():
    camera = cv2.VideoCapture(0)  
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


person_faces = []
person_name=''
@app.route('/take_photo',methods=['GET'])
def take_photo():
    print("in take photo")
    camera = cv2.VideoCapture(0)
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
    camera = cv2.VideoCapture(0)
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
    camera = cv2.VideoCapture(0)
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
    camera = cv2.VideoCapture(0)
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
    camera = cv2.VideoCapture(0)
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
    camera = cv2.VideoCapture(0)
    success, frame = camera.read()  # read the camera frame
    camera.release()
    global person_faces
    person_faces.append(frame)
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    var = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    print(person_faces[0])
    return Response(var, mimetype='multipart/x-mixed-replace; boundary=frame')

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