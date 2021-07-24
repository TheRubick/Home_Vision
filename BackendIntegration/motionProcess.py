import cv2

def motionDetectorProcess(motionObj,fps,windowSize,motionProcessQueue,mainMotionProccesQueue):
    """
    This is a function which will be invoke the motion detector
    """
    while True:
        #Gray conversion and noise reduction (smoothening)
        frame = motionProcessQueue.get()
        gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)
                    
        fgmask = motionObj.fgbg.apply(gray_frame)

        if  motionObj.count % 3 == 0:
            motionObj.frameChecker[motionObj.frameIdx] = motionObj.getNonZeroCount(fgmask,windowSize)
            if(motionObj.frameVote(motionObj.frameChecker)):
                mainMotionProccesQueue.put(True)
                
            motionObj.frameIdx += 1
            motionObj.frameIdx %= motionObj.frameNumber
        
        mainMotionProccesQueue.put(False)

        motionObj.count += 1
        motionObj.count %= fps-1