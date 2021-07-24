"""
    Face detection and recognition process
"""

from Face_Detection import Face_Detection
from detect import Detect
from extendedLBPH_test import *

import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
directory = os.path.join(parentdir,"BackendIntegration")



def FaceDetectionProcess(faceProcessQueue,mainFaceProcessQueue):
    obj = Face_Detection(yolo=os.path.join(directory,"yolov4-tiny"))

    while True:
        obj_to_detect = mainFaceProcessQueue.get()

        if obj_to_detect["status"] == "face":
            image = obj_to_detect["frame"]
            faceName = None

            obj.search_img(image)
            if obj.found:
                # print(obj.boxes)
                # print(obj.classes)
                # obj.draw_bounding_boxes(image,show = True)
                imgs = obj.get_faces(image)
                # Here call face recognize
                for img in imgs:
                    if img.shape[0] > 5 and img.shape[1] > 5:
                        faceName = recognise_face(img)
                        # print(faceName , " during voting")
                        # cv2.imshow('face detection', img)
                        # cv2.waitKey(1)


                response = {"image":imgs,"found":True,"faceName":faceName}
                
            else:
                response = {"image":None,"found":False,"faceName":faceName}
                
            faceProcessQueue.put(response)


def FaceObjProcess(faceObjProcessQueue,mainFaceObjProcessQueue):
    response = {"image":None,"found":False}
    objD = Detect(yolo=os.path.join(directory,"yolov4"))

    while True:
        obj_to_detect = mainFaceObjProcessQueue.get()

        image = obj_to_detect["frame"]
        label = obj_to_detect["class"]
        objD.search_img(image)
        box = []
        classes = []
        if len(objD.classes) > 0:
            # some objects founded 
            if label in objD.classes:
                for idx, c in enumerate(objD.classes):
                    if c == label:
                        box.append(objD.boxes[idx])
                        classes.append(c)

        response = {"image":None,"found":False}
        if len(box) > 0:
            image = objD.draw_bounding_boxes(image, box ,classes)
                      
            response = {"image":image,"found":True}

        faceObjProcessQueue.put(response)            

                

