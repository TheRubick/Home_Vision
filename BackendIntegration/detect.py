"""
class to detect different objects 

"""


import numpy as np
import time
import cv2
import os

class Detect:


    def __init__(self, yolo = "model", conf = 0.1, thres = 0.5):

        """
            initalize parameters of the detector
        """
        
        self.yolo = yolo  # yolo folder contain weights and model 

        self.conf = conf  # responsible for elimanting predications have confidence less than this value
        self.thres = thres # to remove overlapping predication consider area of intersection between similar items
        self.LABELS = None # labels we have
        self.COLORS = None # color for each label
        self.found = False
        self.classes = None
        self.boxes = None
       
        self.add_labels()

        self.net = self.load_model()

        
    def add_labels(self):
        """
         load classes labels and give each a color
        """
        # load the class labels our YOLO model was trained on
        labelsPath = os.path.sep.join([self.yolo,"obj.names"])
        LABELS = open(labelsPath).read().strip().split("\n")
        self.LABELS = LABELS

        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")
        self.COLORS = COLORS
        
    def load_model(self):
        """
        set model weight and configuration

        """

        iteration = "10000"
        weights = "yolov4-obj_{}.weights".format(iteration)

        modelsPath = "weights"

        # derive the paths to the YOLO weights and model configuration
        weightsPath = os.path.sep.join([self.yolo, os.path.join(modelsPath,weights)])
        configPath = os.path.sep.join([self.yolo, "yolov4-obj.cfg"])


        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

        return net

    def search_img(self, image):
        """
            search image for objects and set bounding boxes 
        """
    
        # load our input image and grab its spatial dimensions
        image = image #cv2.imread(image)
        (H, W) = image.shape[:2]
        # determine only the *output* layer names that we need from YOLO
        ln = self.net.getLayerNames()

        ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
            swapRB=True, crop=False) # scale image from 255.0 to 0 -> 1 and size 416 * 416 swapBR=True (since OpenCV uses BGR)
        self.net.setInput(blob)
        start = time.time()
        layerOutputs = self.net.forward(ln)
        end = time.time()


        # show timing information on YOLO
        # print("[INFO] YOLO took {:.6f} seconds".format(end - start))


        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.conf:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

                    # apply non-maxima suppression to suppress weak, overlapping bounding
                    # boxes

        idxs = cv2.dnn.NMSBoxes(boxes, confidences,self.conf,
        self.thres)

        if len(idxs) == 0:
            self.found = False
            self.boxes = []
            self.classes = []
            return
        else:
            self.found = True


        objects = idxs.flatten()

        self.boxes = [boxes[i] for i in objects]
        self.classes = np.take(classIDs, list(objects))

    def draw_bounding_boxes(self, image, boxes ,classes ,show = False):
        """
        draw box around detected objects
        """
        for i in range(len(classes)):
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            # draw a bounding box rectangle and label on the image
            # print(self.COLORS,classIDs)
            color = [int(c) for c in self.COLORS[classes[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}".format(self.LABELS[classes[i]])
            # print(text)
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, color, 2)
        
        if show:
            cv2.imshow("Image", image)
            cv2.waitKey(0)
        else:
            return image





