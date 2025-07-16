import cv2
import numpy as np 
#[5:13 p.m., 15/7/2025] Jose Ruelas: El paquete mide 12" X 12 "
#[5:13 p.m., 15/7/2025] Jose Ruelas: 305 X 305mm
def distancemask(image):
    cropped_img = image.copy()
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
    img = image.copy()
    img2 = image.copy()
    
    pos = []
    lene = []
    distance = 0 
    distance2 = 0
    dismm = 0
    dismm2 = 0
    tole = 0
    hi, wi= img2.shape[:2]
    cont1, hera1 = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 6000  # Define your minimum area threshold
    large_contours = [cnt for cnt in cont1 if cv2.contourArea(cnt) > min_contour_area and cv2.contourArea(cnt) < 13000 ]
    for cnt in large_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                center_x = x+w/2 
                center_y = y+h/2
                pos.append(center_x)
                pos.append(center_y)
                lene = large_contours      
                
    if len(lene) == 4:
        cv2.line(img2,(int(pos[0]),int(pos[1])),(int(pos[6]), int(pos[7])),(26, 52, 255),5)
        cv2.line(img2,(int(pos[2]),int(pos[3])),(int(pos[4]), int(pos[5])),(26, 52, 255),5)
        distance = np.sqrt((pos[2] - pos[4])**2 + (pos[3] - pos[5])**2)
        distance2 = np.sqrt((pos[6] - pos[0])**2 + (pos[7] - pos[1])**2)
        dismm = (distance * 305) / wi
        dismm2 = (distance2 * 305) / wi
        cv2.putText(img2, str(dismm2)[:3]+ "mm", (int(pos[4]), int(pos[5])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(img2, str(dismm)[:3] + "mm", (int(pos[6]), int(pos[7])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        tole = 3
        porcent = tole/100
        tol= 215.6677 * porcent
        
        if dismm > dismm2:
            res = (dismm - dismm2) 
        else:
            res = dismm - dismm2
            res = res * -1
        if res > tol:
            cv2.putText(img2, "No estructurado", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (192,255,199), 2,cv2.LINE_AA)
        else:
            cv2.putText(img2, "Estructurado", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (192,255,199), 2,cv2.LINE_AA)

    return img2