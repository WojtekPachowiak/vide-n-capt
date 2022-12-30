# importing the required packages
import pyautogui
import cv2
import numpy as np
import matplotlib.pyplot as plt


# Specify resolution
resolution = (1920, 1080)
 
# Specify video codec
codec = cv2.VideoWriter_fourcc(*"XVID")
 
# Specify name of Output file
filename = "Recording.avi"
 
# Specify frames rate. We can choose any
# value and experiment with it
fps = 60.0
 
print(cv2.getBuildInformation())

# Creating a VideoWriter object
out = cv2.VideoWriter(filename, codec, fps, resolution)
 
# Create an Empty window
cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
 
# Resize this window
cv2.resizeWindow("Live", 480, 270)
 
while True:
    # Take screenshot using PyAutoGUI
    img = pyautogui.screenshot()
 
    # Convert the screenshot to a numpy array
    frame = np.array(img)
 
    # Convert it from BGR(Blue, Green, Red) to
    # RGB(Red, Green, Blue)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
 
    # Write it to the output file
    out.write(frame)
     
    # Optional: Display the recording screen
    cv2.imshow('Live', frame)
     
    # Stop recording when we press 'q'
    if cv2.waitKey(1) == ord('q'):
        break
 
# Release the Video writer
out.release()

cap = cv2.VideoCapture(filename)

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
 # Create an Empty window
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)

plt.figure()

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()

  # Display the resulting frame
  # cv2.imshow('Frame',frame)
  plt.imshow(frame)

  # Press Q on keyboard to  exit
  if cv2.waitKey(25)== ord('w'):
    break
 

# When everything done, release the video capture object
cap.release()
# Destroy all windows
cv2.destroyAllWindows()