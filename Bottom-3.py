from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import os

camera = PiCamera()
camera.resolution = (320, 240)

import time
from datetime import datetime


import RPi.GPIO as GPIO
COUNTER_PIN = 16 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(COUNTER_PIN, GPIO.IN)

def detector(filename):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.1,4)
    # 判斷有沒有人臉
    if len(faces) == 0:
        detect = False
    else:
        detect = True

    return detect

content = False
try: 
    while not content:
        with PiRGBArray(camera) as output:
            if  GPIO.input(COUNTER_PIN) == GPIO.HIGH:
                for foo in camera.capture_continuous(output, 'bgr', use_video_port=True): 
                    img = output.array
                    img = cv2.rotate(img, cv2.ROTATE_180) 
                    cv2.imshow('capture', img) 
                    cv2.waitKey(10) 
                    cv2.imwrite("captured.jpg", img)
                    print("save the image")
                    output.truncate(0) # 只保留最後一張影像，以免過多影像塞爆暫存
                    detect = False
                    detect = detector("captured.jpg")
                    
                    if detect == True:
                        print("dected faces")        
                    else:
                        print("the user is out of range !")
                        content = True

except KeyboardInterrupt:
        print('interrupt')

finally:
        camera.close()
        cv2.destroyAllWindows()



