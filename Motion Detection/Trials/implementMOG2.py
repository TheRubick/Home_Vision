'''
steps of the algorithm:

1- set the number of guassian mixture models and the other constants: Cthr, mahalanabolis distance, Cf, backgroundPortion
2- start with the first sample 
'''
import cv2

fgbg = cv2.createBackgroundSubtractorMOG2(history=500,detectShadows=False)
'''

MOG2 OPENCV Functions

'''
print("background ratio = ",fgbg.getBackgroundRatio())
print("Cthr = ",fgbg.getVarThreshold()) # related to the Cthr
print("var init = ",fgbg.getVarInit())
print("var max = ",fgbg.getVarMax())
fgbg.setVarThresholdGen(9)
print("var threshold generation = ",fgbg.getVarThresholdGen())
