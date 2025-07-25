import cv2
import numpy as np
import sys



def remove_blue(imag):
        if imag is None:
                print("image not found")
                sys.exit()
        else:
                ima = imag.copy()
                frame_out = imag.copy()
                kernel = np.ones((5, 5), np.uint8) 
                grw = cv2.cvtColor(ima, cv2.COLOR_BGR2GRAY)
                norm = cv2.normalize(grw, None, 0,160, cv2.NORM_MINMAX)
                _,mm1 = cv2.threshold(norm, 120,255,cv2.THRESH_BINARY)
                ero = cv2.erode(mm1, kernel,iterations=3)
                con, _ = cv2.findContours(ero, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                #draw = cv2.drawContours(ima, con, -1,(0,0,255),3)
                large_contours = [cnt for cnt in con if cv2.contourArea(cnt) > 800 and cv2.contourArea(cnt) < 20000 ]
                for cnt in large_contours:
                        x, y, w, h = cv2.boundingRect(cnt)
                        frame_out = cv2.rectangle(ima, (x, y), (x+w, y+h), (0, 0, 200), 3)
  
                return frame_out
                
        
def detectTapes(image):

        img = image.copy()
        frame = image.copy()
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
        inv = -image
        YUVw = cv2.cvtColor(inv, cv2.COLOR_BGR2HSV)
        Yc = cv2.split(YUVw)
        cv2.equalizeHist(Yc[0], Yc[0])
        hisY = cv2.merge(Yc, YUVw)
        his = cv2.cvtColor(hisY, cv2.COLOR_HSV2BGR)
        his = cv2.cvtColor(his, cv2.COLOR_BGR2GRAY) 
        blur = cv2.blur(his, (19,19))
        _, th = cv2.threshold(blur,60, 255, cv2.THRESH_TOZERO + cv2.THRESH_BINARY_INV)
        blu2 = cv2.blur(th, (3,3))
        kernel = np.ones((25, 25), np.uint8) 
        closing = cv2.morphologyEx(blu2, cv2.MORPH_OPEN, kernel)
        cont2, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)       
        min_contour_area = 6000  # Define your minimum area threshold
        large_contours = [cnt for cnt in cont2 if cv2.contourArea(cnt) > min_contour_area and cv2.contourArea(cnt) < 13000 ]
        for cnt in large_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                frame_out = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 200), 3)
                i = len(large_contours)
        """kernel = np.ones((3, 3), np.uint8)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist = cv2.equalizeHist(img)
        bl = cv2.GaussianBlur(hist,(31,31), cv2.BORDER_DEFAULT)
        
        cir = cv2.HoughCircles(th,cv2.HOUGH_GRADIENT,1,bl.shape[0]/64, param1=15, param2=25,minRadius=50, maxRadius=60)
        
        if cir is not None:
                circu = np.around(cir[0,:]).astype("int")
                for (x,y,r) in circu:
                    frame_out = cv2.circle(image, (x,y), r, (0, 255, 0), 2)
                    i = len(circu)"""
        
        frame_out = cv2.putText(frame_out, "Botellas encontradas "+str(i), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0),2)
        
        return frame_out, closing


    
                
        
