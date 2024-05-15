import cv2
import numpy as np
import time as t

video = cv2.VideoCapture("download.mp4")
t.sleep(1)
bg = 0
count = 0
for i in range(60):
    #video.read() returns two information, first imformation is the return status which could be true or false depending upon whether python was able to read every indidivual frame
    #second information is the frame of the video itself
    return_val,bg = video.read()
    if return_val == False:
        continue

bg = np.flip(bg,axis=1)

while video.isOpened():
    status,frame = video.read()
    if not status:
        break
    count += 1 
    img = np.flip(frame,axis=1)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_1 = np.array([100,40,40])
    upper_1 = np.array([100,255,255])
    mask_1 = cv2.inRange(hsv_img,lower_1,upper_1)

    lower_2 = np.array([155,40,40])
    upper_2 = np.array([180,255,255])
    mask_2 = cv2.inRange(hsv_img,lower_2,upper_2)

    mask_1 = mask_1 + mask_2
    
    #blur after proccessing HSV format

    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations = 2)
    mask_1 = cv2.dilate(mask_1, np.ones((3,3), np.uint8), iterations = 1)
    mask_2 = cv2.bitwise_not(mask_1)
    #masking happens here, adding 2 images together
    result_1 = cv2.bitwise_and(bg,bg,mask= mask_1)
    result_2 = cv2.bitwise_and(img,img,mask= mask_2)

    final_img = cv2.addWeighted(result_1,1,result_2,1,0)
    cv2.imshow("red screen effect",final_img)
    k = cv2.waitKey(10)
    if k == 27:
        break
    
cv2.destroyAllWindows()
video.release()