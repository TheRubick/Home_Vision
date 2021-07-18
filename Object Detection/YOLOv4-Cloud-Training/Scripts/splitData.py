"""
    to split dataset into n batches to preprocess and augment
"""
import os
import shutil
import random
from tqdm import tqdm
  
  


root = "Data"
# subroot  = "/home/khaled/Desktop/Projects/GP/ObjectDetection/DataSetPrepartion/OIDv4_ToolKit/OID"

def getInfo(nsplits):
    
    """
    get images number in each class and their files
    """
    classes = os.listdir(root)
    img_to_take = {}
    class_images = {}
    all_images = 0

    for c in classes:
        print("-------------------{}-----------------------------------".format(c))
        allFiles = os.listdir(os.path.join(root,c))
        allFiles.sort()
        class_images [c] = allFiles
        totalNumber = len(allFiles) // 2    
        all_images = all_images +  totalNumber
        img_to_take[c] = totalNumber // nsplits
        print(totalNumber)
    print(" we have {} images in all classes".format(all_images))
    print("we will take {} in each split------------------------".format(img_to_take))


    return class_images, img_to_take


def splitImages(nsplits):
    """
    create folders and split el images
    """
    folder_names = [ "data" + str(i+1) for i in range(nsplits)]
    for i in range(nsplits):
        try:
            os.mkdir(folder_names[i])
        except FileExistsError as exc:
            pass
    
    class_images , img_to_take = getInfo(nsplits)

    subs = ".jpg"
    for c , files in tqdm(class_images.items()):
        print("for class {}".format(c))
        # to get string with substring 
        images = [i.replace(subs,'') for i in files if subs in i]
        random.shuffle(images)

        count = 1
        folderNumber = 0
        total_in_folder = 0
        for image in images:
            if count % img_to_take[c] == 0:
                # print("{} has {} images".format(folder_names[folderNumber] , total_in_folder))
                folderNumber += 1
                total_in_folder = 0
               
            if folderNumber == nsplits:
                folderNumber -= 1

            # copy image and bounding box to folder
            src = os.path.join(root, c, image + ".jpg")
            dst = os.path.join(folder_names[folderNumber], image + ".jpg")
            shutil.copy(src, dst)

            src = os.path.join(root, c, image + ".txt")
            dst = os.path.join(folder_names[folderNumber], image + ".txt")
            shutil.copy(src, dst)
            count += 1
            total_in_folder +=1
        # print("******************{}**************************".format(count))
        



splitImages(8)