import numpy as np
from skimage.exposure import rescale_intensity
from methods import apply_mask, findThrsh

class Thrsh:
    def __init__(self):
        pass
    
    def __call__(self, img, t=None, inv=False, ops=3):
        if inv:
            if t is not None:
                return (img < t).astype(np.uint8) * 255
            return (img < findThrsh(img)).astype(np.uint8) * 255
        if t is not None:
            if t == -1:
                vals = np.unique(img)
                if len(vals) <= ops:
                    val = vals[0]
                else:
                    val =  vals[-ops]
                    if val == 0:
                        val = vals[1]
                t = val
            return (img > t).astype(np.uint8) * 255
        return (img > findThrsh(img)).astype(np.uint8) * 255


class Add:
    def __init__(self):
        pass
    
    def __call__(self, *args, **kwargs):
        mask = kwargs.get('mask', None)
        img1 = args[0]
        if mask is not None:
            img1 = apply_mask(img1, mask)
        img = img1.astype(np.float).copy()
        for i in range(1, len(args)):
            img2 = args[i]
            if mask is not None:
                img2 = apply_mask(img2, mask)
            img += img2
        img = rescale_intensity(img, in_range=(0, 255))
        img = (img * 255).astype("uint8")
        return img


class Prod:
    def __init__(self):
        pass
    
    def __call__(self, img, a):
        img_ = img.copy().astype(np.float32)
        img_ *= a
        img_ = rescale_intensity(img_, in_range=(0, 255))
        img_ = (img_ * 255).astype("uint8")
        return img_


class SmoothedProd:
    def __init__(self):
        pass
    
    def __call__(self, *args):
        img = args[0]
        img_ = img.copy().astype(np.float32)
        for i in range(1, len(args)):
            a = args[i]
            img_ *= a
        min_img = np.min(img_)
        max_img = np.max(img_)
        img_ -= min_img
        img_ /= max_img - min_img + 1
        img_ = (img_ * 255).astype("uint8")
        return img_


class Sub:
    def __init__(self):
        pass
    
    def __call__(self, img1, img2, mask=None):
        if mask is not None:
            img1 = apply_mask(img1, mask)
            img2 = apply_mask(img2, mask)
        img = img1.astype(np.float).copy()
        img -= img2
        img = rescale_intensity(img, in_range=(0, 255))
        img = (img * 255).astype("uint8")
        return img


class SmoothedSub:
    def __init__(self):
        pass
    
    def __call__(self, img1, img2, mask=None):
        if mask is not None:
            img1 = apply_mask(img1, mask)
            img2 = apply_mask(img2, mask)
        img = img1.astype(np.float).copy()
        img -= img2
        min_img = np.min(img)
        max_img = np.max(img)
        img -= min_img
        img /= max_img - min_img + 1
        img = (img * 255).astype("uint8")
        return img


class SmoothedAdd:
    def __init__(self):
        pass
    
    def __call__(self, *args, **kwargs):
        mask = kwargs.get('mask', None)
        img1 = args[0]
        if mask is not None:
            img1 = apply_mask(img1, mask)
        img = img1.astype(np.float).copy()
        for i in range(1, len(args)):
            img2 = args[i]
            if mask is not None:
                img2 = apply_mask(img2, mask)
            img += img2
        min_img = np.min(img)
        max_img = np.max(img)
        img -= min_img
        img /= max_img - min_img + 1
        img = (img * 255).astype("uint8")
        return img    


class Invert:
    def __init__(self):
        pass
    
    def __call__(self, img, mask=None):
        img_ = 255 - img
        if mask is not None:
            img_ = apply_mask(img_, mask)
        return img_
    