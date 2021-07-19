# importing libraries
import numpy as np
import cv2


class motionDetector:
    def __init__(self,frameNumber=9,history=500):
        self.frameNumber = frameNumber
        self.frameChecker = np.zeros(self.frameNumber)
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=1000,detectShadows=True)
        self.frameIdx = 0
        self.count = 0
    

    def skipFrame(self, frames, cap):
        totalFrames = self.getFPS(cap)
        skip = totalFrames // frames    # 30 / 3 = 10  1 ..1 ..11 ..21 ..22 .. 30  ***  2    
        return skip

    def getFPS(self, cap):
        return cap.get(cv2.CAP_PROP_FPS)

    def getNonZeroCount(self, frame, windowSize, threshold = 95):
        nonZeroCount = np.count_nonzero(frame)
        min_threshold = (windowSize / 100) * threshold
        nb_pixels = windowSize
        nb = nb_pixels - nonZeroCount
        return not(nb > min_threshold)
    
    def frameVote(self,frameChecker):
        return (np.count_nonzero(frameChecker) > self.frameNumber // 2)



if(__name__ == "__main__"):
    # capture frames from a camera
    cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 900)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)

    motionObj = motionDetector()
    fps = motionObj.getFPS(cap)
    print("fps = ",fps)
    count = 0
    #outputVideo = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'XVID'), 20.0, (50,50))
    frameIdx = 0
    outputVideo = cv2.VideoWriter('testCaseDummy.avi',
                                cv2.VideoWriter_fourcc('M','J','P','G'), 
                                fps=20, 
                                frameSize=(int(cap.get(3)),int(cap.get(4))))




    #my_mog2_detector = Mog2MotionDetector()

    while(1):
        # read frames
        ret, img = cap.read()


        #Gray conversion and noise reduction (smoothening)
        gray_frame=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)
                
        outputVideo.write(img)
        fgmask = motionObj.fgbg.apply(gray_frame)


        if  count % 3 == 0 :
            motionObj.frameChecker[frameIdx] = motionObj.getNonZeroCount(fgmask,cap)

            if(motionObj.frameVote(motionObj.frameChecker, motionObj.frameNumber)):
                textColor = (255, 0,0)
                textPosition = (100, 100)
                cv2.putText(img, 'motion detected', textPosition
                , cv2.FONT_HERSHEY_SIMPLEX, .5, textColor, 2, cv2.LINE_AA)
            
            frameIdx += 1
            frameIdx %= motionObj.frameNumber

            print(motionObj.frameChecker)

        count += 1
        count %= fps-1
        cv2.imshow('Original', img)
        cv2.imshow('MOG2', fgmask)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    cap.release()
    outputVideo.release()
    cv2.destroyAllWindows()