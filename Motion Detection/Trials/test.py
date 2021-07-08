# importing libraries
import numpy as np
import cv2
  
# creating object
fgbg1 = cv2.createBackgroundSubtractorKNN(detectShadows=True)
fgbg2 = cv2.createBackgroundSubtractorMOG2(history=120)
fgbg3 = cv2.bgsegm.createBackgroundSubtractorGMG(initializationFrames=120,decisionThreshold=0.8)

# capture frames from a camera 
cap = cv2.VideoCapture(0)
while(1):
    # read frames
    ret, img = cap.read()

    #Gray conversion and noise reduction (smoothening)
    gray_frame=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)
      
    # apply mask for background subtraction
    fgmask1 = fgbg1.apply(gray_frame)
    fgmask2 = fgbg2.apply(gray_frame)
    fgmask3 = fgbg3.apply(gray_frame)
      
    cv2.imshow('Original', gray_frame)
    cv2.imshow('KNN', fgmask1)
    cv2.imshow('MOG2', fgmask2)
    cv2.imshow('GMG', fgmask3)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
  
cap.release()
cv2.destroyAllWindows()