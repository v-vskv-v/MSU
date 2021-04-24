import numpy as np
import cv2
from utils import create_circle, create_chess
from skimage.morphology import opening, area_closing
from itertools import product


kernels = {
    'kirsh1': np.array([[5,5,5],[-3,0,-3],[-3,-3,-3]]),
    'kirsh2': np.array([[-3,5,5],[-3,0,5],[-3,-3,-3]]),
    'kirsh3': np.array([[-3,-3,5],[-3,0,5],[-3,-3,5]]),
    'kirsh4': np.array([[-3,-3,-3],[-3,0,5],[-3,5,5]]),
    'kirsh5': np.array([[-3,-3,-3],[-3,0,-3],[5,5,5]]),
    'kirsh6': np.array([[-3,-3,-3],[5,0,-3],[5,5,-3]]),
    'kirsh7': np.array([[5,-3,-3],[5,0,-3],[5,-3,-3]]),
    'kirsh8': np.array([[5,5,-3],[5,0,-3],[-3,-3,-3]]),
    'laplasian': np.array([[0,1,0],[1,-4,1],[0,1,0]], dtype=np.uint8),
    'border3': np.array([[0,3,0],[3,-3,3],[0,3,0]], dtype=np.uint8),
    'border5': np.array([[-5,-5,3,-5,-5],
                          [-5,3,-3,3,-5],
                          [3,-3,-3,-3,1],
                          [-5,3,-3,-3,3],
                          [-5,-5,3,-3,-5]], dtype=np.uint8),
    'misborder3' : np.array([[5,-3,5],[-3,3,-3],[5,-3,5]], dtype=np.uint8),
    'misborder5' : np.array([[5,5,-3,5,5],
                             [5,-3,3,-3,5],
                             [-3,3,3,3,-3],
                             [5,-3,3,-3,5],
                             [5,5,-3,5,5]], dtype=np.uint8),
    'prewitt1': np.array([[-1,-1,-1],[0,0,0],[1,1,1]],dtype=np.uint8),
    'prewitt2': np.array([[-1,0,1],[-1,0,1],[-1,0,1]],dtype=np.uint8),
    'chess3': create_chess(3),
    'chess5': create_chess(5),
    'morphs2': np.full((2, 2), 1),
    'morphs3': np.full((3, 3), 1),
    'morphs5': np.full((5, 5), 1),
    'morphs7': np.full((7, 7), 1),
    'morphc11': create_circle(11),
    'morphc9': create_circle(9),
    'morphc7': create_circle(7),
    'morphc5': create_circle(5),
    'morphc3': create_circle(3),
    'morpht2': np.array([[0,1,0],
                         [1,1,1]],
                        dtype=np.uint8),
    'morpht3': np.array([[0,1,0],
                         [0,1,0],
                         [1,1,1,]],
                        dtype=np.uint8),
    'morpht5': np.array([[0,0,1,0,0],
                         [0,1,1,1,0],
                         [0,1,1,1,0],
                         [1,1,1,1,1],
                         [1,1,1,1,1]],
                        dtype=np.uint8),
    'morpht7': np.array([[0,0,0,1,0,0,0],
                         [0,0,1,1,1,0,0],
                         [0,1,1,1,1,1,0],
                         [1,1,1,1,1,1,1],
                         [1,1,1,1,1,1,1]],dtype=np.uint8),
    'morpht9': np.array([[0,0,0,0,1,0,0,0,0],
                         [0,0,0,1,1,1,0,0,0],
                         [0,0,1,1,1,1,1,0,0],
                         [0,1,1,1,1,1,1,1,0],
                         [1,1,1,1,1,1,1,1,1]],dtype=np.uint8),
    'morpht11': np.array([[0,0,0,0,0,1,0,0,0,0,0],
                         [0,0,0,0,1,1,1,0,0,0,0],
                         [0,0,0,1,1,1,1,1,0,0,0],
                         [0,0,1,1,1,1,1,1,1,0,0],
                         [0,1,1,1,1,1,1,1,1,1,0],
                         [1,1,1,1,1,1,1,1,1,1,1]],dtype=np.uint8)
}


def convolve(image, kernel):
    (iH, iW) = image.shape[:2]
    (kH, kW) = kernel.shape[:2]
    pad = (kW - 1) // 2
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad,
                               cv2.BORDER_REPLICATE)
    output = np.zeros((iH, iW), dtype="float32")
    for y in np.arange(pad, iH + pad):
        for x in np.arange(pad, iW + pad):
            roi = image[y-pad : y+pad+1, x-pad : x+pad+1]
            k = (roi * kernel).sum()
            output[y-pad, x-pad] = k

    # rescale the output image to be in the range [0, 255]
    output = rescale_intensity(output, in_range=(0, 255))
    
    output = (output * 255).astype("uint8")
    return output


def findThrsh(img):
    H = np.bincount(img.ravel())
    k = np.arange(H.size)
    S_max = (H * k).sum()
    R_max = H.sum()
    S = 0
    R = 0
    for p in range(1, H.size):
        S += k[p] * H[p]
        R += H[p]
        if R == 0:
            continue
        D1 = S / R
        D2 = (S_max - S) / (R_max - R)
        if D1 + D2 - 2 * p <= 0:
            return p
    return H.size // 2


def addBrightness(image, thrsh, size=3):
    image_ = image[:]
    max_val = np.max(image)
    if max_val >= thrsh:
        step = size // 2
        shapes = image.shape
        for i, j in zip(*np.where(image_ == max_val)):
            idxs = np.asarray(list(product(np.arange(max(i-step, 0), min(i+step+1, shapes[0])),
                                           np.arange(max(j-step, 0), min(j+step+1, shapes[1])))))
            image_[idxs[:, 0], idxs[:, 1]] = 255
    return image_


def defuse(img, ker, reker, it=1, reit=1):
    img = cv2.erode(img, ker, iterations=it)
    img = cv2.dilate(img, reker, iterations=reit)
    return img


def refuse(img, ker, reker, it=1, reit=1):
    img = cv2.dilate(img, ker, iterations=it)
    img = cv2.erode(img, reker, iterations=reit)
    return img


def multi_dil(im, ker=kernels['morphs3'], it=1):
    im_ = im[:]
    for i in range(it):
        im_ = cv2.dilate(im_, ker)
    return im_


def multi_ero(im, ker=kernels['morphs3'], reit=1):
    im_ = im[:]
    for i in range(reit):
        im_ = cv2.erode(im_, ker)
    return im_


def make_mask(layers, thrsh, sub):
    masks = [thrsh(sub(layers[0], layers[1])),
             thrsh(sub(layers[1], layers[2]))]
    opened = []
    for mask in masks:
        multi_dilated = multi_dil(mask, kernels['morphc3'], 1)
        area_closed = area_closing(multi_dilated, 50000)
        multi_eroded = multi_ero(area_closed, kernels['morpht7'], 1)
        multi_eroded = multi_ero(area_closed, kernels['morpht5'], 1)
        multi_eroded = multi_ero(area_closed, kernels['morphs3'], 5)
        opened.append(opening(multi_eroded).astype(np.float32))
    opened = np.clip(np.sum(opened, axis=0), 0, 255).astype(np.uint8)
    return opened


def apply_mask(img, mask):
    img_ = np.zeros_like(img)
    img_[mask.astype(np.bool)] = img[mask.astype(np.bool)]
    return img_
