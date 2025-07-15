import cv2
import numpy as np 
#[5:13 p.m., 15/7/2025] Jose Ruelas: El paquete mide 12" X 12 "
#[5:13 p.m., 15/7/2025] Jose Ruelas: 305 X 305mm
def distancemask(image):
    img = image.copy()
    img2 = image.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    cont1, hera1 = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conts = cv2.drawContours(img2, cont1,-1, (0, 255, 0), 3)
    return conts