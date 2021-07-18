from adaMotionClass import motionDetector
import multiprocessing
from integrationUtils import motionDetectorProcess, objectTrackerProcess
import cv2
import pickle

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    ret,frame = cap.read()
    motionObj = motionDetector()
    windowSize = cap.get(3) * cap.get(4)
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    frameIdx = 0
    motionProcessQueueOne = multiprocessing.Queue()
    motionProcess = multiprocessing.Process(target=motionDetectorProcess,
    args=(motionObj,fps,windowSize,motionProcessQueueOne,))
    #starting the child processes
    #motionProcess.start()
    trackerProcessQueue = multiprocessing.Queue()

    selectingObject = False
    initTracking = False
    onTracking = False
    ix, iy, cx, cy = -1, -1, -1, -1
    w, h = 0, 0
    trackerProcess = multiprocessing.Process(target=objectTrackerProcess,args=
    (trackerProcessQueue,))
    
    trackerProcess.start()
    while True:
        ret,frame = cap.read()
        if ret == True:
            #initiating motion detection and the object tracking processes with their queues
            
            #joining the child processes
            #motionProcessQueueOne.put(frame)

            trackerProcessQueue.put(frame)
            #motion detection 
            '''
            count = motionProcessQueue.get()
            frameIdx = motionProcessQueue.get()
            '''
            
            cv2.imshow("Camera Feedback",frame)

        if cv2.waitKey(1) == ord('q'):
            break
    
    #motionProcess.join()
    trackerProcess.join()
    cap.release()
    cv2.destroyAllWindows()
    #integrationUtils.objectTrackerProcess()