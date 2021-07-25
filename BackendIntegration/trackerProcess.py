import cv2
from time import time
import kcftracker


def objectTrackerProcess(trackerProcessQueue,mainProcessQueue,ix, iy, frameWidth, frameHeight, w, h):
    """
    function to handle the tracking process including the initial frame and its subsequence frames' updates
    """
    initTracking = True
    onTracking = False
    
    tracker = kcftracker.KCFTracker(True, True, True)  # hog, fixed_window, multiscale
    
    while True:
        trackerStatus = mainProcessQueue.get()
        frame = trackerStatus["frame"]
        set_track = trackerStatus["set_track"]

        initTracking = True if not set_track else False

        if(initTracking):
            ix , iy , w , h = trackerStatus["rect"]
            cv2.rectangle(frame, (ix, iy), (ix + w, iy + h), (0, 255, 255), 7)
            #print([ix, iy, w, h])
            tracker.init([ix, iy, w, h], frame)

            initTracking = False
            onTracking = True
            trackerProcessQueue.put("go on")

        elif(onTracking):
            boundingbox = tracker.update(frame)

            boundingbox = list(map(int, boundingbox))

            cx = (boundingbox[0]) + (boundingbox[2] // 2)
            cy = (boundingbox[1]) + (boundingbox[3] // 2)


                    

            #print(boundingbox)
            cv2.rectangle(frame, (boundingbox[0], boundingbox[1]), (boundingbox[0] + boundingbox[2], boundingbox[1] + boundingbox[3]), (255, 0, 0), 7)

           
            trackerResp = {
                "frame" : frame,
                "resp" : False, 
                "box":boundingbox
            }

            
            if((cx > frameWidth or cx < 0) or (cy > frameHeight or cy < 0)):
                # print("cx = ",cx," cy = ",cy)
                # print("height = ",frameHeight," width = frameWidth")
                trackerResp["resp"] = True

            trackerProcessQueue.put(trackerResp)

        #cv2.imshow('tracking', frame)
        #cv2.waitKey(inteval)