import numpy as np
import cv2

cap = cv2.VideoCapture(0)

codec = cv2.VideoWriter_fourcc(*"XVID")
fps = 60.0
width,height = cap.get(3), cap.get(4)
out = cv2.VideoWriter('wojtekface.mp4',codec, fps, (width,height))

while cap.isOpened():
    ret,frame = cap.read()
    if ret ==True:
        out.write(frame)
        cv2.imshow('output',frame)
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()