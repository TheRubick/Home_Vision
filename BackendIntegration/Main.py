from adaMotionClass import motionDetector
import multiprocessing
from integrationUtils import motionDetectorProcess
import cv2

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    motionObj = motionDetector()
    windowSize = cap.get(3) * cap.get(4)
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    frameIdx = 0
    fgbg = cv2.createBackgroundSubtractorMOG2(history=1000,detectShadows=True)
    while True:
        ret,frame = cap.read()
        if ret == True:
            #initiating motion detection and the object tracking processes with their queues
            motionProcessQueue = multiprocessing.Queue()
            motionProcess = multiprocessing.Process(target=motionDetectorProcess,
            args=(motionObj,fgbg,count,frame,fps,windowSize,frameIdx,motionProcessQueue,))
            
            #starting the child processes
            motionProcess.start()

            #joining the child processes
            motionProcess.join()

            #motion detection 
            motionObj = motionProcessQueue.get()
            count = motionProcessQueue.get()
            frameIdx = motionProcessQueue.get()
            
            cv2.imshow("Camera Feedback",frame)

        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    #integrationUtils.objectTrackerProcess()