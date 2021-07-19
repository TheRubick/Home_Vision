from os import sendfile
from adaMotionClass import motionDetector
import multiprocessing
from trackerProcess import objectTrackerProcess
from motionProcess import motionDetectorProcess
from detectionProcess import objectDetectionProcess
from detect_RecognizeProcess import FaceDetectionProcess


import cv2
import time

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    ret,frame = cap.read()

    # Face detection
    

    receiveFace = True
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
    detectOn = True    # set by back

    receiveTracker = True
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

    
    
    recieveMotion = True
    coolDownPeriod = 5 # in seconds
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
        ret,frame = cap.read()
        if ret == True:
            #initiating motion detection and the object tracking processes with their queues
            #joining the child processes
            motionProcessQueueOne.put(frame)
            
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
                #print(dum)
                #print("heererererererereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
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
                        else:
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
            #print(motionOccured)
            
            if not resetMotionDetection:
                if motionOccured and recieveMotion:
                    print("motion detected")
                    #integrate with the back
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
                            print("obj founded")
                            # send to user obj location in scene
                            cv2.imshow('detection', result["image"])
                            cv2.waitKey(1)
                        else:
                            print("obj not founded")
                            # send to user obj location in scene

                except:
                        pass

                


            #########################################
            #         Face detection              #
            #########################################

            if receiveFace:
                if not sentFace:
                    mainFaceProcessQueue.put({"frame":frame})
                    sentFace = True
                try:
                    result = faceProcessQueue.get_nowait()
                    if "found" in result:
                        sentFace = False
                        if result["found"]:
                            print("Face detected")
                            # send to user obj location in scene
                            cv2.imshow('detection', result["image"])
                            cv2.waitKey(1)
                        else:
                            print("no Face founded")
                            # send to user obj location in scene

                except:
                        pass
                
                
            

        if cv2.waitKey(1) == ord('q'):
            break
    
    #motionProcess.join()
    trackerProcess.join()
    motionProcess.join()
    detectionProcess.join()
    faceProcess.join()
    cap.release()
    cv2.destroyAllWindows()
    #integrationUtils.objectTrackerProcess()