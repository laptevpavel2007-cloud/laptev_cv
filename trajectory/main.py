import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

def centroid(labeled, label = 1):
    y, x = np.where(labeled == label)
    return np.mean(y), np.mean(x)

def distance(x1, x2, y1, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

x_1 = []
y_1 = []
x_2 = []
y_2 = []
x_3 = []
y_3 = []

image = np.load("./motion/out/h_0.npy")
labeled = label(image)
for j in range(1, np.max(labeled)+1):
    y, x = centroid(labeled, j)
    if y is not None and x is not None:
        if j == 1:
            y_1.append(y)
            x_1.append(x)
        elif j == 2:
            y_2.append(y)
            x_2.append(x)
        elif j == 3:
            y_3.append(y)
            x_3.append(x)


for i in range(1, 100):
    image = np.load(f"./motion/out/h_{i}.npy")
    labeled = label(image)

    for j in range(1, np.max(labeled)+1):
        y, x = centroid(labeled, j)

        dist = float('inf')
        dist1 = distance(x, x_1[-1], y, y_1[-1])
        if dist1 < dist and dist1 <= 20:
            dist = dist1
            index = 1
                    
        dist2 = distance(x, x_2[-1], y, y_2[-1])
        if dist2 < dist and dist2 <= 20:
            dist = dist2
            index = 2

        dist3 = distance(x, x_3[-1], y, y_3[-1])
        if dist3 < dist and dist3 <= 20:
            dist = dist3
            index = 3
                  
        if index == 1:
            y_1.append(y)
            x_1.append(x)
        elif index == 2:
            y_2.append(y)
            x_2.append(x)
        elif index == 3:
            y_3.append(y)
            x_3.append(x)

plt.plot(x_1, y_1, 'y-')
plt.plot(x_2, y_2, 'g-')
plt.plot(x_3, y_3, 'b-')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()
plt.show()

