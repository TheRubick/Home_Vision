import cv2
from adaMotionClass import motionDetector
from time import time
import kcftracker
from adaMotionClass import motionDetector
import pickle

def motionDetectorProcess(motionObj,fps,windowSize,motionProcessQueueOne,):
    """
    This is a function which will be invoke the motion detector
    """
    while True:
        #Gray conversion and noise reduction (smoothening)
        frame = motionProcessQueueOne.get()
        gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)
                    
        fgmask = motionObj.fgbg.apply(gray_frame)


        if  motionObj.count % 3 == 0:
            motionObj.frameChecker[motionObj.frameIdx] = motionObj.getNonZeroCount(fgmask,windowSize)

            if(motionObj.frameVote(motionObj.frameChecker)):
                textColor = (255, 0,0)
                textPosition = (100, 100)
                
                #@cv2.putText(frame, 'motion detected', textPosition
                    #, cv2.FONT_HERSHEY_SIMPLEX, .5, textColor, 2, cv2.LINE_AA)
                
                motionObj.frameIdx += 1
                motionObj.frameIdx %= motionObj.frameNumber

                print(motionObj.frameChecker)

            motionObj.count += 1
            motionObj.count %= fps-1
        print(gray_frame)
        cv2.imshow("gray mask",fgmask)
        cv2.waitKey(1)

    
def draw_boundingbox(event, x, y,flags,param):
    
    if event == cv2.EVENT_LBUTTONDOWN:
        selectingObject = True
        onTracking = False
        ix, iy = x, y
        cx, cy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        cx, cy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        selectingObject = False
        if(abs(x - ix) > 10 and abs(y - iy) > 10):
            w, h = abs(x - ix), abs(y - iy)
            ix, iy = min(x, ix), min(y, iy)
            initTracking = True
        else:
            onTracking = False

    elif event == cv2.EVENT_RBUTTONDOWN:
        onTracking = False
        if(w > 0):
            ix, iy = x - w / 2, y - h / 2
            initTracking = True

global selectingObject,initTracking,onTracking,ix, iy, cx, cy,w, h
def objectTrackerProcess(trackerProcessQueue):
    
    selectingObject = False
    initTracking = False
    onTracking = False
    ix, iy, cx, cy = -1, -1, -1, -1
    w, h = 0, 0

    inteval = 1
    duration = 0.01
    tracker = kcftracker.KCFTracker(True, True, True)  # hog, fixed_window, multiscale
    # if you use hog feature, there will be a short pause after you draw a first boundingbox, that is due to the use of Numba.

    cv2.namedWindow('tracking')
    cv2.setMouseCallback('tracking', draw_boundingbox)

    while True:
        frame = trackerProcessQueue.get()
        if(selectingObject):
            cv2.rectangle(frame, (ix, iy), (cx, cy), (0, 255, 255), 7)
        elif(initTracking):
            cv2.rectangle(frame, (ix, iy), (ix + w, iy + h), (0, 255, 255), 7)
            print([ix, iy, w, h])
            tracker.init([ix, iy, w, h], frame)

            initTracking = False
            onTracking = True
        elif(onTracking):
            t0 = time()
            boundingbox = tracker.update(frame)
            t1 = time()

            boundingbox = list(map(int, boundingbox))
            print(boundingbox)
            cv2.rectangle(frame, (boundingbox[0], boundingbox[1]), (boundingbox[0] + boundingbox[2], boundingbox[1] + boundingbox[3]), (255, 0, 0), 7)

            duration = 0.8 * duration + 0.2 * (t1 - t0)
            #duration = t1-t0
            cv2.putText(frame, 'FPS: ' + str(1 / duration)[:4].strip('.'), (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow('tracking', frame)
        cv2.waitKey(inteval)