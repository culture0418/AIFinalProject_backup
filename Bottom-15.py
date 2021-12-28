# coding=utf-8
# input25.avi fps=15
# input26.avi fps=10
# input27.avi fps=5
import cv2
import time
import numpy as np
import subprocess


#import Levenshtein

import RPi.GPIO as GPIO
LED_PIN = [3]
COUNTER_PIN = 16 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(COUNTER_PIN, GPIO.IN)


password=[]
pushbutton=True


# 重設密碼：數字 abc 句子
def setpassword():  #set password if there is older passsword,user need to enter the older one,or user can't change
    print("setpassword()")
    a1 = raw_input("please choose what kind of your pasword, 1:numbers 2:letter 3:sentence: ")
    
    if a1=='1': #set the number password ,turn the number to letters
        print("setpassword:number")
        s=''
        number_letter={'1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine','0':'zero'}
        if password == []:
            x = raw_input("please input your password: ")
            for i in x:
                s+=(number_letter[i]+' ')
            password.append(s)  
                
            for pas in password:
                print(pas)
                
            print("the type of password is : ") #test
            print(type(password[0]))

        else:
            y=raw_input("please input the older password: ")
            if password_check1(y,password)!=0:
                x = raw_input("please input new password: ")
                password.pop()
                for i in x:
                    s+=(number_letter[i]+' ')  #翻譯成英文單字後連成字串儲存
                password.append(s) 
                return 0
                
    elif a1=='2':
        
        print("setpassword:letter")
        s=''
        
        if password == []:
            x = raw_input("please input your password: ")
            for i in x:
                s+=(i+' ')  #以字串儲存
            password.append(s)       
            for pas in password:
                print(pas)
                
        else:
            x=raw_input("please input the older password: ")
            if password_check1(x,password)!=0:
                password.pop()
                x = raw_input("please input your password: ")
                for i in x:  #以字串儲存
                    s+=(i+' ')
                password.append(s)
                return 0
            
            else:
                print("Wrong,plese try again")
        
    elif a1=='3':
        print("setpassword:sentence")
        
        
        if password == []:
            x = raw_input("please input your password: ")
            password.append(x)      #直接儲存輸入字串 
            for pas in password:
                print(pas)
                
        else:
            x=raw_input("please input the older password: ")
            if password_check1(x,password)!=0:
                password.pop()
                x = raw_input("please input new password: ")
                password.append(x)
                return 0
            
            else:
                print("Wrong,plese try again")
                
        
    return 0


def password_check1(test,password):  #分割成單字
    
    test1=test.split(' ')
    password1=password[0].split(' ')
    print(type(password1))
    print(type(test1))
    
    diff=int(len(password1)-len(test1))
    print(diff)
    test1.extend("" for _ in range(diff)) #如果輸入密碼太短把它補成跟原本密碼同樣長度
    
    #test
    print("test is: ")
    print(test1)
    
    print("password1 is: ")
    print(password1)
    
    wrong=[]
    for i in range(len(password1)):
        # print("password[%d] is %s" %(i,password1[i]))
        # print("test1[%d] is %s" %(i,test1[i]))
        if test1[i]!=password1[i]:
            # print(" |%s| != |%s|" %(password1[i],test1[i]))
            wrong.append(str(i+1)) #把錯第幾個字存起來
        
    if wrong:
        print("The password is wrong.")
        
        print("The lenth you input %d words" %(len(test.split(' ')))) #告訴user輸入了幾個字
        print("The password's lenth is %d words" %(len(password1)))  #正確密碼幾個字
        
        print("No.{} word is wrong".format(" ".join(wrong)))  #錯了第幾個字
        
        bottom = False
        return bottom
        # return 0

    else:
        #GPIO.output(LED_PIN[0], GPIO.HIGH)
        time.sleep(1.5) #delay 1.5 seconds
        print("The password is right.")
        bottom = False
        return bottom 
        # return 1
        
        
def password_check2(test,password): #組合成一個字串
    
    test1=test.split(' ')
    s1=""
    test2=s1.join(test1)
    print(test2) #test
    password1=s1.join(password[0].split(' '))
    print(password1) #test
    
    diff=int(len(password1)-len(test2))
    print(diff)
    
    if diff<0:
        bigger=len(test2)
        password1+="0"*(-diff)
    else:
        bigger=len(password1)
        test2+="0"*diff
    
    wrong=[]
    for i in range(bigger):
        if test2[i]!=password1[i]:
            wrong.append(str(i+1))
            
    if wrong:
        print("The password is wrong.")
        print("The lenth you input %d words" %(len(s1.join(test1))))
        print("The password's lenth is %d words" %(len(s1.join(password[0].split(' '))))) 
        
        print("No.{} word is wrong".format(" ".join(wrong)))  #錯了第幾個字母
        
        
        return 0
        
    else:
        #GPIO.output(LED_PIN[0], GPIO.HIGH)
        time.sleep(1.5) #delay 1.5 seconds
        print("The password is right,you can enter.")
        return 1

 


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


def camerarecording():
    # 读取设备，picamera跟webcam分別對應0跟1
    cap = cv2.VideoCapture(0) 
    # 读取摄像头FPS
    cap.set(cv2.CAP_PROP_FPS, 60)
    # set dimensions 设置分辨率
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    print('get the bottom sign && start recording!')
    out = cv2.VideoWriter('input47(2525).avi', fourcc, 20, (640, 480))
    
    
    while cap.isOpened():
        ret, frame = cap.read()
        out.write(frame)
        cv2.imwrite('image.jpg', frame)
        detect = detector('image.jpg')
        print('decting')

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
            print('''\nif you want to set password, enter "1".if you want to enter,push the button: ''')
            c=raw_input()
            print("c is {}".format(c))
            print("type c is {}".format(type(c)))
            if c=='1':
                setpassword()
        
            bottom = True
            content.append(bottom)
            
        if content[-1] == True:
            bottom = False # 等待下一次按按鈕
            camerarecording()
            # 轉檔 、丟入資料夾 、# model inference
            subprocess.call(
                        'ffmpeg -i input47\(2525\).avi output47.mpg',
                    shell=True)
            subprocess.call(
                        'ffmpeg -i output47.mpg -s 100x50 -c:a copy output1.mpg',
                    shell=True)
            print("------------------")
            subprocess.call(
                        'python3 /home/pi/LipNet/predict.py /home/pi/LipNet/evaluation/models/overlapped-weights368.h5 /home/pi/LipNet/output1.mpg',
                    shell=True)
            # sum = subprocess.check_output('python3 /home/pi/LipNet/predict.py /home/pi/LipNet/evaluation/models/overlapped-weights368.h5 /home/pi/LipNet/output1.mpg',
            #          shell=True)
            # print("This is {}".format(sum))
        
            print("----------")
            
            # 讀檔案
            path = './result.txt'
            num1 = 0
            with open(path, 'r') as file:
                for num in file:
                    print(num)
                    num1 = num
            
                
            # 密碼確認
            password_check1(num1,password) #test接inference result

except KeyboardInterrupt:
        print('interrupt')

finally:
    cv2.destroyAllWindows()


# todo task
# (1) 自動轉成.mpg
# (2) 丟入modle inference 
# (3) output 比對
# (4) correct or back to the top


