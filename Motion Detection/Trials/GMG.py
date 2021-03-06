import numpy as np
import cv2
  
cap = cv2.VideoCapture(0)
  
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
  
# initializing subtractor 
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG(initializationFrames=120,decisionThreshold=0.8)

  
while(1):
    ret, frame = cap.read()
  
    # applying on each frame
    fgmask = fgbg.apply(frame)
  
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)     
  
    cv2.imshow('frame', fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
  
cap.release()
cv2.destroyAllWindows()