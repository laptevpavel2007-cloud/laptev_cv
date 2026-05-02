import numpy as np
import cv2
import random

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)

mouse_x, mouse_y = 0, 0

def on_mouse(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y

cv2.setMouseCallback("Image", on_mouse)

cam = cv2.VideoCapture(0)

lower_1 = None
upper_1 = None
lower_2 = None
upper_2 = None
lower_3 = None
upper_3 = None
clicked_1 = False
clicked_2 = False
clicked_3 = False
color_1 = None
color_2 = None
color_3 = None

def find_ball(hsv):
    global mouse_x, mouse_y
    color = hsv[mouse_y, mouse_x]
    lower = np.clip(color * 0.9, 0, 255).astype("u1")
    upper = np.clip(color * 1.1, 0, 255).astype("u1")
    return lower, upper, color

def show_ball(lower, upper, hsv, frame, color):

    if lower is None or upper is None:
        return
    inr = cv2.inRange(hsv, lower, upper)
    mask = cv2.morphologyEx(inr, cv2.MORPH_CLOSE, np.ones((5, 5), dtype="u1"))
    cv2.imshow("Mask", mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if radius > 10:
            x = int(x)
            y = int(y)
            radius = int(radius)
            cv2.circle(frame, (x, y), radius, cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_HSV2BGR)[0][0].tolist(), 4)
            cv2.circle(frame, (x, y), 5, cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_HSV2BGR)[0][0].tolist(), -1)
            if (cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_HSV2BGR)) not in my_list or len(my_list < 4):
                my_list.append(cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_HSV2BGR))

while cam.isOpened():
    ret, frame = cam.read()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    key = cv2.waitKey(1) & 0xFF

    my_list = []

    if key == ord('q'):
        break
    
    if key == ord('1'):
        lower_1, upper_1, color_1 = find_ball(hsv)

    if key == ord('2'):
        lower_2, upper_2, color_2 = find_ball(hsv)

    if key == ord('3'):
        lower_3, upper_3, color_3 = find_ball(hsv)

    show_ball(lower_1, upper_1, hsv, frame, color_1)
    show_ball(lower_2, upper_2, hsv, frame, color_2)
    show_ball(lower_3, upper_3, hsv, frame, color_3)

    random.shuffle(my_list)
    
    if len(my_list == 3):
        

    cv2.imshow("Image", frame)

cam.release()
cv2.destroyAllWindows()