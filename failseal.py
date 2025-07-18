import cv2
import numpy as np 

def seilfailed(image, ref):
    img = cv2.imread(image)
    img1 = img.copy()
    ref1 = ref.copy()
    ref1 = cv2.resize(ref1,(700,590))
    cropped_img = img.copy()
    img2 = img.copy()
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 210, 255, cv2.THRESH_TOZERO + cv2.THRESH_BINARY_INV)
    cont1, hera1 = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    for i in range(0,len(cont1)):
        area=cv2.contourArea(cont1[i])
        if( area>20000):
            x,y,w,h= cv2.boundingRect(cont1[i])
            cropped_img=img1[y:y+h+5, x:x+w+5]
    
    rez = cv2.resize(cropped_img, (700 ,590))
    img2 = rez.copy()
    frame_out = rez.copy()
    gray1 = cv2.cvtColor(rez, cv2.COLOR_BGR2GRAY)
    refgray = cv2.cvtColor(ref1, cv2.COLOR_BGR2GRAY)
    _,thref = cv2.threshold(refgray, 245, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    _, th1 = cv2.threshold(gray1, 210, 255, cv2.THRESH_TOZERO + cv2.THRESH_BINARY_INV)
    cont2, hera2 = cv2.findContours(th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    conref, heraref = cv2.findContours(thref, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cn = cv2.drawContours(ref, conref, -1, (255,0,0), 2)
    min_contour_area = 0  # Define your minimum area threshold
    large_contours = [cnt for cnt in cont2 if cv2.contourArea(cnt) > min_contour_area ]
    for cnt in large_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            frame_out = cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 0, 200), 3)
    return frame_out