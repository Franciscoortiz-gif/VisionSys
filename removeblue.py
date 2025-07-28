import cv2
import numpy as np
import sys



def remove_blue(imag, thvalue, normval, itera,kerne, areamin, areamax):
        if imag is None:
                print("image not found")
                sys.exit()
        else:
                ima = imag.copy()
                frame_out = imag.copy()
                kernel = np.ones((kerne, kerne), np.uint8) 
                grw = cv2.cvtColor(ima, cv2.COLOR_BGR2GRAY)
                norm = cv2.normalize(grw, None, 0,normval, cv2.NORM_MINMAX)
                _,mm1 = cv2.threshold(norm, thvalue,255,cv2.THRESH_BINARY)
                ero = cv2.erode(mm1, kernel,iterations=itera)
                con, _ = cv2.findContours(ero, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                draw = cv2.drawContours(ima, con, -1,(0,0,255),3)
                large_contours = [cnt for cnt in con if cv2.contourArea(cnt) > areamin and cv2.contourArea(cnt) < areamax ]
                for cnt in large_contours:
                        x, y, w, h = cv2.boundingRect(cnt)
                        frame_out = cv2.rectangle(ima, (x, y), (x+w, y+h), (0, 0, 200), 3)
  
                return frame_out, mm1, norm, ero, draw
                
        
def detectTapes(image):

        img = image.copy()
        frame = image.copy()
        frame2 = image.copy()
        closing = image.copy()
        frame_out = image.copy()
        i = 0
        
        # build a lookup table mapping the pixel values [0, 255] to
        """gamma = 2.56
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                for i in np.arange(0, 256)]).astype("uint8")
        # apply gamma correction using the lookup table
        gammacor = cv2.LUT(img, table)"""
        his = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        blur = cv2.blur(his, (19,19))
        _, th = cv2.threshold(blur,60, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        blu2 = cv2.blur(th, (3,3))
        kernel = np.ones((25, 25), np.uint8) 
        closing = cv2.morphologyEx(blu2, cv2.MORPH_OPEN, kernel)
        cont2, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        draw = cv2.drawContours(frame2, cont2, -1, (255,0,0),2)       
        min_contour_area = 6000  # Define your minimum area threshold
        large_contours = [cnt for cnt in cont2 if cv2.contourArea(cnt) > min_contour_area and cv2.contourArea(cnt) < 13000 ]
        for cnt in large_contours:
                #x, y, w, h = cv2.boundingRect(cnt)
                (x,y) ,radius= cv2.minEnclosingCircle(cnt)
                center = (int(x), int(y))
                radius = int(radius)
                frame_out = cv2.circle(frame, center, radius,(120,58,82), 2)
                i = len(large_contours)
        
        frame_out = cv2.putText(frame_out, "Botellas encontradas "+str(i), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0),2)
        
        return frame_out, closing, blur, th,blu2,draw


    
                
        
