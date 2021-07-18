"""
    script to change names of images and txt 
"""


import os
import shutil
import random
from unicodedata import name
from tqdm import tqdm



root = "newLabel"



def change(label):
    
    """
    get names of images
    """
    all = os.listdir(root)
    all.sort()
    subs = ".jpg"
    images = [i for i in all if i.endswith(subs)]
    names = [i.replace(subs,'') for i in images if subs in i]
    number = len(all) // 2



    os.chdir("newLabel")

    for i , name in enumerate(tqdm(names),1):
        os.rename(name + ".txt",label + str(i) + ".txt") 
        os.rename(name + ".jpg",label + str(i) + ".jpg") 
        print( i , name)
 
label = "Knife"

change(label)

