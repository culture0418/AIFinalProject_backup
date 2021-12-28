# coding=utf-8
# 先拍下來，再組合成影片
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

def images_to_video():
    img = cv2.imread('image1.jpg')
    fps = 30
    imgInfo = img.shape
    size = (imgInfo[0], imgInfo[1])
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('input23.mp4', fourcc, fps, size)

    files = os.listdir('videodata/')
    out_num = len(files)
    for i in range(0, out_num):
        filename = 'videodata/' + str(i) + 'jpg'
        img = cv2.imread(filename)
        out.write(img)
        return out

def video():
    # 读取设备
    cap = cv2.VideoCapture(0)
    time.sleep(5)
    if  GPIO.input(COUNTER_PIN) == GPIO.HIGH:
        print('get the bottom sign')
        while cap.isOpened():
            for i in range(50):
                ret, frame = cap.read()
                i += 1
                print(i)
                cv2.imwrite('/home/pi/videodata/image{}.jpg'.format(i), frame)
                detect = detector('image{}.jpg'.format(i))
                print('decting')
                if detect != True:
                    print('no faces')
                    cap.release()
                    break

         


def main():
    video()
    output = images_to_video()

if __name__ == "__main__":
    main()

