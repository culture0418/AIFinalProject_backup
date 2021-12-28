from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import os

camera = PiCamera()
camera.resolution = (640, 480)

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
                    cv2.imshow('capture', img) 
                    cv2.waitKey(10) 
                    cv2.imwrite("captured.jpg", img)
                    print("save the image")
                    output.truncate(0) # 只保留最後一張影像，以免過多影像塞爆暫存
                    detect = False
                    detect = detector("captured.jpg")
                    
                    if detect == True:
                        print("dected faces")
                        # camera.start_recording('video.h264')
                        # print("start recording!")
                    else:
                        print("the user is out of range !")
                       #camera.stop_recording()
                        print("stop recording!")
                        content = True
                       #camera.close()
                        

except KeyboardInterrupt:
        print('interrupt')

finally:
        camera.close()
        cv2.destroyAllWindows()



