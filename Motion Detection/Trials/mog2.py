# importing libraries
import numpy as np
import cv2
  

def skipFrame(frames, cap):
    totalFrames = getFPS(cap)
    skip = totalFrames // frames    # 30 / 3 = 10  1 ..1 ..11 ..21 ..22 .. 30  ***  2    
    return skip

def getFPS(cap):
    return cap.get(cv2.CAP_PROP_FPS)

def getNonZeroCount(frame,threshold = 10000):
    nonZeroCount = np.count_nonzero(frame)
    threshold = cap.get(3) * cap.get(4) / 100
   
    return (nonZeroCount > threshold)
    

def frameVote(frameChecker, frameNumber):
    return (np.count_nonzero(frameChecker) > frameNumber //2 )

frameNumber = 9
frameChecker = np.zeros(frameNumber)
frameIdx = 0
textColor = (255, 255, 255)
textPosition = (100, 100)
# creating object
fgbg = cv2.createBackgroundSubtractorMOG2(history=120,detectShadows=True)

# capture frames from a camera
cap = cv2.VideoCapture(0)


fps = getFPS(cap)
print("fps = ",fps)
count = 0

while(1):
    # read frames
    ret, img = cap.read()

    
   
        
    #Gray conversion and noise reduction (smoothening)
    gray_frame=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)
        
    
    fgmask = fgbg.apply(gray_frame)


    if  count % 3 == 0 :
 
        frameChecker[frameIdx] = getNonZeroCount(fgmask,cap)

        if(frameVote(frameChecker, frameNumber)):
            cv2.putText(fgmask, 'Someones stealing your honey', textPosition
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
