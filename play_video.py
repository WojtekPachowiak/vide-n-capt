import numpy as np
import cv2

cap = cv2.VideoCapture('outlaw.mkv')

while True:
    ret,frame = cap.read()
    cv2.imshow('output',frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()