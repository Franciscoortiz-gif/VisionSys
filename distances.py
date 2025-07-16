import cv2
import numpy as np 
#[5:13 p.m., 15/7/2025] Jose Ruelas: El paquete mide 12" X 12 "
#[5:13 p.m., 15/7/2025] Jose Ruelas: 305 X 305mm
def distancemask(image):
    kernel = np.ones((5, 5), np.uint8) 
    img = image.copy()
    img2 = image.copy()
    img3 = image.copy() 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mor = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=23)
    cont1, hera1 = cv2.findContours(mor, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conts = cv2.drawContours(img2, cont1,-1, (0, 255, 0), 3)
    
    return mor