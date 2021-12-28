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
    
    if len(faces) == 0:
        detect = False
    else:
        detect = True

    return detect


try:
    camera.start_preview()
    time.sleep(2)
    content = False
    if  GPIO.input(COUNTER_PIN) == GPIO.HIGH:
        camera.start_recording('video-test2.h264')
        print("start recording")
        content = True
        while True:
            with PiRGBArray(camera) as output:
                for foo in camera.capture_continuous(output, 'bgr'): 
                    img = output.array 
                    cv2.imshow('capture', img) 
                    cv2.waitKey(1) 
                    cv2.imwrite("captured.jpg", img)
                    print("save the image")
                    output.truncate(0) 
                    detect = False
                    detect = detector("captured.jpg")
                    
                    if detect != True:
                        print("the user is out of range !")
                        break

            camera.stop_recording()
            print("stop recording!")
            content = True
        
                        

except KeyboardInterrupt:
        print('interrupt')

finally:
        camera.close()
        cv2.destroyAllWindows()



