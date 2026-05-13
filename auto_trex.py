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
max_exp = 150


x_b1 = 175
x_b2 = 260
y_b1 = 50
y_b2 = 115


go_x1 = 330
go_x2 = 650
go_y1 = 25
go_y2 = 80


base_jump_t = 280
base_duck_t = 250


jump_cooldown = 0.1
duck_cooldown = 0.2      
fall_delay = 0.18        

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
        speed_factor = 1.0 + (delta / 200.0)

        dynamic_x2 = x2 + int((speed_factor - 1.0) * max_exp)
        dynamic_x2 = min(dynamic_x2, monitor['width'] - 10)

        dynamic_x_b2 = x_b2 + int((speed_factor - 1.0) * (max_exp * 0.8))
        dynamic_x_b2 = min(dynamic_x_b2, monitor['width'] - 10)

        jump_threshold = base_jump_t * (0.8 + 0.2 / speed_factor)
        duck_threshold = base_duck_t * (0.8 + 0.2 / speed_factor)


        roi = binary[y1:y2, x1:dynamic_x2]
        aray = np.sum(roi) / 255.0
        
        if aray > jump_threshold and (not is_jumping) and (current_time - last_jump_time > jump_cooldown):
            pyautogui.press('space')
            is_jumping = True
            last_jump_time = current_time
            if is_ducking:
                pyautogui.keyUp('down')
                is_ducking = False


        roi2 = binary[y_b1:y_b2, x_b1:dynamic_x_b2]
        aray_b = np.sum(roi2) / 255.0

        if aray_b > duck_threshold and (not is_ducking) and (current_time - last_duck_time > duck_cooldown) and (not is_jumping):
            pyautogui.keyDown('down')
            is_ducking = True
            last_duck_time = current_time
            time.sleep(0.08)
            pyautogui.keyUp('down')
            is_ducking = False


        if is_jumping and aray < 100 and (current_time - last_jump_time) > fall_delay:
            pyautogui.keyDown('down')
            time.sleep(0.005)
            pyautogui.keyUp('down')
            is_jumping = False
        
        if is_jumping and (current_time - last_jump_time) > 0.25 and aray < 50:
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
        cv2.imshow('T-Rex Bot', binary)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        time.sleep(0.008)

cv2.destroyAllWindows()