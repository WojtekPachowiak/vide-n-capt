#base taken from here: https://www.geeksforgeeks.org/create-a-screen-recorder-using-python/

import pyautogui
import cv2
import numpy as np
 



window_name = "Live"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 480, 270)

################################
#position the recording window
################################

region=None
while True:
    region = cv2.getWindowImageRect(window_name)
    img = pyautogui.screenshot(region=region)
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    cv2.imshow(window_name, frame)
     
    k = cv2.waitKey(100)
    if k == ord('q'):
        break
    if k == ord('r'):
        break


###########################
#record the chosen region
###########################


resolution = (region[2],region[3])
codec = cv2.VideoWriter_fourcc(*"XVID")
filename = "Recording.avi"
fps = 60.0
out = cv2.VideoWriter(filename, codec, fps, resolution)

while True:
    img = pyautogui.screenshot(region=region)
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    out.write(frame)
    # cv2.imshow('output',frame)

    if cv2.waitKey(100) == ord('q'):
        break

out.release()

###########################
#play the recording
###########################

cap = cv2.VideoCapture(filename)

while True:
    ret,frame = cap.read()
    if ret:
        cv2.imshow('output',frame)
        if cv2.waitKey(1) == ord('q'):
            break
    else: 
        break

cap.release()
 
# Destroy all windows
cv2.destroyAllWindows()

