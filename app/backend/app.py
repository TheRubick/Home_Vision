from flask import Flask, json, request, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message


#from models import User, Course, Student, StaffMember, Semester, Requirement
import cv2
from datetime import datetime

# from extendedLBPH_test import *
from extendedLBPH_train import *

# track box

track_box = [0,0,0,0]

feed = False

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'homevisionapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'homevisionGP21'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
CORS(app, support_credentials=True)

cameraIndx = 0

import multiprocessing
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
directory = os.path.join(parentdir,"BackendIntegration")
sys.path.insert(0, directory)

from Main import modulesProcess

flask_main_queue,main_flask_queue = multiprocessing.Queue() , multiprocessing.Queue()

queue_from_cam = multiprocessing.Queue()


moduleProcess = multiprocessing.Process(target=modulesProcess,args=(
        flask_main_queue,main_flask_queue, queue_from_cam))

moduleProcess.start()



def gen_frames(box = False):
    # camera = cv2.VideoCapture(cameraIndx)  
    while feed:
        
        frame = queue_from_cam.get()
        if box:
            x , y = track_box[:2]
            w =  track_box[2]
            h =  track_box[3]
            cv2.rectangle(frame,(x,y),(x + w, y+ h),(255,0,0),2)


        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/stop_feed',methods=['GET'])
def stop_feed():
    global track_flag
    main_flask_queue.put({"stopFeed":True , "track_flag" : track_flag})
    print("in stop request")
    global feed
    feed = False
    response = {'res':"sucess"}
    return jsonify(response)

