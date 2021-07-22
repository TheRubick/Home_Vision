# from BackendIntegration.Face_Detection import Face_Detection
# from BackendIntegration.Face_Detection import Face_Detection
from common import *

import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
directory = os.path.join(parentdir,"BackendIntegration")
sys.path.insert(0, directory)

from Face_Detection import Face_Detection

obj = Face_Detection(yolo = os.path.join(directory,"yolov4-tiny"))


def detectFaces(frame):
     
    image = frame
    obj.search_img(image)

    if obj.found:
        # print(obj.boxes)
        # print(obj.classes)
        # # obj.draw_bounding_boxes(image,show = True)
        imgs = obj.get_faces(image)
    
        return imgs
    else:
        return []

   


def train_faces(label,images):
    training_data_hist1 = readList(fileName="train1.txt")
    training_data_hist2 = readList(fileName="train2.txt")
    labels1 = readLabeslFromFile("labels1.txt")
    labels2 = readLabeslFromFile("labels2.txt")
    for img in images:
        faces = detectFaces(img)
        print(faces)
        for test_img in faces:
            image = cv2.cvtColor(test_img, cv2.COLOR_RGB2GRAY)
            dim = (198, 198)
            if  image.shape[0] <=160 or image.shape[1] <= 160:
                dim = (100,100)
            image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
            image = cv2.equalizeHist(image)
            image = extended_lbp(image, 1,8)
            image_grids = img_to_grid(image, x=7, y = 7)
            trainHist = calculate_weighted_hist(image_grids)
            if image.shape[0] <=160 or image.shape[1] <= 160:
                training_data_hist2.append(trainHist)
                labels2.append(label)
            else:
                training_data_hist1.append(trainHist)
                labels1.append(label)
    writeFile(fileName="train1.txt",l=training_data_hist1)
    writeFile(fileName="train2.txt",l=training_data_hist2)
    writeLabelsToFile(fileName='labels1.txt',l=labels1)
    writeLabelsToFile(fileName='labels2.txt',l=labels2)
    
        
        

