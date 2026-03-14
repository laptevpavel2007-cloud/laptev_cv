from scipy.datasets import face
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import opening


struct = np.ones((3, 1))


for i in range(1, 7):
    image = np.load(f'./wires/wires{i}.npy')
    labeled_image = label(image)

    for j in range(1, np.max(labeled_image)+1):
        l = labeled_image == j
        process = opening(l, struct)
        labeled_process = label(process)
        if np.max(labeled_process) > 1:
            print(f'file-{i} провод-{j} разорван на {np.max(np.max(labeled_process))} кусочков')
        else:
            print(f'file-{i} провод-{j} цел')

        # plt.subplot(121)
        # plt.imshow(image)
        # plt.subplot(122)
        # plt.imshow(process)
        # plt.show()

