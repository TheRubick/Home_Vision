import cv2
import numpy as np
from numpy.core.einsumfunc import _parse_possible_contraction
from numpy.core.fromnumeric import shape
from numpy.lib.function_base import extract
import fhog


def fftd(img, backwards=False):
    return cv2.dft(np.float32(img), flags=((cv2.DFT_INVERSE | cv2.DFT_SCALE) if backwards else cv2.DFT_COMPLEX_OUTPUT))

def real(x):
    return x[:,:,0]

def imag(x):
    return x[:,:,1]

def rearrange(img):
    assert(img.ndim == 2)
    _img = np.zeros(img.shape,np.dtype)
    x, y = img.shape[0] // 2, img.shape[1] // 2
    xs ,ys = img.shape[0] , img.shape[1]
    _img[0:x,0:y] , _img[x:xs,y:ys] = img[x:xs,y:ys] , img[0:x,0:y]
    _img[0:x,y:ys] , _img[x:xs,0:y] = img[x:xs,0:y] , img[0:x,y:ys]
    return _img

def limit(rect, limit):
    if(rect[0] + rect[2] > limit[0] + limit[2]):
        rect[2] = limit[0] + limit[2] - rect[0]
    if(rect[1] + rect[3] > limit[1] + limit[3]):
        rect[3] = limit[1] + limit[3] - rect[1]
    if(rect[0] < limit[0]):
        rect[2] -= (limit[0] - rect[0])
        rect[0] = limit[0]
    if(rect[1] < limit[1]):
        rect[3] -= (limit[1] - rect[1])
        rect[1] = limit[1]
    if(rect[2] < 0):
        rect[2] = 0
    if(rect[3] < 0):
        rect[3] = 0
    return rect

# recttools
def x2(rect):
    return rect[0] + rect[2]


def y2(rect):
    return rect[1] + rect[3]

def complexDivision(a, b):
    res = np.zeros(a.shape, a.dtype)
    divisor = 1. / (b[:, :, 0]**2 + b[:, :, 1]**2)

    res[:, :, 0] = (a[:, :, 0] * b[:, :, 0] + a[:, :, 1] * b[:, :, 1]) * divisor
    res[:, :, 1] = (a[:, :, 1] * b[:, :, 0] + a[:, :, 0] * b[:, :, 1]) * divisor
    return res

def complexMultiplication(a, b):
    res = np.zeros(a.shape,a.dtype)

    res[:, :, 0] = a[:, :, 0] * b[:, :, 0] - a[:, :, 1] * b[:, :, 1] 
    res[:, :, 1] = a[:, :, 1] * b[:, :, 0] + a[:, :, 0] * b[:, :, 1]
    return res

def getBorder(original, limited):
    res = [0, 0, 0, 0]
    res[0] = limited[0] - original[0]
    res[1] = limited[1] - original[1]
    res[2] = x2(original) - x2(limited)
    res[3] = y2(original) - y2(limited)
    assert(np.all(np.array(res) >= 0))
    return res

def subwindow(img, window, borderType=cv2.BORDER_CONSTANT):
    cutWindow = [x for x in window]
    limit(cutWindow, [0, 0, img.shape[1], img.shape[0]])   # modify cutWindow
    assert(cutWindow[2] > 0 and cutWindow[3] > 0)
    border = getBorder(window, cutWindow)
    res = img[cutWindow[1]:cutWindow[1] + cutWindow[3], cutWindow[0]:cutWindow[0] + cutWindow[2]]

    if(border != [0, 0, 0, 0]):
        res = cv2.copyMakeBorder(res, border[1], border[3], border[0], border[2], borderType)
    return res

