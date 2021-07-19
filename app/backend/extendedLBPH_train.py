from common import *
import face_recognition

def detectFaces(frame):
    small_frame = frame
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # Find all the facesimport face_recognition and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    return face_locations

def train_faces(label,images):
    training_data_hist1 = readList(fileName="train1.txt")
    training_data_hist2 = readList(fileName="train2.txt")
    labels1 = readLabeslFromFile("labels1.txt")
    labels2 = readLabeslFromFile("labels2.txt")
    for img in images:
        face_locations = detectFaces(img)
        for (top, right, bottom, left) in face_locations:
            test_img = img[top:bottom, left:right]
            image = cv2.cvtColor(test_img, cv2.COLOR_RGB2GRAY)
            dim = (198, 198)
            if  abs(left-right) <=160 or abs(top-bottom) <= 160:
                dim = (100,100)
            image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
            image = cv2.equalizeHist(image)
            image = extended_lbp(image, 1,8)
            image_grids = img_to_grid(image, x=7, y = 7)
            trainHist = calculate_weighted_hist(image_grids)
            if abs(left-right) <=160 or abs(top-bottom) <= 160:
                training_data_hist2.append(trainHist)
                labels2.append(label)
            else:
                training_data_hist1.append(trainHist)
                labels1.append(label)
    writeFile(fileName="train1.txt",l=training_data_hist1)
    writeFile(fileName="train2.txt",l=training_data_hist2)
    writeLabelsToFile(fileName='labels1.txt',l=labels1)
    writeLabelsToFile(fileName='labels2.txt',l=labels2)
    
        
        

