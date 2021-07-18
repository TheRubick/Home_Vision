# importing libraries
import numpy as np
import cv2

from motionDetection import Mog2MotionDetector

def skipFrame(frames, cap):
    totalFrames = getFPS(cap)
    skip = totalFrames // frames    # 30 / 3 = 10  1 ..1 ..11 ..21 ..22 .. 30  ***  2    
    return skip

def getFPS(cap):
    return cap.get(cv2.CAP_PROP_FPS)

def getNonZeroCount(frame,cap,threshold = 95):
    nonZeroCount = np.count_nonzero(frame)
    min_threshold = (cap.get(3) * cap.get(4) / 100) * threshold
    nb_pixels = cap.get(3) * cap.get(4)
    nb = nb_pixels - nonZeroCount
    return not(nb > min_threshold)
    

def frameVote(frameChecker, frameNumber):
    return (np.count_nonzero(frameChecker) > frameNumber // 2)

frameNumber = 9
frameChecker = np.zeros(frameNumber)
frameIdx = 0
textColor = (255, 0,0)
textPosition = (100, 100)
# creating object
fgbg = cv2.createBackgroundSubtractorMOG2(history=1000,detectShadows=True)

# capture frames from a camera
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 900)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)

fps = getFPS(cap)
print("fps = ",fps)
count = 0
#outputVideo = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'XVID'), 20.0, (50,50))

outputVideo = cv2.VideoWriter('testCaseDummy.avi',
                            cv2.VideoWriter_fourcc('M','J','P','G'), 
                            fps=20, 
                            frameSize=(int(cap.get(3)),int(cap.get(4))))




my_mog2_detector = Mog2MotionDetector()

while(1):
    # read frames
    ret, img = cap.read()


    #Gray conversion and noise reduction (smoothening)
    gray_frame=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)
        
    outputVideo.write(img)
    fgmask = fgbg.apply(gray_frame)


    if  count % 3 == 0 :
 
        frameChecker[frameIdx] = getNonZeroCount(fgmask,cap)

        if(frameVote(frameChecker, frameNumber)):
            cv2.putText(img, 'motion detected', textPosition
            , cv2.FONT_HERSHEY_SIMPLEX, .5, textColor, 2, cv2.LINE_AA)
    
        frameIdx += 1
        frameIdx %= frameNumber

        print(frameChecker)



    count += 1
    count %= fps-1
    cv2.imshow('Original', img)
    cv2.imshow('MOG2', fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
outputVideo.release()
cv2.destroyAllWindows()



        # # Finding contour of moving object
        # cnts,_ = cv2.findContours(fgmask.copy(), 
        #                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        # for contour in cnts:
        #     if cv2.contourArea(contour) < 10000:
        #         continue
        #     motion = 1
    
        #     (x, y, w, h) = cv2.boundingRect(contour)
        #     # making green rectangle arround the moving object
        #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)