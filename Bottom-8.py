# coding=utf-8
import os
import cv2
import numpy as np

import time
from datetime import datetime
filename = datetime.now().strftime("%m%d_%H%M")
print(filename)


import RPi.GPIO as GPIO
COUNTER_PIN = 16 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(COUNTER_PIN, GPIO.IN)

def detector(filename):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.1,4)
    
    if len(faces) == 0:
        detect = False
    else:
        detect = True

    return detect

try:
    # 读取设备
    cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    # 读取摄像头FPS
    fps = cap.get(cv2.CAP_PROP_FPS)
    # set dimensions 设置分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    print('start recording!')

    if  GPIO.input(COUNTER_PIN) == GPIO.HIGH:
        print('get the bottom sign')
        out = cv2.VideoWriter('input16.mp4v', fourcc, fps, (640, 480))
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                out.write(frame)
                cv2.imshow('frame', frame)
                cv2.imwrite('image.jpg', frame) # 截图
                detect = detector('image.jpg')
                print('decting')
                if detect == False:
                    print('no faces')
                    out.release()
                    cap.release()
                    break
            
except KeyboardInterrupt:
        print('interrupt')

finally:
    cv2.destroyAllWindows()



