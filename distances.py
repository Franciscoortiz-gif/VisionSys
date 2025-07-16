import cv2
import numpy as np 
#[5:13 p.m., 15/7/2025] Jose Ruelas: El paquete mide 12" X 12 "
#[5:13 p.m., 15/7/2025] Jose Ruelas: 305 X 305mm
def distancemask(image):
    cropped_img = image.copy()
    kernel = np.ones((5, 5), np.uint8) 
    img = image.copy()
    img3 = image.copy() 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(gray, 25, 255, cv2.THRESH_TRIANGLE)
    cont1, hera1 = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for i in range(0,len(cont1)):
        area=cv2.contourArea(cont1[i])
        if( area>20000):
            x,y,w,h= cv2.boundingRect(cont1[i])
            cropped_img=img3[y:y+h, x:x+w]
                  
    return cropped_img

def isdestructured(mask, image):
    return image