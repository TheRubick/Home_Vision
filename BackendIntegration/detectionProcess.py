from numpy.lib.type_check import imag
from detect import Detect
import sys, os, inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
directory = os.path.join(parentdir,"BackendIntegration")

def objectDetectionProcess(detectionProcessQueue,mainProcessQueue):
    obj = Detect(yolo=os.path.join(directory,"yolov4"))

    while True:
        obj_to_detect = mainProcessQueue.get()
        image = obj_to_detect["frame"]
        label = obj_to_detect["class"]
        obj.search_img(image)
        box = []
        classes = []
        print(obj.classes)
        if len(obj.classes) > 0:
            # some objects founded 
            if label in obj.classes:
                for idx, c in enumerate(obj.classes):
                    if c == label:
                        box.append(obj.boxes[idx])
                        classes.append(c)

        response = {"image":None,"found":False}
        if len(box) > 0:
            image = obj.draw_bounding_boxes(image, box ,classes)
            response = {"image":image,"found":True}

        detectionProcessQueue.put(response)            

            

