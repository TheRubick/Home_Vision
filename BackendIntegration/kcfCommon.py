import numpy as np
import cv2
import fhog
# ffttools

def fftd(img, backwards=False):
    """
    this function used to perform discrete fourier transform on the given input
    """
   
    return cv2.dft(np.float32(img), flags=((cv2.DFT_INVERSE | cv2.DFT_SCALE) if backwards else cv2.DFT_COMPLEX_OUTPUT)) 


def real(img):
    """
    function to return the real part of complex variable
    """
    return img[:, :, 0]


def imag(img):
    """
    function to return the imaginary part of complex variable
    """
    return img[:, :, 1]


def complexMultiplication(a, b):
    """
    function to perform complex multiplication
    """
    res = np.zeros(a.shape, a.dtype)

    res[:, :, 0] = a[:, :, 0] * b[:, :, 0] - a[:, :, 1] * b[:, :, 1]
    res[:, :, 1] = a[:, :, 0] * b[:, :, 1] + a[:, :, 1] * b[:, :, 0]
    return res


def complexDivision(a, b):
    """
    function to perform complex division
    """
    res = np.zeros(a.shape, a.dtype)
    divisor = 1. / (b[:, :, 0]**2 + b[:, :, 1]**2)

    res[:, :, 0] = (a[:, :, 0] * b[:, :, 0] + a[:, :, 1] * b[:, :, 1]) * divisor
    res[:, :, 1] = (a[:, :, 1] * b[:, :, 0] + a[:, :, 0] * b[:, :, 1]) * divisor
    return res


def rearrange(img):
    """
    function used to replace the quarters of the image on the image's diagonal
    """
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
    """
    ensure that bounding box after padding is still contained  
    rect is ROI   , limit ( 0,0,w,h)
    """
    if(rect[0] + rect[2] > limit[0] + limit[2]):  # remove extra postive padding 
        rect[2] = limit[0] + limit[2] - rect[0]
    if(rect[1] + rect[3] > limit[1] + limit[3]):
        rect[3] = limit[1] + limit[3] - rect[1]
    if(rect[0] < limit[0]):  # remove extra negative padding 
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
    """
    function used to get the subwindow of the image
    """
    cutWindow = [x for x in window]
    limit(cutWindow, [0, 0, img.shape[1], img.shape[0]])  
    assert(cutWindow[2] > 0 and cutWindow[3] > 0)
    border = getBorder(window, cutWindow)
    res = img[cutWindow[1]:cutWindow[1] + cutWindow[3], cutWindow[0]:cutWindow[0] + cutWindow[2]]  # get part from image surronded by bounding box

    if(border != [0, 0, 0, 0]):
        res = cv2.copyMakeBorder(res, border[1], border[3], border[0], border[2], borderType)
    return res
