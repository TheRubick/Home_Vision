import numpy as np
import cv2
import fhog
# ffttools

def fftd(img, backwards=False):
    # shape of img can be (m,n), (m,n,1) or (m,n,2)
    # in my test, fft provided by numpy and scipy are slower than cv2.dft
    return cv2.dft(np.float32(img), flags=((cv2.DFT_INVERSE | cv2.DFT_SCALE) if backwards else cv2.DFT_COMPLEX_OUTPUT))   # 'flags =' is necessary!


def real(img):
    return img[:, :, 0]


def imag(img):
    return img[:, :, 1]


def complexMultiplication(a, b):
    res = np.zeros(a.shape, a.dtype)

    res[:, :, 0] = a[:, :, 0] * b[:, :, 0] - a[:, :, 1] * b[:, :, 1]
    res[:, :, 1] = a[:, :, 0] * b[:, :, 1] + a[:, :, 1] * b[:, :, 0]
    return res


def complexDivision(a, b):
    res = np.zeros(a.shape, a.dtype)
    divisor = 1. / (b[:, :, 0]**2 + b[:, :, 1]**2)

    res[:, :, 0] = (a[:, :, 0] * b[:, :, 0] + a[:, :, 1] * b[:, :, 1]) * divisor
    res[:, :, 1] = (a[:, :, 1] * b[:, :, 0] + a[:, :, 0] * b[:, :, 1]) * divisor
    return res


def rearrange(img):
    # return np.fft.fftshift(img, axes=(0,1))
    assert(img.ndim == 2)
    img_ = np.zeros(img.shape, img.dtype)
    xh, yh = img.shape[1] // 2, img.shape[0] // 2
    #rearrange the diagonals
    img_[0:yh, 0:xh], img_[yh:img.shape[0], xh:img.shape[1]] = img[yh:img.shape[0], xh:img.shape[1]], img[0:yh, 0:xh]
    img_[0:yh, xh:img.shape[1]], img_[yh:img.shape[0], 0:xh] = img[yh:img.shape[0], 0:xh], img[0:yh, xh:img.shape[1]]
    return img_


# recttools
def x2(rect):
    return rect[0] + rect[2]


def y2(rect):
    return rect[1] + rect[3]


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


# KCF tracker
class KCFTracker:
    def __init__(self, hog=False, fixed_window=True, multiscale=False):
        """
        
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

        '''
            multiscale leha 3elaqa bel box eno yt3'yr swa2 2rbt 
        '''
        if(multiscale):
            self.templateSize = 96   # template size
            self.scaleStep = 1.05   # scale step for multi-scale estimation
            self.scaleWeight = 0.96   # to downweight detection scores of other scales for added stability
        elif(fixed_window):
            self.templateSize = 96
            self.scaleStep = 1
        else:
            self.templateSize = 1
            self.scaleStep = 1

        self.modelTemplateSize = [0, 0]  # cv::Size, [width,height]  #[int,int]
        self.roi = [0., 0., 0., 0.]  # cv::Rect2f, [x,y,width,height]  #[float,float,float,float]
        self.targetPatchSize = [0, 0, 0]  # [int,int,int]
        self.scale = 1.   # float
        self.modelAlpha = None  # numpy.ndarray    (size_patch[0], size_patch[1], 2)
        self.desiredResponse = None  # numpy.ndarray    (size_patch[0], size_patch[1], 2)
        self.modelTemplate = None  # numpy.ndarray    raw: (size_patch[0], size_patch[1])   hog: (size_patch[2], size_patch[0]*size_patch[1])
        self.hannInit = None  # numpy.ndarray    raw: (size_patch[0], size_patch[1])   hog: (size_patch[2], size_patch[0]*size_patch[1])

    def subPixelPeak(self, left, center, right):
        divisor = 2 * center - right - left  # float
        return (0 if abs(divisor) < 1e-3 else 0.5 * (right - left) / divisor)

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

    def createGaussianPeak(self, sizey, sizex):
        cy, cx = sizey / 2, sizex / 2
        output_sigma = (np.sqrt(sizex * sizey) / self.padding) * self.output_sigma_factor
        mult = -0.5 / (output_sigma * output_sigma)
        y, x = np.ogrid[0:sizey, 0:sizex]
        y, x = (y - cy)**2, (x - cx)**2
        res = np.exp((y + x) * mult)
        return fftd(res)

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
        dUV = np.exp(-dUV / (self.kernelSigma * self.kernelSigma))
        return dUV

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
                self.modelTemplateSize[0] = int(self.modelTemplateSize[0]) // (2 * self.cellSize) * 2 * self.cellSize + 2 * self.cellSize
                self.modelTemplateSize[1] = int(self.modelTemplateSize[1]) // (2 * self.cellSize) * 2 * self.cellSize + 2 * self.cellSize
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
            mapp = fhog.getFeatureMaps(z, self.cellSize, mapp)
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

    def detect(self, z, x):
        k = fftd(self.gaussianCorrelation(x, z))
        res = real(fftd(complexMultiplication((k),self.modelAlpha), True))

        _, pv, _, pi = cv2.minMaxLoc(res)   # pv:float  pi:tuple of int
        p = [float(pi[0]), float(pi[1])]   # cv::Point2f, [x,y]  #[float,float]

        
        if(pi[0] > 0 and pi[0] < res.shape[1] - 1):
            p[0] += self.subPixelPeak(res[pi[1], pi[0] - 1], pv, res[pi[1], pi[0] + 1])
        if(pi[1] > 0 and pi[1] < res.shape[0] - 1):
            p[1] += self.subPixelPeak(res[pi[1] - 1, pi[0]], pv, res[pi[1] + 1, pi[0]])
        
        
        p[0] -= res.shape[1] / 2.
        p[1] -= res.shape[0] / 2.

        return p, pv

    def train(self, x, train_interp_factor):
        k = self.gaussianCorrelation(x, x) #define the maximum response ely byb2a 3'aleban el target position
        alphaf = complexDivision(self.desiredResponse, fftd(k) + self.lambdar)

        self.modelTemplate = (1 - train_interp_factor) * self.modelTemplate + train_interp_factor * x
        self.modelAlpha = (1 - train_interp_factor) * self.modelAlpha + train_interp_factor * alphaf

    def init(self, roi, image):
        self.roi = list(map(float, roi))
        assert(roi[2] > 0 and roi[3] > 0)
        self.modelTemplate = self.getFeatures(image, 1)
        self.desiredResponse = self.createGaussianPeak(self.targetPatchSize[0], self.targetPatchSize[1])
        self.modelAlpha = np.zeros((self.targetPatchSize[0], self.targetPatchSize[1], 2), np.float32)
        self.train(self.modelTemplate, 1.0)

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

        features = self.getFeatures(image,0,1.0)
        self.train(features,self.interp_factor)
        return self.roi
