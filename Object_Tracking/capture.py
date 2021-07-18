
import cv2

feedBack = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter("./test3.avi", fourcc, 20.0, (640,480))

while True:
    ret, frame = feedBack.read()
    out.write(frame)
    cv2.imshow('MOG 2', frame) #show on window
    if cv2.waitKey(1) & 0xFF == ord('q'): break #Exit when Q is pressed

feedBack.release()