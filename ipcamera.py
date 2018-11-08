import cv2
import numpy
cap = cv2.VideoCapture("rtsp://192.168.3.53:6554/stream_0")#use wireshark to find out the video stream
print cap.isOpened()
frameNum = 1
while(cap.isOpened()):
    ret,frame = cap.read()
    print frameNum
    frameNum = frameNum + 1
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
