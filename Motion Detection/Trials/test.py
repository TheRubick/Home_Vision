# importing libraries
import numpy as np
import cv2
  
# creating object
#fgbg1 = cv2.createBackgroundSubtractorKNN(detectShadows=False)
fgbg2 = cv2.createBackgroundSubtractorMOG2(history=500,detectShadows=False)
#fgbg3 = cv2.bgsegm.createBackgroundSubtractorGMG(initializationFrames=120,decisionThreshold=0.8)
fgbg4 = cv2.bgsegm.createBackgroundSubtractorMOG(history=500)

# capture frames from a camera 
cap = cv2.VideoCapture(0)
while(1):
    # read frames
    ret, img = cap.read()
      
    # apply mask for background subtraction
    #fgmask1 = fgbg1.apply(img)
    fgmask2 = fgbg2.apply(img)
    #fgmask3 = fgbg3.apply(img)
    fgmask4 = fgbg4.apply(img)
    
      
    cv2.imshow('Original', img)
    #cv2.imshow('KNN', fgmask1)
    cv2.imshow('MOG2', fgmask2)
    #cv2.imshow('GMG', fgmask3)
    cv2.imshow('MOG', fgmask4)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
  
cap.release()
cv2.destroyAllWindows()