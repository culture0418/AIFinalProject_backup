# coding=utf-8
# input25.avi fps=15
# input26.avi fps=10
# input27.avi fps=5
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
    if  GPIO.input(COUNTER_PIN) == GPIO.HIGH:
        # 读取设备
        # 我同時試picamera跟webcam所以有兩台，分別對應0跟1
        cap = cv2.VideoCapture(1) 
        # 读取摄像头FPS
        fps = cap.get(cv2.CAP_PROP_FPS)
        print('fps={}'.format(fps))
        # set dimensions 设置分辨率
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        print('get the bottom sign && start recording!')
        out = cv2.VideoWriter('input31.avi', fourcc, 20, (640, 480))
        
        while cap.isOpened():
            ret, frame = cap.read()
            out.write(frame)
            cv2.imwrite('image.jpg', frame)
            detect = detector('image.jpg')
            print('decting')

            if detect != True:
                print('no faces')
                out.release()
                cap.release()
                break
            
except KeyboardInterrupt:
        print('interrupt')

finally:
    cv2.destroyAllWindows()



