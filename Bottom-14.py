# coding=utf-8
# input25.avi fps=15
# input26.avi fps=10
# input27.avi fps=5
import cv2
import time
import numpy as np


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
        return detect
    else:
        detect = True
        return detect, faces

    


def camerarecording():
    # 读取设备，picamera跟webcam分別對應0跟1
    cap = cv2.VideoCapture(0) 
    # 读取摄像头FPS
    fps = cap.get(cv2.CAP_PROP_FPS)
    # set dimensions 设置分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    print('get the bottom sign && start recording!')
    out = cv2.VideoWriter('input32.avi', fourcc, 20, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        out.write(frame)
        cv2.imwrite('image.jpg', frame)
        detect, faces = detector('image.jpg')
        print('decting')
        for (x, y, w, h) in faces:
        # Draw the rectangle around each face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            print('---------------------------')
            cv2.imshow("Face Detection", frame)
        
        
        

        if detect != True:
            bottom = False
            content.append(bottom)
            print('no faces, stop recording!')
            out.release()
            cap.release()
            break


try:   
    content = [False]
    bottom = False
    while True:
        if  GPIO.input(COUNTER_PIN) == GPIO.HIGH:
            bottom = True
            content.append(bottom)

        if content[-1] == True:
            bottom = False # 等待下一次按按鈕
            camerarecording()

except KeyboardInterrupt:
        print('interrupt')

finally:
    cv2.destroyAllWindows()


# todo task
# (1) 自動轉成.mpg
# (2) 丟入modle inference 
# (3) output 比對
# (4) correct or back to the top


