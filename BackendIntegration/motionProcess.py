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

        #print(motionObj.count)
        if  motionObj.count % 3 == 0:
            motionObj.frameChecker[motionObj.frameIdx] = motionObj.getNonZeroCount(fgmask,windowSize)
            #print("dummy")
            if(motionObj.frameVote(motionObj.frameChecker)):
                mainMotionProccesQueue.put(True)
                #print("here")
                #@cv2.putText(frame, 'motion detected', textPosition
                    #, cv2.FONT_HERSHEY_SIMPLEX, .5, textColor, 2, cv2.LINE_AA)
            motionObj.frameIdx += 1
            motionObj.frameIdx %= motionObj.frameNumber
        #print(motionObj.frameChecker)
        mainMotionProccesQueue.put(False)
                #print(motionObj.frameChecker)

        motionObj.count += 1
        motionObj.count %= fps-1
        #print(gray_frame)
        # cv2.imshow("gray mask",fgmask)
        # cv2.waitKey(1)