class ObjectTracker:
    
    def __init__(self,multiscale=True,fixed_window=False,hogFeature=False):
        """ 
            initialize the parameters required for the tracker as mentioned in 
            the "High-Speed Tracking with Kernelized Correlation Filters" paper
        """

        self.multiscale = multiscale
        self.fixed_window = fixed_window
        self.hogFeature = hogFeature
        
        if self.hogFeature:
            self.interp_factor = 0.02
            self.kernel_sigma = 0.6
            self.cell_size = 4
            self.hogOrientations = 9
        else:
            self.grayFeature = True
            self.interp_factor = 0.075
            self.kernel_sigma = 0.2
            self.cell_size = 1
        
        if(self.multiscale):
            self.templateSize = 96
            self.scaleStep = 1.05 
            self.scaleWeight = 0.96
        elif(self.fixed_window):
            self.templateSize = 96
            self.scaleStep = 1
        else:
            self.templateSize = 1
            self.scaleStep = 1

        self.lamda = 0.0001
        self.padding = 2.5
        self.output_sigma_factor = 0.125
        
        self.desiredResponse = None
        self.modelAlpha  = None
        self.modelTemplate = None
        self.hannInit = None

        self.modelTemplateSize = [0, 0]
        self.scale = 1.0
        self.targetPatchSize = [0, 0, 0]
        self.roi = [0., 0., 0., 0.]

    def init(self,roi,image):
        """ 
            this function should be used on the first frame only
            initialize the desiredResponse,train model,extract the roi features
        """
        self.roi = list(map(float,roi))
        assert(roi[2] > 0 and roi[3] > 0)
        self.modelTemplate = self.getFeatures(image,1)
        self.desiredResponse = self.gaussianPeak(self.targetPatchSize[0],self.targetPatchSize[1])
        self.modelAlpha = np.zeros((self.targetPatchSize[0],self.targetPatchSize[1],2),np.float32)
        print(self.modelTemplate)
        self.train(self.modelTemplate,1.0)

    def createGaussianPeak(self, sizey, sizex):
        syh, sxh = sizey / 2, sizex / 2
        output_sigma = np.sqrt(sizex * sizey) / self.padding * self.output_sigma_factor
        mult = -0.5 / (output_sigma * output_sigma)
        y, x = np.ogrid[0:sizey, 0:sizex]
        y, x = (y - syh)**2, (x - sxh)**2
        res = np.exp(mult * (y + x))
        return fftd(res)

    def update(self,image):
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

        self.roi[0] = cx - self.roi[2] / 2 + loc[0] * self.cell_size * self.scale
        self.roi[1] = cy - self.roi[3] / 2 + loc[1] * self.cell_size * self.scale

        if(self.roi[0] >= image.shape[1] - 1):
            self.roi[0] = image.shape[1] - 1
        if(self.roi[1] >= image.shape[0] - 1):
            self.roi[1] = image.shape[0] - 1
        if(self.roi[0] + self.roi[2] <= 0):
            self.roi[0] = -self.roi[2] + 2
        if(self.roi[1] + self.roi[3] <= 0):
            self.roi[1] = -self.roi[3] + 2
        assert(self.roi[2] > 0 and self.roi[3] > 0)

        features = self.getFeatures(image,0,1.0)
        self.train(features,self.interp_factor)
        return self.roi

    def subPixelPeak(self, left, center, right):
        divisor = 2 * center - right - left  # float
        return (0 if abs(divisor) < 1e-3 else 0.5 * (right - left) / divisor)
    
    def detect(self,z,x):
        k = fftd(self.gaussianCorrelation(z,x))
        res = real(fftd(self.complexMultiplication(k,self.modelAlpha),True))

        _, pv, _, pi = cv2.minMaxLoc(res)   # pv:float  pi:tuple of int
        p = [float(pi[0]), float(pi[1])]   # cv::Point2f, [x,y]  #[float,float]

        
        if(pi[0] > 0 and pi[0] < res.shape[1] - 1):
            p[0] += self.subPixelPeak(res[pi[1], pi[0] - 1], pv, res[pi[1], pi[0] + 1])
        if(pi[1] > 0 and pi[1] < res.shape[0] - 1):
            p[1] += self.subPixelPeak(res[pi[1] - 1, pi[0]], pv, res[pi[1] + 1, pi[0]])
        
        
        p[0] -= res.shape[1] / 2.
        p[1] -= res.shape[0] / 2.

        return p, pv

    def train(self,x,current_interp_factor):
        k = fftd(self.gaussianCorrelation(x,x))
        alphaNew = complexDivision(self.desiredResponse , (k + self.lamda))
        self.modelAlpha = (1 - current_interp_factor) * self.modelAlpha + current_interp_factor * alphaNew
        self.modelTemplate = (1 - current_interp_factor) * self.modelTemplate + current_interp_factor * x


    '''
    def getFeatures(self,image,initialHann,scaleAdjust=1.0):
        extractedRoi = [0, 0, 0, 0]
        cx = self.roi[0] + self.roi[2] / 2
        cy = self.roi[1] + self.roi[3] / 2

        if(initialHann):
            paddedWidth = self.roi[2] * self.padding
            paddedHeight = self.roi[3] * self.padding

            if(self.templateSize > 1):
                scaleWH = max(paddedWidth,paddedHeight)
                self.scale = scaleWH / self.templateSize
                self.modelTemplateSize[0] = int(paddedWidth / self.scale)
                self.modelTemplateSize[1] = int(paddedHeight / self.scale)
            else:
                self.scale = 1.0
                self.modelTemplateSize[0] = int(paddedWidth)
                self.modelTemplateSize[1] = int(paddedHeight)

            if(self.hogFeature):
                self.modelTemplateSize[0] = int(self.modelTemplateSize[0]) // (2 * self.cell_size) * 2 * self.cell_size + 2 * self.cell_size
                self.modelTemplateSize[1] = int(self.modelTemplateSize[1]) // (2 * self.cell_size) * 2 * self.cell_size + 2 * self.cell_size
            else:
                self.modelTemplateSize[0] = int(self.modelTemplateSize[0]) // 2 * 2
                self.modelTemplateSize[1] = int(self.modelTemplateSize[1]) // 2 * 2

        extractedRoi[2] = int(self.scale * scaleAdjust * self.modelTemplateSize[0])
        extractedRoi[3] = int(self.scale * scaleAdjust * self.modelTemplateSize[1])
        extractedRoi[0] = int(cx - extractedRoi[0] / 2)
        extractedRoi[1] = int(cy - extractedRoi[1] / 2)

        z = subwindow(image,extractedRoi,cv2.BORDER_REPLICATE)

        if(z.shape[1] != self.modelTemplateSize[0] and z.shape[0] != self.modelTemplateSize[1]):
            z = cv2.resize(z,tuple(self.modelTemplateSize))

        if(self.hogFeature):
            mapp = {'sizeX': 0, 'sizeY': 0, 'numFeatures': 0, 'map': 0}
            mapp = fhog.getFeatureMaps(z, self.cell_size, mapp)
            mapp = fhog.normalizeAndTruncate(mapp, 0.2)
            mapp = fhog.PCAFeatureMaps(mapp)
            self.targetPatchSize = list(map(int, [mapp['sizeY'], mapp['sizeX'], mapp['numFeatures']]))
            featuresMap = mapp['map'].reshape((self.targetPatchSize[0] * self.targetPatchSize[1], self.targetPatchSize[2])).T   # (targetPatchSize[2], targetPatchSize[0]*targetPatchSize[1])
        else:
            if(z.ndim == 3 and z.shape[2] == 3):
                featuresMap = cv2.cvtColor(z,cv2.COLOR_RGB2GRAY)
            elif(z.ndim == 2):
                featuresMap = z

            featuresMap = featuresMap.astype(np.float32) / 255.0
            featuresMap -= 0.5
            self.targetPatchSize = [z.shape[0], z.shape[1], 1]
        
        if(initialHann):
            self.createHanningMats()
        
        featuresMap = self.hannInit * featuresMap

        return featuresMap

    '''
    def getFeatures(self, image, inithann, scale_adjust=1.0):
        extractedroi = [0, 0, 0, 0]  # [int,int,int,int]
        cx = self.roi[0] + self.roi[2] / 2  # float
        cy = self.roi[1] + self.roi[3] / 2  # float

        if(inithann):
            padded_w = self.roi[2] * self.padding
            padded_h = self.roi[3] * self.padding

            #bashof anhy el akbar fehom w b3d kda b3ml scale 3leh
            #3shan a3ml set lel template size ely ha5od mno el features
            if(self.templateSize > 1):
                if(padded_w >= padded_h):
                    self.scale = padded_w / float(self.templateSize)
                else:
                    self.scale = padded_h / float(self.templateSize)
                self.modelTemplateSize[0] = int(padded_w / self.scale)
                self.modelTemplateSize[1] = int(padded_h / self.scale)
            else:
                self.modelTemplateSize[0] = int(padded_w)
                self.modelTemplateSize[1] = int(padded_h)
                self.scale = 1.

            if(self.hogFeature):
                self.modelTemplateSize[0] = int(self.modelTemplateSize[0]) // (2 * self.cell_size) * 2 * self.cell_size + 2 * self.cell_size
                self.modelTemplateSize[1] = int(self.modelTemplateSize[1]) // (2 * self.cell_size) * 2 * self.cell_size + 2 * self.cell_size
            else:
                self.modelTemplateSize[0] = int(self.modelTemplateSize[0]) // 2 * 2
                self.modelTemplateSize[1] = int(self.modelTemplateSize[1]) // 2 * 2

        #hena bn7ded el features beta3t el extracted roi: el cx w el cy w el dimensions beta3tha
        extractedroi[2] = int(scale_adjust * self.scale * self.modelTemplateSize[0])
        extractedroi[3] = int(scale_adjust * self.scale * self.modelTemplateSize[1])
        extractedroi[0] = int(cx - extractedroi[2] / 2)
        extractedroi[1] = int(cy - extractedroi[3] / 2)

        #stretching the borders
        z = subwindow(image, extractedroi, cv2.BORDER_REPLICATE)
        #hena 3aksna 3shan el [1] fel z.shape hwa el width w el [0] hwa el height
        if(z.shape[1] != self.modelTemplateSize[0] or z.shape[0] != self.modelTemplateSize[1]):
            z = cv2.resize(z, tuple(self.modelTemplateSize))

        if(self.hogFeature):
            mapp = {'sizeX': 0, 'sizeY': 0, 'numFeatures': 0, 'map': 0}
            mapp = fhog.getFeatureMaps(z, self.cell_size, mapp)
            mapp = fhog.normalizeAndTruncate(mapp, 0.2)
            mapp = fhog.PCAFeatureMaps(mapp)
            self.targetPatchSize = list(map(int, [mapp['sizeY'], mapp['sizeX'], mapp['numFeatures']]))
            FeaturesMap = mapp['map'].reshape((self.targetPatchSize[0] * self.targetPatchSize[1], self.targetPatchSize[2])).T   # (targetPatchSize[2], targetPatchSize[0]*targetPatchSize[1])
        else:
            if(z.ndim == 3 and z.shape[2] == 3):
                FeaturesMap = cv2.cvtColor(z, cv2.COLOR_BGR2GRAY)   # z:(targetPatchSize[0], targetPatchSize[1], 3)  FeaturesMap:(targetPatchSize[0], targetPatchSize[1])   #np.int8  #0~255
            elif(z.ndim == 2):
                FeaturesMap = z  # (targetPatchSize[0], targetPatchSize[1]) #np.int8  #0~255
            FeaturesMap = FeaturesMap.astype(np.float32) / 255.0 - 0.5
            self.targetPatchSize = [z.shape[0], z.shape[1], 1]

        if(inithann):
            self.createHanningMats()  # createHanningMats need targetPatchSize

        FeaturesMap = self.hannInit * FeaturesMap
        return FeaturesMap


    def gaussianPeak(self,sizex,sizey):
        cx,cy = sizex / 2, sizey / 2
        outputSigma = (np.sqrt(sizex * sizey) / self.padding) * self.output_sigma_factor
        allOutputSigmas = -0.5 / (outputSigma * outputSigma)
        y , x = np.ogrid[0:sizey,0:sizex]
        y , x = (y - cy) ** 2, (x - cx) ** 2
        expr = np.exp((y+x) * allOutputSigmas)
        return fftd(expr)
    
    
    def gaussianCorrelation(self,u,v):
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
        dUV = np.exp(-dUV / (self.kernel_sigma * self.kernel_sigma))
        return dUV

    def createHanningMats(self):
        hann2t, hann1t = np.ogrid[0:self.targetPatchSize[0], 0:self.targetPatchSize[1]]

        hann1t = 0.5 * (1 - np.cos(2 * np.pi * hann1t / (self.targetPatchSize[1] - 1)))
        hann2t = 0.5 * (1 - np.cos(2 * np.pi * hann2t / (self.targetPatchSize[0] - 1)))
        hann2d = hann2t * hann1t

        if(self.hogFeature):
            hann1d = hann2d.reshape(self.targetPatchSize[0] * self.targetPatchSize[1])
            self.hannInit = np.zeros((self.targetPatchSize[2], 1), np.float32) + hann1d
        else:
            self.hannInit = hann2d
        self.hannInit = self.hannInit.astype(np.float32)
        