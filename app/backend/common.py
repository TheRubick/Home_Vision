import cv2
import numpy as np
import os
# import matplotlib.pyplot as plt
import math 


def extended_lbp(src,r = 1,neighbours = 8):
    #output image
    result =np.zeros(src.shape,np.uint8)
    for n in range(neighbours):
        #sample points
        x = r* math.cos((2.0*math.pi*n)/neighbours)
        y = -1*r*math.sin((2.0*math.pi*n)/neighbours)
        #realtive indicies 
        fx = math.floor(x)
        fy = math.floor(y)
        cx = math.ceil(x)
        cy = math.ceil(y)
        #fractional part
        ty = y-fy
        tx = x-fx
        #interpolation weights
        w1 = (1-tx)*(1-ty)
        w2 = (tx)*(1-ty)
        w3 = (1-tx)*(ty)
        w4 = (tx)*(ty)
        for i in range(r,src.shape[0]-r):
            for j in range(r,src.shape[1]-r):
                t = w1*src[i+fy,j+fx] + w2*src[i+fy,j+cx] + w3*src[i+cy,j+fx] + w4*src[i+cy,j+cx]
                if t > src[i,j] or abs(t-src[i,j]) < 0.01:
                    #print(pow(2,n))
                    result[i,j] += pow(2,n)
    rows = result.shape[0]
    cols = result.shape[1]
    
    return result[1:rows-1,1:cols-1]

def img_to_grid(lbp_img, x=8, y=8):
    grid_imgs = []
    height = lbp_img.shape[0]
    width = lbp_img.shape[1]
    step_h = int(height/x)
    step_w = int(width/y)
    current_h = 0
    current_w = 0
    while current_h<height:
        while current_w<width:
            if current_h+step_h<=height and current_w+step_w<=width:
                #print("current h = ",current_h," current w = ",current_w)
                grid_imgs.append(lbp_img[current_h:current_h+step_h,current_w:current_w+step_w])
            current_w+=step_w
        current_w=0
        current_h+=step_h
    return grid_imgs

def calculate_hist(grid_imgs):
    final_hist = cv2.calcHist([grid_imgs[0]],[0],None,[256],[0,256],accumulate=False)
    final_hist /= final_hist.sum()
    #final_hist = cv2.normalize(final_hist, final_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    for img in grid_imgs[1:]:
        hist = cv2.calcHist([img],[0],None,[256],[0,256],accumulate=False)
        hist /= hist.sum()
        #hist = cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        final_hist = np.vstack((final_hist,hist))
    return final_hist
def load_images_from_folder(folderName):
    images = []
    labels = []
    for img in os.listdir(folderName):
        image = cv2.imread(os.path.join(folderName,img),cv2.IMREAD_COLOR)
        images.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        labels.append(img.split('-')[0])
    return images, labels

def load_labels(folderName):
    labels = []
    for img in os.listdir(folderName):
        labels.append(img.split('-')[0])
    return labels


def writeFile(fileName,l):
    dummy = open(fileName,"w+")
    for l2 in l:
        str1 = ""
        listLen = len(l2)
        for i in range(listLen):
            str1 += str(l2[i][0])
            if(i < listLen - 1):
                str1 += ","
        dummy.write(str1+"\n")
    dummy.close()


#reading training file
def readList(fileName):
    readFile = open(fileName)
    lists = readFile.readlines()
    bigL = []
    for l in lists:
        strL = l[:-1]
        strL = "".join(strL)
        strL = strL.split(",")
        smallL = []
        for i in strL:
            smallL.append([float(i)])
        bigL.append(np.array(smallL, dtype="float32"))
    readFile.close()
    return bigL
#remember could make training data hist global to save memory
def get_perfect_match(training_data_hist, test_hist, labels):
    min_dist = 65
    predicted_lbl = 'unknown'
    result_dist = []
    for i in range(len(training_data_hist)):
        #1 for chi square
        current_dist = cv2.compareHist(training_data_hist[i], test_hist, 1)
        result_dist.append((current_dist, labels[i]))
        if current_dist<min_dist:
            min_dist=current_dist
            predicted_lbl=labels[i]
#             print('min_dist = ', min_dist, 'label=', labels[i])
    #result_dist.sort(key = lambda x: x[0])
    #print(result_dist)
    print(min_dist)
    return predicted_lbl

    
def calculate_weighted_hist(grid_imgs):
    final_hist = cv2.calcHist([grid_imgs[0]],[0],None,[256],[0,256],accumulate=False)
    final_hist /= final_hist.sum()
    #final_hist = cv2.normalize(final_hist, final_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    j = 1
    for img in grid_imgs[1:]:
        hist = cv2.calcHist([img],[0],None,[256],[0,256],accumulate=False)
        hist /= hist.sum()
        if (7 <= j <= 9) or (11 <= j <= 16) or (18 <= j <= 20):
            hist *= 4
        if (j == 17) or ( 23 <= j <= 25 ):
            hist *=2
        if (37 <= j <= 39):
            hist *= 3
        if j in [28,34,35,41,42,49]:
            hist *= 0
        #hist = cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        final_hist = np.vstack((final_hist,hist))
        j+=1
    return final_hist

def writeLabelsToFile(fileName,l):
    dummy = open(fileName,"w+")
    for label in l:
        dummy.write(label+"\n")
    dummy.close()

def readLabeslFromFile(fileName):
    readFile = open(fileName)
    lists = readFile.readlines()
    labels = []
    for l in lists:
        labels.append(l.replace('\n',''))
    readFile.close()
    return labels
