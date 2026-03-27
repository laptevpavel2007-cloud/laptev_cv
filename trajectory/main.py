import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

def centroid(labeled, label = 1):
    y, x = np.where(labeled == label)
    return np.mean(y), np.mean(x)

x_all = []
y_all = []
for i in range(100):
    image = np.load(f"./motion/out/h_{i}.npy")
    labeled = label(image)
    for j in range(1, np.max(labeled)+1):
        l = labeled == j
        y, x = centroid(l)
        x_all.append(x)
        y_all.append(y)

x_1 = []
y_1 = []
x_2 = []
y_2 = []
x_3 = []
y_3 = []
flag = 1
for i in range(len(x_all)):
    if flag == 1:
        x_1.append(x_all[i])
        y_1.append(y_all[i])
        flag += 1
    elif flag == 2:
        x_2.append(x_all[i])
        y_2.append(y_all[i])
        flag += 1 
    elif flag == 3:
        x_3.append(x_all[i])
        y_3.append(y_all[i])
        flag = 1

plt.plot(x_1, y_1, 'y-')
plt.plot(x_2, y_2, 'g-')
plt.plot(x_3, y_3, 'b-')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()
plt.show()

