import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import CVisionTags
import cv2 
import numpy as np
import time
import subprocess
last_timer=0


video_capture = cv2.VideoCapture(0)

while True:
    timer=int(time.time()) #Время со старта процессора сек.
    ret, frame = video_capture.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.putText(frame,"Timer req/5 sec.: "+ str(timer - last_timer ), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255))
    if timer - last_timer > 5:
        cv2.imwrite('c:/python/ImageNet/images/img.jpg',frame)
        img = open("c:/python/ImageNet/images/img.jpg", "rb")
        info = CVisionTags.GetImageInfo(img)
        img.close()
        last_timer=timer  # сбрасываем таймер
    cv2.putText(frame,"Tags: ", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255))
    for i in range(len(info)):
        cv2.putText(frame,str(len(info)), (80,80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255))
        cv2.putText(frame,str(info[i]), (10,100+i*20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255))
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()


