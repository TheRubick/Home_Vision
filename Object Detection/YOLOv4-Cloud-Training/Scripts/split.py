"""
    to split dataset into training and validation datasets
"""

import os
import shutil
import random
from tqdm import tqdm
  
  


root = "/home/khaled/Desktop/Projects/GP/ObjectDetection/DataSetPrepartion/OIDv4_ToolKit/OID/Dataset/train"
subroot  = "/home/khaled/Desktop/Projects/GP/ObjectDetection/DataSetPrepartion/OIDv4_ToolKit/OID"



def getInfo():
    
    """
    get images number in each class and their files
    """
    classes = os.listdir(root)
    # classes = ["Hammer","Kitchen knife"]
    # test and train numbers
    train_test = {}
    class_images = {}

    for c in classes:
        print("-------------------{}-----------------------------------".format(c))
        allFiles = os.listdir(os.path.join(root,c))
        allFiles.sort()
        class_images [c] = allFiles
        totalNumber = len(allFiles) // 2    
        train = round(totalNumber * 0.8)
        test = totalNumber - train
        train_test[c] = (train, test)
        print(totalNumber , "  ",train , " ", test)
        print("-------------------------------------------------------")

    return train_test , class_images


def splitData():
    """
    divide images into training and testing
    """
    train_test , class_images = getInfo()

    # initializing substring
    subs = '.jpg'
  
    for c , files in tqdm(class_images.items()):
        # to get string with substring 
        images = [i.replace(subs,'') for i in files if subs in i]
        random.shuffle(images)

        # train_dir =  os.path.join(root,c,"train")
        train_dir =  os.path.join(subroot,"obj")
        try:
            os.mkdir(train_dir)
        except FileExistsError as exc:
            pass

        # test_dir =  os.path.join(root,c,"test")
        test_dir =  os.path.join(subroot,"test")
        try:
            os.mkdir(test_dir)
        except FileExistsError as exc:
            pass
        count = 0
        for image in images:
            if count < train_test[c][0]:
                count += 1
                # copy image and bounding box to train folder
                src = os.path.join(root, c, image + ".jpg")
                dst = os.path.join(train_dir, image + ".jpg")
                shutil.copy(src, dst)
                src = os.path.join(root, c, image + ".txt")
                dst = os.path.join(train_dir, image + ".txt")
                shutil.copy(src, dst)
            else:
                
                # copy image and bounding box to test folder
                src = os.path.join(root, c, image + ".jpg")
                dst = os.path.join(test_dir, image + ".jpg")
                shutil.copy(src, dst)
                src = os.path.join(root, c, image + ".txt")
                dst = os.path.join(test_dir, image + ".txt")
                shutil.copy(src, dst)



splitData()
