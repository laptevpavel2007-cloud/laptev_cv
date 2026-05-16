import numpy as np
import cv2
import zmq 

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.connect("tcp://84.237.21.36:6002")

cv2.namedWindow("Stream", cv2.WINDOW_GUI_NORMAL)
cnt = 0
background = None
while True:
    msg = socket.recv()
    print(len(msg))
    key = cv2.waitKey(100)
    if key == ord("q"):
        break
    cnt += 1

    frame = cv2.imdecode(np.frombuffer(msg, np.uint8), -1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame, contours, -1, (255, 0, 0), 2)

    eps = 0.02 * cv2.arcLength(contours[0], True)
    approx = cv2.approxPolyDP(contours[0], eps, True)
    for p in approx:
        x, y = p[0]
        cv2.circle(frame, (x, y), 5, (255, 0, 0), 2)

    corners = approx.reshape(4, 2).astype(np.float32)
    s = corners.sum(axis=1)
    diff = np.diff(corners, axis=1)
    pts2 = np.array([corners[np.argmin(s)], corners[np.argmin(diff)], corners[np.argmax(s)], corners[np.argmax(diff)]], dtype="float32")

    text_str = "Meow"          
    (text_w, text_h), line = cv2.getTextSize(text_str, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)

    img_w = text_w + 2 * 20
    img_h = text_h + 2 * 20 + line
    text_img = np.ones((img_h, img_w), dtype=np.uint8) * 255
    
    cv2.putText(text_img, text_str, (20, text_h + 20), cv2.FONT_HERSHEY_SIMPLEX, 2, 3)
    text_img = cv2.cvtColor(text_img, cv2.COLOR_GRAY2BGR) 

    pts1 = np.float32([[0, 0], [img_w, 0], [img_w, img_h], [0, img_h]])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(text_img, M, (frame.shape[1], frame.shape[0]))

    mask_leaf = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask_leaf, [approx.astype(np.int32)], 255)

    bg = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask_leaf))
    fg = cv2.bitwise_and(warped, warped, mask=mask_leaf)
    result = cv2.add(bg, fg)

    cv2.imshow("Stream", result)
