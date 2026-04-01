import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from scipy import ndimage
from skimage.io import imread
from pathlib import Path

save_path = Path(__file__).parent

def cnt_void(region):
    labeled = label(np.logical_not(region.image))
    bays = 0
    for r in regionprops(labeled):
        if r.area > 3:
            bays += 1
    return bays

def cnt_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0]+2, shape[1]+2))
    new_image[1:-1, 1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled)

def extractor(region):
    cy, cx = region.centroid_local
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]
    area_r = region.area / region.image.size
    perimeter = region.perimeter / region.image.size
    holes = cnt_holes(region)
    vlines = (np.sum(region.image, 0) == region.image.shape[1]).sum()
    hlines = (np.sum(region.image, 1) == region.image.shape[0]).sum()
    eccentricity = region.eccentricity
    aspect = region.image.shape[0]/region.image.shape[1]
    void = cnt_void(region)
    den = region.image.sum()/region.image.size
    vert_sym = np.mean(region.image == np.fliplr(region.image))
    horiz_sym = np.mean(region.image == np.flipud(region.image))
    orientation = region.orientation
    center_row = region.image[region.image.shape[0]//2, :]
    transitions = np.sum(np.diff(center_row.astype(int)) != 0)
    solidity = region.solidity
    row_std = np.std(np.sum(region.image, 1)) / region.image.shape[0]
    col_std = np.std(np.sum(region.image, 0)) / region.image.shape[1]

    return np.array([region.area/region.image.size, cy, cx, perimeter, holes, hlines, vlines, eccentricity, aspect, void, den, area_r, vert_sym, horiz_sym, orientation, transitions, solidity, row_std, col_std])

def classificator(region, tamplates):
    features = extractor(region)
    result = ""
    min_d = 10 ** 16
    for symbol, t in templates.items():
        d = ((t - features) ** 2).sum() ** 0.5
        if d < min_d:
            result = symbol
            min_d = d
    return result


image = imread("./alphabet-small.png")[:, :, :-1]
image = image.sum(2)
binary = image != 765

labeled = label(binary)
props = regionprops(labeled)

templates = {}
for region, symbol in zip(props, ["8", "O", "A", "B", "1", "W", "X", "*", "/", "-"]):
    templates[symbol] = extractor(region)

image2 = imread("./alphabet.png")[:, :, :-1]
abinary = image2.mean(2) > 0
alabeled = label(abinary)
apros = regionprops(alabeled)

result = {}
image_path = save_path/"out"
image_path.mkdir(exist_ok=True)

# plt.ion()
plt.figure(figsize=(5, 7))
for region in apros:
    symbol = classificator(region, templates)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1
    plt.cla()
    plt.title(f"Class - {symbol}")
    plt.imshow(region.image)
    plt.savefig(image_path/ f"image_{region.label}.png")


print(result)
plt.imshow(abinary)
plt.show()