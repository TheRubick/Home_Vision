from adaMotionClass import motionDetector
import multiprocessing
from trackerProcess import objectTrackerProcess
from motionProcess import motionDetectorProcess
import cv2
import pickle
import kcftracker
import time

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    ret,frame = cap.read()
    


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

            

        if cv2.waitKey(1) == ord('q'):
            break
    
    #motionProcess.join()
    trackerProcess.join()
    motionProcess.join()
    cap.release()
    cv2.destroyAllWindows()
    #integrationUtils.objectTrackerProcess()