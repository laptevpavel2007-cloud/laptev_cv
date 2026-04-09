import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.io import imread
from pathlib import Path

def cnt_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0]+2, shape[1]+2))
    new_image[1:-1, 1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled) - 1

def classificator(region):
    holes = cnt_holes(region)
    if holes == 2:
        vlines = (np.sum(region.image, 0) == region.image.shape[0]).sum()
        vlines = vlines/region.image.shape[1]
        if vlines > 0.2:
            return "B"
        else:
            return "8"
        
    elif holes == 1:
        vlines = (np.sum(region.image, axis=0) == region.image.shape[0]).sum()
        if vlines > 0:
            den = region.image.sum()/region.image.size
            if den > 0.5555:
                return "D"
            else:
                return "P"
        else:
            labeled = label(np.logical_not(region.image))
            bays = 0
            for r in regionprops(labeled):
                if r.area > 3:
                    bays += 1

            if bays == 4:
                return "A"
            elif bays == 5:
                return "O"   
    else:
        if region.image.sum()/region.image.size == 1.0:
            return "-"
        
        aspect = np.min(region.image.shape) / np.max(region.image.shape) 
        if aspect > 0.9:
            return "*"
        
        vlines = (np.sum(region.image, 0) == region.image.shape[0]).sum()
        hlines = (np.sum(region.image, 1) == region.image.shape[1]).sum()
        if vlines>0 and hlines>0:
            return "1"
        
        labeled = label(np.logical_not(region.image))
        bays = 0
        for r in regionprops(labeled):
            if r.area > 3:
                bays += 1

        if bays == 2:
            return "/"
        
        elif bays == 4:
            return "X"
        
        elif bays == 5:
            return "W"
    return "?"

save_path = Path(__file__).parent

image = imread("./symbols.png")[:, :, :-1]
abinary = image.mean(2) > 0
alabeled = label(abinary)
apros = regionprops(alabeled)

result = {}
image_path = save_path/"out"
image_path.mkdir(exist_ok=True)

plt.figure(figsize=(5, 7))
for region in apros:
    symbol = classificator(region)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1

    plt.cla()
    plt.title(f"Class - {symbol}")
    plt.imshow(region.image)
    plt.savefig(image_path/ f"image_{region.label}.png")

print(result)