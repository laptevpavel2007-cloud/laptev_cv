import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import opening
from skimage import morphology

image = np.load("./stars.npy")
labeled = label(image)

def area(labeled):
    return np.sum(labeled)

cnt_stars = 0
for i in range(1, np.max(labeled)+1):
    l = labeled == i
    old_area = area(l)
    l = opening(l, morphology.square(3))
    new_area = area(l)

    if (new_area/old_area) < 5/9:
        cnt_stars += 1

print("Количество звёздочек = ", cnt_stars)
plt.imshow(labeled)
plt.show()