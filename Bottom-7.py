# coding=utf-8

import os
import cv2 
import numpy as np
import time
import threading
from datetime import datetime
filename = datetime.now().strftime("%m%d_%H%M")
print(filename)

import RPi.GPIO as GPIO
COUNTER_PIN = 16 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(COUNTER_PIN, GPIO.IN)

# 读取设备
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
# 读取摄像头FPS
fps = cap.get(cv2.CAP_PROP_FPS)
print("1")


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

'''
opencv每隔若干秒拍照并且保存
'''
def takephoto():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read() # ret 回傳 bool, fram回傳攝影機單張畫面
    while ret:
        img = cv2.resize(frame, (512,512), interpolation=cv2.INTER_NEAREST)
        cv2.imshow('capture', img) 
        cv2.waitKey(1) 
        cv2.imwrite("captured.jpg", img)
        print("save the image")
        img.truncate(0) 
        return img

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
    time.sleep(2)
    content = False
    if  GPIO.input(COUNTER_PIN) == GPIO.HIGH:
        print('get the bottom sign')
        # 初始化文件写入 文件名 编码解码器 帧率 文件大小
        video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (800, 400)) 
        ret, frame = cap.read()
        print("start recording")
        content = True
        print('1')
        while cap.isOpened():
            takephoto()
            detect = False
            detect = detector("captured.jpg")
            if detect != True:
                print("the user is out of range !")
                break

            cap.release()
            print("stop recording!")
            content = True

except KeyboardInterrupt:
        print('interrupt')

finally:
        cap.release()
        cv2.destroyAllWindows()