@app.route('/video_feed')
def video_feed():
    main_flask_queue.put({"livefeed": True})
    print("in live feed")
    global feed 
    feed = True
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/find_object/<objectId>', methods=['GET'])
def find_object(objectId):
    print("objectId = ", objectId)
    main_flask_queue.put({"find_object":True,"classID":int(objectId)})
    result = flask_main_queue.get()
    if result["found"]:
        frame = result["frame"]
    else:
        frame = cv2.imread("404-error.jpg")

    print("get images")
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    var = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    return Response(var, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/track_object')
def track_object():
    main_flask_queue.put({"livefeed": True})
    global feed 
    feed = True
    return Response(gen_frames(box= True), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/track_coords',methods=['POST'])
def take_track_coords():
    coords = request.get_json()
    print(coords, " from front")
    global track_flag
    track_flag = True
    x1 = coords.get('x1')
    y1 = coords.get('y1')
    x2 = coords.get('x2')
    y2 = coords.get('y2')
    res = {"track":True,"points":[x1,x2,y1,y2]}
    main_flask_queue.put(res)
    response = {'res':"success"}
    return jsonify(response)

person_faces = []
person_name=''
@app.route('/take_photo',methods=['GET'])
def take_photo():
    print("in take photo")
    
    main_flask_queue.put({"wantFrame":True})
    frame = flask_main_queue.get()
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

    main_flask_queue.put({"wantFrame":True})
    frame = flask_main_queue.get()
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
    main_flask_queue.put({"wantFrame":True})
    frame = flask_main_queue.get()
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
    main_flask_queue.put({"wantFrame":True})
    frame = flask_main_queue.get()
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
    main_flask_queue.put({"wantFrame":True})
    frame = flask_main_queue.get()
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
    
    main_flask_queue.put({"wantFrame":True})
    frame = flask_main_queue.get()
    global person_faces
    global person_name
    person_faces.append(frame)
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    var = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    print("finish take photo")

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

settings=[False, False]
@app.route('/current_settings',methods=['GET'])
def current_settings():
    return jsonify(settings)

@app.route('/update_settings',methods=['POST'])
def update_settings():
    global settings
    json = request.get_json()
    settings=json.get('Current_Settings')

    main_flask_queue.put({"settings": settings})
    print(settings)
    res=""
    return jsonify(res)

@app.route('/get_faces',methods=['GET'])
def get_faces():
    labels = readLabeslFromFile('labels1.txt')
    labels += readLabeslFromFile('labels2.txt')
    labels = list(set(labels))
    return jsonify(labels)

@app.route('/delete_face',methods=['POST'])
def delete_face():
    payload = request.get_json()
    face = payload.get('name')
    labels1 = readLabeslFromFile('labels1.txt')
    labels2 = readLabeslFromFile('labels2.txt')
    training_data_hist1 = readList(fileName="train1.txt")
    training_data_hist2 = readList(fileName="train2.txt")
    size = len(labels1)
    i = 0
    while(i < size):
        if labels1[i] == face:
            labels1.pop(i)
            training_data_hist1.pop(i)
            size-=1
            continue
        i+=1
    size = len(labels2)
    i = 0
    while(i < size):
        if labels2[i] == face:
            labels2.pop(i)
            training_data_hist2.pop(i)
            size-=1
            continue
        i+=1
    writeFile(fileName="train1.txt",l=training_data_hist1)
    writeFile(fileName="train2.txt",l=training_data_hist2)
    writeLabelsToFile(fileName='labels1.txt',l=labels1)
    writeLabelsToFile(fileName='labels2.txt',l=labels2)
    return jsonify("")


@app.route('/from_main',methods=['GET'])
def from_main():

    mode = request.args.get("mode")
    msg = None
    if mode == "motion":
        msgText = "Motion is detected .... check it out :D"
    if mode == "track":
        global track_flag
        track_flag = False
        global track_box 
        track_box = [0,0,0,0]
        msgText = "Your object is out of the scene :("
    if mode == "face":
        name = request.args.get("name")
        if name == "unknown":
            msgText = "there is a person in the scene and we dont know it :("
        else:
            msgText = " Say hello to your friend {}".format(name)

    msg = Message(mode.upper(), sender = 'homevisionapp@gmail.com', recipients = ['gellesh.arg@gmail.com'])
    msg.body = msgText
    mail.send(msg)
    return "dummy"

@app.route('/from_track',methods=['GET'])
def from_track():

    # x , y ,w ,h
    x = int(request.args.get("x1"))
    y = int(request.args.get("y1"))

    w = int(request.args.get("w"))

    h = int(request.args.get("h"))

    global track_box 

    track_box = [ x ,y , w , h ] 
    
    # msg = Message('Hello', sender = 'homevisionapp@gmail.com', recipients = ['engjimmy98@gmail.com'])
    # msg.body = "Hello Flask message sent from Flask-Mail"
    # mail.send(msg)
    return "dummy"
track_flag = False
@app.route('/track_flag',methods=['GET'])
def track_flag():
    global track_flag

    response = {'flag':track_flag}
    return jsonify(response)

@app.route('/track_flag_stop',methods=['GET'])
def track_flag_stop():

    global track_flag
    # payload = request.get_json()
    track_flag = False
    global track_box 
    track_box = [0,0,0,0]
    main_flask_queue.put({"closeTrack":True})
    return jsonify('success')
email = "engjimmy98@gmail.com"
@app.route('/change_mail',methods=['POST'])
def changeEmail():
    global email
    payload = request.get_json()
    email = payload.get('email')   
    return jsonify('success')
@app.route('/get_mail',methods=['GET'])
def getEmail():
    global email
    res = {
        'email':email
    }
    return jsonify(res)
useCaseEnabledFlag = False
useCaseItem = ""
useCaseFace = ""
@app.route('/get_use_case',methods = ['GET'])
def getUseCase():
    global useCaseEnabledFlag
    global useCaseItem
    global useCaseFace
    res = {
        "flag":useCaseEnabledFlag,
        "item":useCaseItem,
        "face": useCaseFace
    }
    return jsonify(res)
@app.route('/set_use_case',methods = ['POST'])
def setUseCase():
    global useCaseEnabledFlag
    global useCaseItem
    global useCaseFace
    payload = request.get_json()
    useCaseEnabledFlag = payload.get("flag")
    useCaseFace = payload.get("face")
    useCaseItem = payload.get("item")
    #print(useCaseEnabledFlag)
    return jsonify("")
