#base taken from here: https://www.geeksforgeeks.org/create-a-screen-recorder-using-python/

import pyautogui
import cv2
import numpy as np
 
resolution = (1920, 1080)
 
codec = cv2.VideoWriter_fourcc(*"XVID")
 
filename = "Recording.avi"
 

fps = 60.0
 
 
# out = cv2.VideoWriter(filename, codec, fps, resolution)
 
window_name = "Live"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
 
cv2.resizeWindow(window_name, 480, 270)


record= False
region = cv2.getWindowImageRect(window_name)
while True:
    
    #update region only when not recording
    if record == False:
        region = cv2.getWindowImageRect(window_name)

    img = pyautogui.screenshot(region=region)
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    
    # out.write(frame)

    # if record == False:
    cv2.imshow(window_name, frame)
     
    k = cv2.waitKey(100)
    if k == ord('q'):
        break
    if k == ord('r'):
        if record==False:
            record = True
            cv2.destroyWindow(window_name)
        else:
            break

# Release the Video writer
# out.release()


# cap = cv2.VideoCapture(filename)

# # Check if camera opened successfully
# if (cap.isOpened()== False): 
#   print("Error opening video stream or file")
 
# # Read until video is completed
# while(cap.isOpened()):
#   # Capture frame-by-frame
#   ret, frame = cap.read()
#   if ret == True:
 
#     # Display the resulting frame
#     cv2.imshow('Frame',frame)
 
#     # Press Q on keyboard to  exit
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#       break
 
#   # Break the loop
#   else: 
#     break
 
# # When everything done, release the video capture object
# cap.release()


 
# Destroy all windows
cv2.destroyAllWindows()

