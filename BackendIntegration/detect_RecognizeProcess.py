from Face_Detection import Face_Detection
from extendedLBPH_test import *

import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
directory = os.path.join(parentdir,"BackendIntegration")


# directory = os.path.join(parentdir,"BackendIntegration")
# sys.path.insert(0, directory)


def FaceDetectionProcess(faceProcessQueue,mainFaceProcessQueue):
    obj = Face_Detection(yolo=os.path.join(directory,"yolov4-tiny"))
    response = {"image":None,"found":False}

    while True:
        obj_to_detect = mainFaceProcessQueue.get()
        image = obj_to_detect["frame"]
        obj.search_img(image)
        if obj.found:
            # print(obj.boxes)
            # print(obj.classes)
            # obj.draw_bounding_boxes(image,show = True)
            imgs = obj.get_faces(image)
            # Here call face recognize
            for img in imgs:
                if img.shape[0] > 90 and img.shape[1] > 90:
                    faceName = recognise_face(img)
                    print(faceName)
            response = {"image":imgs,"found":True,"faceName":faceName}
            
        else:
            response = {"image":None,"found":False,"faceName":faceName}
            
        faceProcessQueue.put(response)            

            

