import numpy as np
import cv2
import fhog
from kcfCommon import *

# KCF tracker
class KCFTracker:
    def __init__(self, hog=False, fixed_window=True, multiscale=False):
        """
        initializing the KCF tracker attributes       
        """
        self.lambdar = 0.0001
        self.padding = 2.5
        self.output_sigma_factor = 0.125

        if(hog):
            self.interp_factor = 0.012
            self.kernelSigma = 0.6
            self.cellSize = 4
            self.hogFeature = True
        else:
            self.interp_factor = 0.075
            self.kernelSigma = 0.2
            self.cellSize = 1
            self.hogFeature = False

        if(multiscale):
            self.templateSize = 96   # template size
            self.scaleStep = 1.05   # scale step for multi-scale estimation
            self.scaleWeight = 0.96   # to downweight detection scores of other scales for added stability
        elif(fixed_window):
            self.templateSize = 96
            self.scaleStep = 1
       

        self.modelTemplateSize = [0, 0]
        self.roi = [0., 0., 0., 0.]
        self.targetPatchSize = [0, 0, 0]
        self.scale = 1.
        self.modelAlpha = None  
        self.desiredResponse = None  
        self.modelTemplate = None
        self.hannInit = None

    def subPixelPeak(self, left, center, right):
        divisor = 2 * center - right - left
        return (0 if abs(divisor) < 1e-3 else 0.5 * (right - left) / divisor)

    def createHanningMats(self):
        """
        function to create hanning matrix
        """
        hann2t, hann1t = np.ogrid[0:self.targetPatchSize[0], 0:self.targetPatchSize[1]]

        # create 2 cosine wave for create hanning window 

        hann1t = 0.5 * (1 - np.cos(2 * np.pi * hann1t / (self.targetPatchSize[1] - 1)))
        hann2t = 0.5 * (1 - np.cos(2 * np.pi * hann2t / (self.targetPatchSize[0] - 1)))
        hann2d = hann2t * hann1t

        if(self.hogFeature):
            hann1d = hann2d.reshape(self.targetPatchSize[0] * self.targetPatchSize[1])
            self.hannInit = np.zeros((self.targetPatchSize[2], 1), np.float32) + hann1d
        else:
            self.hannInit = hann2d
        self.hannInit = self.hannInit.astype(np.float32)

    def createGaussianPeak(self, sizey, sizex):
        """
        function to create gaussian peak for the desired response
        f(x) = 1 / simga sqrt(2PI) * exp(-0.5/simga^2 * (x-mean)^2)
        """
        cy, cx = sizey / 2, sizex / 2
        output_sigma = (np.sqrt(sizex * sizey) / self.padding) * self.output_sigma_factor
        mult = -0.5 / (output_sigma * output_sigma)
        y, x = np.ogrid[0:sizey, 0:sizex]
        y, x = (y - cy)**2, (x - cx)**2
        res = np.exp((y + x) * mult)
        return fftd(res)

    def gaussianCorrelation(self,u,v):
        """
        function to retrieve the gaussian correlation of two variables
        """
        if(self.hogFeature):
            uv = np.zeros((self.targetPatchSize[0], self.targetPatchSize[1]), np.float32)
            for i in range(self.targetPatchSize[2]):
                uaux = u[i, :].reshape((self.targetPatchSize[0], self.targetPatchSize[1]))
                vaux = v[i, :].reshape((self.targetPatchSize[0], self.targetPatchSize[1]))
                uvaux = cv2.mulSpectrums(fftd(uaux), fftd(vaux), 0, conjB=True)
                uvaux = real(fftd(uvaux, True))
                uv += uvaux
            uv = rearrange(uv)
        else:
            uv = cv2.mulSpectrums(fftd(u),fftd(v),0,conjB=True)
            uv = fftd(uv,True)
            uv = real(uv)
            uv = rearrange(uv)

        if(u.ndim == 3 and v.ndim == 3):
            dUV = (np.sum(real(u) ** 2) + np.sum(real(v) ** 2) - 2.0 * uv) / (self.targetPatchSize[0] * self.targetPatchSize[1] * self.targetPatchSize[2]) 
        elif(u.ndim == 2 and v.ndim == 2):
            dUV = (np.sum(u*u) + np.sum(v*v) - 2.0 * uv) / (self.targetPatchSize[0] * self.targetPatchSize[1] * self.targetPatchSize[2])

        dUV = dUV * (dUV >= 0)
        dUV = np.exp(-dUV / (self.kernelSigma * self.kernelSigma))
        return dUV

    def getFeatures(self, image, inithann, scale_adjust=1.0):
        """
        function to extract the features of the roi "region of interest" whether fhog or gray features
        """
        extractedroi = [0, 0, 0, 0]  
        cx = self.roi[0] + self.roi[2] / 2  # float
        cy = self.roi[1] + self.roi[3] / 2  # float

        if(inithann):
            padded_w = self.roi[2] * self.padding
            padded_h = self.roi[3] * self.padding

            if(self.templateSize > 1):
                if(padded_w >= padded_h):
                    self.scale = padded_w / float(self.templateSize)
                else:
                    self.scale = padded_h / float(self.templateSize)
                self.modelTemplateSize[0] = int(padded_w / self.scale)
                self.modelTemplateSize[1] = int(padded_h / self.scale)
          

            if(self.hogFeature):
                self.modelTemplateSize[0] = int(self.modelTemplateSize[0]) + 2 * self.cellSize
                self.modelTemplateSize[1] = int(self.modelTemplateSize[1]) + 2 * self.cellSize
    
        
        extractedroi[2] = int(scale_adjust * self.scale * self.modelTemplateSize[0])
        extractedroi[3] = int(scale_adjust * self.scale * self.modelTemplateSize[1])
        extractedroi[0] = int(cx - extractedroi[2] / 2)
        extractedroi[1] = int(cy - extractedroi[3] / 2)

        #stretching the borders
        z = subwindow(image, extractedroi, cv2.BORDER_REPLICATE)
        
        if(z.shape[1] != self.modelTemplateSize[0] or z.shape[0] != self.modelTemplateSize[1]):
            z = cv2.resize(z, tuple(self.modelTemplateSize))

        if(self.hogFeature):
            mapp = {'sizeX': 0, 'sizeY': 0, 'numFeatures': 0, 'map': 0}
            mapp = fhog.getFeatureMaps(z, self.cellSize, mapp) # calculate histogram of gradient for every cell we get 9 bins 
            mapp = fhog.normalizeAndTruncate(mapp, 0.2)
            mapp = fhog.PCAFeatureMaps(mapp)  # 2 steps used to reduce number of features from 36 to 13 feature
            self.targetPatchSize = list(map(int, [mapp['sizeY'], mapp['sizeX'], mapp['numFeatures']]))
            FeaturesMap = mapp['map'].reshape((self.targetPatchSize[0] * self.targetPatchSize[1], self.targetPatchSize[2])).T
        else:
            if(z.ndim == 3 and z.shape[2] == 3):
                FeaturesMap = cv2.cvtColor(z, cv2.COLOR_BGR2GRAY)
            elif(z.ndim == 2):
                FeaturesMap = z
            FeaturesMap = FeaturesMap.astype(np.float32) / 255.0 - 0.5
            self.targetPatchSize = [z.shape[0], z.shape[1], 1]

        if(inithann):
            self.createHanningMats()

        FeaturesMap = self.hannInit * FeaturesMap
        return FeaturesMap

    def detect(self, z, x):
        """
        function to detect the location of the bounding box
        """
        k = fftd(self.gaussianCorrelation(x, z)) # corrleation between prev batch and current batch
        res = real(fftd(complexMultiplication((k),self.modelAlpha), True))

        _, pv, _, pi = cv2.minMaxLoc(res)   # pv -> max val   pi ->  pos of max val
        p = [float(pi[0]), float(pi[1])]  #  xy coord of maximum value

        
        if(pi[0] > 0 and pi[0] < res.shape[1] - 1):
            # average value in case point is out boundry
            p[0] += self.subPixelPeak(res[pi[1], pi[0] - 1], pv, res[pi[1], pi[0] + 1])
        if(pi[1] > 0 and pi[1] < res.shape[0] - 1):
            p[1] += self.subPixelPeak(res[pi[1] - 1, pi[0]], pv, res[pi[1] + 1, pi[0]])


        # get top left that will be added to the new point
        
        p[0] -= res.shape[1] / 2.0
        p[1] -= res.shape[0] / 2.0

        return p, pv

    def train(self, x, train_interp_factor):
        """
        function used to update the learning parameters "alpha"
        """
        k = self.gaussianCorrelation(x, x)
        alphaf = complexDivision(self.desiredResponse, fftd(k) + self.lambdar)

        self.modelTemplate = (1 - train_interp_factor) * self.modelTemplate + train_interp_factor * x
        self.modelAlpha = (1 - train_interp_factor) * self.modelAlpha + train_interp_factor * alphaf

    def init(self, roi, image):
        """
        this function is called only on the first frame
        """
        self.roi = list(map(float, roi))
        assert(roi[2] > 0 and roi[3] > 0)
        self.modelTemplate = self.getFeatures(image, 1)
        self.desiredResponse = self.createGaussianPeak(self.targetPatchSize[0], self.targetPatchSize[1])
        self.modelAlpha = np.zeros((self.targetPatchSize[0], self.targetPatchSize[1], 2), np.float32)
        self.train(self.modelTemplate, 1.0)

    def update(self,image):
        """
        this function is used to update the frames after the first frame have been initialized
        """
        if(self.roi[0] + self.roi[2] <= 0):
            self.roi[0] = -self.roi[2] + 1
        if(self.roi[1] + self.roi[3] <= 0):
            self.roi[1] = -self.roi[2] + 1
        if(self.roi[0] >= image.shape[1] - 1):
            self.roi[0] = image.shape[1] - 2
        if(self.roi[1] >= image.shape[0] - 1):
            self.roi[1] = image.shape[0] - 2
        
        cx = self.roi[0] + self.roi[2] / 2
        cy = self.roi[1] + self.roi[3] / 2

        loc, peakValue = self.detect(self.modelTemplate,self.getFeatures(image,0,1.0))

        if(self.scaleStep != 1):
            smallLoc , smallPeakValue = self.detect(self.modelTemplate,self.getFeatures(image,0,1.0/self.scaleStep))
            bigLoc , bigPeakValue = self.detect(self.modelTemplate,self.getFeatures(image,0,self.scaleStep))

            if((self.scaleWeight * smallPeakValue > peakValue) and (smallPeakValue > bigPeakValue)):
                loc = smallLoc
                self.scale /= self.scaleStep
                self.roi[2] /= self.scaleStep
                self.roi[3] /= self.scaleStep
            
            elif(self.scaleWeight * bigPeakValue > peakValue):
                loc = bigLoc
                self.scale *= self.scaleStep
                self.roi[2] *= self.scaleStep
                self.roi[3] *= self.scaleStep

        # move top left coordinate according to the max response

        self.roi[0] = cx - self.roi[2] / 2 + loc[0] * self.cellSize * self.scale
        self.roi[1] = cy - self.roi[3] / 2 + loc[1] * self.cellSize * self.scale

        if(self.roi[0] >= image.shape[1] - 1):
            self.roi[0] = image.shape[1] - 1
        if(self.roi[1] >= image.shape[0] - 1):
            self.roi[1] = image.shape[0] - 1
        if(self.roi[0] + self.roi[2] <= 0):
            self.roi[0] = -self.roi[2] + 2
        if(self.roi[1] + self.roi[3] <= 0):
            self.roi[1] = -self.roi[3] + 2
        assert(self.roi[2] > 0 and self.roi[3] > 0)

        # get features and train for the next frame 
        features = self.getFeatures(image,0,1.0)
        self.train(features,self.interp_factor)
        return self.roi