"""
 MAIN FILE that open processes and communicate with API
"""


from os import sendfile
from pickle import FALSE
from flask.json import jsonify

from flask.wrappers import Response
from numba.core.serialize import FastNumbaPickler
from numpy.core.numeric import False_
from requests.api import head
from adaMotionClass import motionDetector
import multiprocessing
from trackerProcess import objectTrackerProcess
from motionProcess import motionDetectorProcess
from detectionProcess import objectDetectionProcess
from detect_RecognizeProcess import FaceDetectionProcess , FaceObjProcess
import requests

import cv2
import time

def modulesProcess(flask_main_queue,main_flask_queue, queue_from_cam):

    cap = cv2.VideoCapture(0)

    ret,frame = cap.read()

    liveFeed = False


    # Face and object
    send_face_obj = False
    face_object = {"name":None, "object":None, "on_off":False}

    faceObjProcessQueue = multiprocessing.Queue()
    mainFaceObjProcessQueue = multiprocessing.Queue()

    faceObjProcess = multiprocessing.Process(target=FaceObjProcess,args=(
        faceObjProcessQueue,mainFaceObjProcessQueue))

    faceObjProcess.start()

    # Face detection
    
    def most_common(lst):
        return max(set(lst), key=lst.count)

    faceCoolDownPeriod = 10 # in seconds
    resetFaceDetection = False
    faceTimer = None
    face_rego = False

    faces = []
    faceVotes = 3
    receiveFace = False   # face on / off   
    sentFace = False

    faceProcessQueue = multiprocessing.Queue()
    mainFaceProcessQueue = multiprocessing.Queue()

    faceProcess = multiprocessing.Process(target=FaceDetectionProcess,args=(
        faceProcessQueue,mainFaceProcessQueue))

    faceProcess.start()


   

    
    # object detection

    sentObj = False
    detectionProcessQueue = multiprocessing.Queue()
    mainDetectionProcessQueue = multiprocessing.Queue()

    detectionProcess = multiprocessing.Process(target=objectDetectionProcess,args=(
        detectionProcessQueue,mainDetectionProcessQueue,))

    detectionProcess.start()


    class_to_detect = 4  # set by back
    detectOn = False    # set by back   obj on / off 

    receiveTracker = False  # tracker on / off
    set_track = False
    rect_box = [150,174,200,200] # will get from backend to as tracking boundbox
    trackerProcessQueue = multiprocessing.Queue()
    mainProcessQueue = multiprocessing.Queue()
    selectingObject = False
    firstTrack = False
    initTracking = False
    onTracking = False
    ix, iy, cx, cy = -1, -1, -1, -1
    w, h = 0, 0
    trackerProcess = multiprocessing.Process(target=objectTrackerProcess,args=
    (trackerProcessQueue,mainProcessQueue,248,174,cap.get(3),cap.get(4),200,200))
    
    trackerProcess.start()

    
    
    recieveMotion = False # motion on / off
    coolDownPeriod = 60 # in seconds
    resetMotionDetection = False
    startedTimer = False
    timer = None
    
    motionObj = motionDetector()
    windowSize = cap.get(3) * cap.get(4)
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    frameIdx = 0
    mainMotionProcessQueue = multiprocessing.Queue()
    motionProcessQueueOne = multiprocessing.Queue()
    motionProcess = multiprocessing.Process(target=motionDetectorProcess,
    args=(motionObj,fps,windowSize,motionProcessQueueOne,mainMotionProcessQueue,))
    
    #starting the child processes
    motionProcess.start()
    
    while True:
        # flask_main_queue.put("from main hahahahaha")
    


        ret,frame = cap.read()
        if ret == True:

           
            
            #initiating motion detection and the object tracking processes with their queues
            #joining the child processes
            motionProcessQueueOne.put(frame)
        

            try:
                # messages taken from API 
                msg = main_flask_queue.get_nowait()

                if "settings" in msg:
                    print("setting changed")
                    receiveFace , recieveMotion= msg["settings"]
                    face_rego = receiveFace
                    faces = []


                if "track" in msg:
                    receiveTracker = True
                   
                    width = frame.shape[0]
                    height = frame.shape[1]
                    x1 , x2 = (float(msg["points"][0])) * height, (float(msg["points"][1])) * height
                    y1 , y2 = (float(msg["points"][2])) * width, (float(msg["points"][3])) * width
                
                    rect_box = [int(x1),int(y1),int(x2-x1),int(y2-y1)]
                

                if "livefeed" in msg:
                    liveFeed = True
                    # send frame to flask
                    queue_from_cam.put(frame)
  
                if "stopFeed" in msg:
                    liveFeed = False
            

                if "closeTrack" in msg:
                    cv2.destroyWindow('tracking')
                    receiveTracker = False


                if "find_object" in msg:
                    detectOn = True
                    class_to_detect = msg["classID"]

                if "wantFrame" in msg:
                    flask_main_queue.put(frame)


                if "face_object" in msg:
                    print(msg)
                    face_object["on_off"] = msg["face_object"]
                    receiveFace = msg["face_object"]
                    face_object["name"] = msg["name"]
                    face_object["object"] = msg["object"]

            except:
                if liveFeed == True:
                    queue_from_cam.put(frame)    
                pass

            
         


            trackerStatus = {
                "frame" : frame,
                "set_track" : set_track, # to set co_ordinate or get track
                "rect" : rect_box  

            }

        
            #########################################
            #         object Tracking               #
            #########################################
            

            if not initTracking:
                mainProcessQueue.put(trackerStatus)
                dum = trackerProcessQueue.get()
                initTracking = True
            else:
                if receiveTracker:
                    mainProcessQueue.put(trackerStatus)

                    if not set_track:
                        # send rect_box to initliaze bounding box
                        trackerProcessQueue.get()
                        set_track = True
                        # cv2.imshow('tracking', frameTracker["frame"])
                        # cv2.waitKey(1)
                        #this frame should be sended to the backend
                    else:


                        frameTracker = trackerProcessQueue.get()
                        if frameTracker["resp"]:
                            # object exit scence send to users
                            print("object is not found anymore......")
                            receiveTracker = False
                            cv2.destroyWindow('tracking')
                            resp = requests.get(url = "http://0.0.0.0:5000/from_main?mode={}".format("track"))
                            requests.get(url="http://0.0.0.0:5000/stop_feed")
                            liveFeed = False
                        else:
                            print(frameTracker["box"])
                            x1 , y1 , w , h = frameTracker["box"]
                            if liveFeed:
                                requests.get("http://0.0.0.0:5000/from_track?x1={}&y1={}&w={}&h={}".
                                format(x1,y1,w,h))

                            cv2.imshow('tracking', frameTracker["frame"])
                            cv2.waitKey(1)
                        #this frame should be sended to the backend
                else:
                    trackerStatus["set_track"] = False
                    mainProcessQueue.put(trackerStatus)
                    trackerProcessQueue.get()


            #########################################
            #         motion detection              #
            #########################################
            motionOccured = mainMotionProcessQueue.get()
            
            if not resetMotionDetection:
                if motionOccured and recieveMotion:
                    print("motion detected")
                    #integrate with the back
                    response = {"motion":True}
                    resp = requests.get(url = "http://0.0.0.0:5000/from_main?mode={}".format("motion"))
                    # print(resp.text)
                    resetMotionDetection = True
                    startedTimer = True
                    timer = time.time()
            
            if(startedTimer):
                if(time.time() - timer >= coolDownPeriod):
                    resetMotionDetection = False
                    startedTimer = False
            
             
            '''
            count = motionProcessQueue.get()
            frameIdx = motionProcessQueue.get()
            '''
            
            cv2.imshow("Camera Feedback",frame)

            #########################################
            #         object detection              #
            #########################################

            if detectOn:
                if not sentObj:
                    mainDetectionProcessQueue.put({"frame":frame, "class":class_to_detect })
                    sentObj = True
                try:
                    result = detectionProcessQueue.get_nowait()
                    if "found" in result:
                        sentObj = False
                        if result["found"]:
                            # print("obj founded")
                            # send to user obj location in scene
                            flask_main_queue.put({"frame":result["image"],"found":True})
                            cv2.imshow('detection', result["image"])
                            cv2.waitKey(1)
                        else:
                            print("obj not founded")
                            flask_main_queue.put({"frame":frame,"found":False})
                            # send to user obj location in scene
                    detectOn = False
                except:
                        pass

                


            #########################################
            #         Face detection              #
            #########################################

            if receiveFace:
                if not sentFace:
                    mainFaceProcessQueue.put({"frame":frame,"status":"face"})
                    sentFace = True
                try:
                    result = faceProcessQueue.get_nowait()

                    print(result)
                    if "found" in result:
                        if result["found"]:
                            if result["faceName"] == None:
                                pass
                            else:
                                faces.append(result["faceName"])

                        sentFace = False
                        print(faces)
                        if result["found"] and len(faces)==faceVotes:
                            most = most_common(faces)
                            faces = []
                            print(" most face detected is {}".format(most))
                            # send to user obj location in scene
                            
                            if not resetFaceDetection and face_rego:
                                # send mail and start timer
                                print("send mail to {} *******************************".format(most))
                                resp = requests.get(url ="http://0.0.0.0:5000/from_main?mode={}&name={}"
                                .format("face",most))
                                faceTimer = time.time()
                                resetFaceDetection = True
                                
                            # cv2.imshow('detection', result["image"])
                            # cv2.waitKey(1)


                            if face_object["on_off"] and face_object["name"] == most:
                                if not send_face_obj :

                                    mainFaceObjProcessQueue.put({"frame":frame,"class":face_object["object"]})
                                    send_face_obj = True
                                else:
                                    try:
                                        result = faceObjProcessQueue.get_nowait()
                                        send_face_obj = False
                                        if "found" in result:
                                            if result["found"]:
                                                # flask_main_queue.put({"frame":result["image"],"found":True})
                                                print("object with face detected {}".format(most))
                                                cv2.imwrite("frame.jpg", result["image"])
                                                resp = requests.get(url ="http://0.0.0.0:5000/from_main?mode={}&name={}&obj={}"
                                                .format("face_obj",most,face_object["object"]))
                                                
                                            else:
                                                print("obj not founded with face {}".format(most))
                                        
                                    except:
                                        pass
                                        


                        elif not result["found"]:
                            print("calculate face votes")
                            # send to user obj location in scene 

                except:
                        pass


            if(resetFaceDetection):
                if(time.time() - faceTimer >= faceCoolDownPeriod):
                    resetFaceDetection = False
                
            

        if cv2.waitKey(1) == ord('q'):
            break
    
    #motionProcess.join()
    trackerProcess.join()
    motionProcess.join()
    detectionProcess.join()
    faceProcess.join()
    faceObjProcess.join()
    cap.release()
    cv2.destroyAllWindows()
    #integrationUtils.objectTrackerProcess()