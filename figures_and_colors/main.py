import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.io import imread
from skimage.color import rgb2hsv

image = imread("./balls_and_rects.png")
hsv = rgb2hsv(image)
hue = hsv[:, :, 0]
binary = hue > 0


def col(res, colors, hue, region):
    coords = region.coords
    mid_hue = hue[coords[:, 0], coords[:, 1]]
    color = np.mean(mid_hue)
    
    colors.append(color)
    colors = sorted(colors)

    while colors:
        val = colors.pop()              
        res[val] = res.get(val, 0) + 1
        deltas = []

        for color in colors:
            deltas.append((color, abs(val - color)))

        for key, value in deltas:           
            if value < 0.01:
                res[key] = res.get(key, 0) + 1  
                colors.remove(key)

res_cir = {}
colors_cir = []
res_cube = {}
colors_cube = []

labeled = label(binary)
for region in regionprops(labeled):
    
    area = region.area
    perimeter = region.perimeter

    circularity = (4 * np.pi * area) / (perimeter ** 2)
    
    if circularity > 0.85:
        col(res_cir, colors_cir, hue, region)

    else:
        col(res_cube, colors_cube, hue, region)

print("Оттенки кружков: ", res_cir)
print("Оттенки прямоугольников: ", res_cube)