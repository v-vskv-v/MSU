import numpy as np
import sys
import cv2
from skimage.measure import label, regionprops
from PIL import Image
from methods import make_mask, multi_dil, defuse, kernels, apply_mask, addBrightness
from preprocess import adjust_gamma, applyCLAHEGray
from utils import cos, euc
from classes import (Thrsh, Invert, Add, Sub, Prod,
                     SmoothedAdd, SmoothedSub, SmoothedProd)


thrsh = Thrsh()
inv = Invert()
add = Add()
sub = Sub()
prod = Prod()
ssub = SmoothedSub()
sadd = SmoothedAdd()
sprod = SmoothedProd()


path = sys.argv[1]

img = np.asarray(Image.open(path))
layers = [img[:, :, i] for i in range(img.shape[2])]
labs = applyCLAHEGray(img)

mask = make_mask(layers, thrsh, sub)

label_im = label(mask)
regions = regionprops(label_im)

masks = []
bbox = []
cmasks = []
list_of_index = []
for num, x in enumerate(regions):
    area = x.area
    convex_area = x.convex_area
    if (convex_area / area < 1.15) and (convex_area / area > 0.95):
        masks.append(regions[num].convex_image)
        cmasks.append(list(map(int, x.centroid)))
        bbox.append(regions[num].bbox)   
        list_of_index.append(num)
count = len(masks)

print(count)

triangles = []
lab_triangles = []

for box, mask_ in zip(bbox, masks):
    red  =  layers[0][box[0] : box[2], box[1] : box[3]] * mask_
    green = layers[1][box[0] : box[2], box[1] : box[3]] * mask_
    blue  = layers[2][box[0] : box[2], box[1] : box[3]] * mask_
    image = np.dstack([red, green, blue])
    triangles.append(image)
    
    red  =  labs[0][box[0] : box[2], box[1] : box[3]] * mask_
    green = labs[1][box[0] : box[2], box[1] : box[3]] * mask_
    blue  = labs[2][box[0] : box[2], box[1] : box[3]] * mask_
    image = np.dstack([red, green, blue])
    lab_triangles.append(image)

full_masks = []
for M in range(len(triangles)):
    img_ = triangles[M]
    layers_ = [img_[:, :, i] for i in range(3)]
    labs_ = applyCLAHEGray(img_)
    
    blurred_ = cv2.medianBlur(triangles[M], 5)
    blurred_layers = [blurred_[:, :, i] for i in range(3)]
    wm = sprod(add(sub(blurred_layers[0], blurred_layers[1]), blurred_layers[2]),
               add(sub(blurred_layers[1], blurred_layers[2]), blurred_layers[0]),
               add(sub(blurred_layers[2], blurred_layers[0]), blurred_layers[1]))
    lmask = masks[M].astype(np.uint8) * 255
    delete = multi_dil(sub(multi_dil(lmask, kernels['morphc5']), lmask), kernels['morphc5'])
    full_masks.append(add(
        defuse(thrsh(sub(sadd(sub(cv2.GaussianBlur(wm, (7,7), 1), wm, masks[M]), sub(multi_dil(wm, kernels['morphc3'], 2), wm, masks[M])), delete), 128), kernels['morpht2'], kernels['morphc7']),
        defuse(thrsh(adjust_gamma(sub(layers_[1],layers_[0]), 5), -1, ops=50), kernels['morpht2'], kernels['morphs3']),
        defuse(thrsh(adjust_gamma(sub(labs_[2], sub(layers_[0], layers_[1]), sprod(adjust_gamma(layers_[0], 0.1), adjust_gamma(layers_[1], 0.1), layers_[2])), 2), 254), kernels['morphc3'], kernels['morphc5']),
        defuse(thrsh(add(sub(layers_[1],layers_[2]), sub(layers_[0],layers_[2]), mask=None), 254), kernels['morpht2'], kernels['morphc5']),
        defuse(apply_mask(inv(thrsh(add(adjust_gamma(sub(layers_[0],layers_[2]), 0.5), adjust_gamma(sub(layers_[0], layers_[1]), 0.5), adjust_gamma(sub(labs_[0], labs_[1]), 0.5), adjust_gamma(labs_[0], 0.5)), 20)), masks[M]), kernels['morpht2'], kernels['morphc5']),
        defuse(addBrightness(thrsh(adjust_gamma(add(sub(layers_[1],layers_[2]), sub(layers_[0],layers_[2]), mask=None), 0.5), 254), 255), kernels['morpht2'], kernels['morphc3']),
        defuse(apply_mask(inv(thrsh(sub(layers_[0],layers_[2]), 1)), masks[M]), kernels['morphc3'], kernels['morphc5']),
        defuse(apply_mask(thrsh(inv(add(sub(labs_[0], labs_[2]), sub(layers_[0], layers_[1]), mask=None)), 254), masks[M]), kernels['morphc3'], kernels['morphc3']),
        defuse(apply_mask(thrsh(add(sub(layers_[0], layers_[1]), sub(labs_[0], labs_[1])), 254), masks[M]), kernels['morpht2'], kernels['morphc5'])
                         ))

for i in range(len(masks)):
    mask_ = masks[i].astype(np.uint8) * 255
    cmask_ = cmasks[i]
    full_mask = full_masks[i].copy()

    label_m = label(mask_)
    reg_m = regionprops(label_m)
    cX, cY = map(int, reg_m[0].centroid)

    dst = cv2.cornerHarris(mask_, 2, 5, 0.04)

    x, y = np.where(dst>0.1*dst.max())
    pairs = np.asarray(list(zip(x, y)))
    norms = []
    C = np.array([cX, cY])

    for i in range(len(pairs)):
        norms.append(euc(pairs[i], C))
    norms = np.asarray(norms)
    idxs = np.argsort(norms)[::-1]
    dots = [pairs[idxs[0]]]
    i = 1
    thrsh_ = euc(dots[0], C) * np.sqrt(3) - 20

    while len(dots) < 3:
        fl = True
        for dot in dots:
            n = euc(pairs[idxs[i]], dot)
            if n <= thrsh_:
                fl = False
        if fl:
            dots.append(pairs[idxs[i]])
        i += 1

    dots = np.asarray(dots)

    label_d = label(full_mask)
    reg_d = regionprops(label_d)
    
    cnt_dots = np.zeros(3, dtype=np.int_)
    for i in range(len(reg_d)):
        x, y = map(int, reg_d[i].centroid)

        max_sim = 0
        max_i = -1
        for j in range(len(dots)):
            sim = cos(np.array([x, y], dtype=np.float32)-C,
                      dots[j].astype(np.float32)-C)
            if max_sim < sim:
                max_sim = sim
                max_i = j
        cnt_dots[max_i] += 1
    
    print(f'{cmask_[0]}, {cmask_[1]}; {", ".join(list(map(str, cnt_dots)))}')
