from skimage.morphology import remove_small_objects
import mss
import cv2
import pyautogui
import numpy as np
import time

monitor = {'top': 205, 'left': 500, 'width': 1000, 'height': 350}

pyautogui.FAILSAFE = False


x1 = 175
x2 = 320
y1 = 115
y2 = 175
max_exp = 130


x_b1 = 175
x_b2 = 260
y_b1 = 50
y_b2 = 115
max_exp_b = 50

go_x1 = 330
go_x2 = 650
go_y1 = 25
go_y2 = 80


fall_delay = 0.12       

time.sleep(3)

is_jumping = False
is_ducking = False
last_jump_time = 0.0
last_duck_time = 0.0
start_time = time.time()   
game_start_time = start_time

with mss.mss() as monic:
    while True:

        screenshot = monic.grab(monitor)
        frame = np.array(screenshot)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
        binary = remove_small_objects(binary > 0, min_size=20).astype(np.uint8) * 255

        current_time = time.time()
        delta = current_time - game_start_time
        speed_factor = 1.0 + (delta / 175.0)

        dynamic_x2 = x2 + int((speed_factor - 1.0) * max_exp)
        dynamic_x2 = min(dynamic_x2, monitor['width'] - 10)

        dynamic_x_b2 = x_b2 + int((speed_factor - 1.0) * max_exp_b) 
        dynamic_x_b2 = min(dynamic_x_b2, monitor['width'] - 10)   
      
        roi = binary[y1:y2, x1:dynamic_x2]
        aray = np.sum(roi) / 255.0
        
        if aray > 100 and (not is_jumping):
            pyautogui.press('space')
            is_jumping = True
            last_jump_time = current_time
            if is_ducking:
                pyautogui.keyUp('down')
                is_ducking = False


        roi2 = binary[y_b1:y_b2, x_b1:dynamic_x_b2]
        aray_b = np.sum(roi2) / 255.0

        if aray_b > 100 and (not is_ducking):
            pyautogui.keyDown('down')
            is_ducking = True
            last_duck_time = current_time
            time.sleep(0.08)
            pyautogui.keyUp('down')
            is_ducking = False


        if is_jumping and aray < 180 and (current_time - last_jump_time) > fall_delay:
            pyautogui.keyDown('down')
            time.sleep(0.01)
            pyautogui.keyUp('down')
            is_jumping = False
        
        if is_jumping and (current_time - last_jump_time) > 0.18 and aray < 50:
            is_jumping = False

        roi_go = binary[go_y1:go_y2, go_x1:go_x2]
        aray_go = np.sum(roi_go) / 255.0
        if aray_go > 300: 
            time.sleep(1.0)           
            pyautogui.press('space')  
            time.sleep(0.8)           

            game_start_time = time.time()
            is_jumping = False
            is_ducking = False
            last_jump_time = 0.0
            last_duck_time = 0.0
            continue

        cv2.rectangle(binary, (x1, y1), (dynamic_x2, y2), 255, 2)
        cv2.rectangle(binary, (x_b1, y_b1), (dynamic_x_b2, y_b2), 255, 2)
        cv2.rectangle(binary, (go_x1, go_y1), (go_x2, go_y2), 255, 2)

        cv2.imshow('T-Rex', binary)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        time.sleep(0.008)

cv2.destroyAllWindows()