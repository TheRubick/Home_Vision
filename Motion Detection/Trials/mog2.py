# importing libraries
import numpy as np
import cv2
  
# creating object
fgbg = cv2.createBackgroundSubtractorMOG2(history=120,detectShadows=True)


# capture frames from a camera  
cap = cv2.VideoCapture(0)
while(1):
    # read frames
    ret, img = cap.read()

    #Gray conversion and noise reduction (smoothening)
    gray_frame=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)
      
  
    fgmask = fgbg.apply(gray_frame)
 
    
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

    cv2.imshow('Original', img)
    cv2.imshow('MOG2', fgmask)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
  
cap.release()
cv2.destroyAllWindows()