"""
    script to change labels of the images .txt 
"""


import os
import shutil
import random
from tqdm import tqdm



root = "Label"



def change(old_label, new_label):
    
    """
    get txt label files and replace old_label with new_label
    """
    all = os.listdir(root)
    subs = ".txt"
    alltxt = [i for i in all if i.endswith(subs)]

    os.chdir("Label")

    for txt in tqdm(alltxt):
        lines = []
        with open(txt) as f:
            for line in f:
                line = line.replace(old_label, new_label)
                lines.append(line)
        f.close()

        print(lines)

        os.chdir("..")
        os.chdir("newLabel")
        with open(txt, "w+") as outfile:
            for line in lines:
                outfile.write(line)
            outfile.close()
            os.chdir("..")
        os.chdir("Label")

old_label = "Kitchen knife"    
new_label = "Knife"

change(old_label,new_label)


# #read input file
# fin = open("data.txt", "rt")
# #read file contents to string
# data = fin.read()
# #replace all occurrences of the required string
# data = data.replace('pyton', 'python')
# #close the input file
# fin.close()
# #open the input file in write mode
# fin = open("data.txt", "wt")
# #overrite the input file with the resulting data
# fin.write(data)
# #close the file
# fin.close()