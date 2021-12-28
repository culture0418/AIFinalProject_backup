# coding=utf-8
import cv2
 
cap = cv2.VideoCapture(1)
# 設定擷取影像的尺寸大小
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 使用 XVID 編碼
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# 建立 VideoWriter 物件，輸出影片至 output.avi
# FPS 值為 20.0，解析度為 640x480
out = cv2.VideoWriter('output1.avi', fourcc, 20.0, (640, 480))

while cap.isOpened():
   ret, frame = cap.read()
   print('recroding')
 
   if not ret:
       print("結束")
       break
 
   # 將擷取的圖片寫入VideoWriter
   out.write(frame)
 
   cv2.imshow('frame', frame)
 
   if cv2.waitKey(1) == ord('q'):
       break

# 釋放所有資源
cap.release()
out.release()
cv2.destroyAllWindows()