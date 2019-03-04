import cv2
import time

cap = cv2.VideoCapture(1)
print(cap)
while True:
    ret, frame = cap.read()

    #print(frame)


    if(frame is not None):
        cv2.imshow('sample', frame)

        cv2.waitKey(1)
    else:
        time.sleep(1)
