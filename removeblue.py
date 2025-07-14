import cv2
import numpy as np
import sys

def remove_blue(imag):
        """
        
        """
        if imag is None:
                print("image not found")
                sys.exit()
        else:
                image = imag.copy()
                conts = imag.copy()
                conts2 = imag.copy()
                fra = imag.copy()
                blurred = cv2.GaussianBlur(image, (11, 11), 0)
                gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
                

                ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO + cv2.THRESH_OTSU + cv2.THRESH_BINARY)
                cont, hera = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
                contornos = cv2.drawContours(conts, cont, -1, (0, 255, 0), 3)
                efe = cv2.blur(contornos,(3,3))
                edges = cv2.Canny(efe,170,255)
                cont2, hera2 = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
                contornos2 = cv2.drawContours(conts2, cont2, -1, (0, 255, 0), 3)
                min_contour_area = 1000  # Define your minimum area threshold
                large_contours = [cnt for cnt in cont2 if cv2.contourArea(cnt) > min_contour_area and cv2.contourArea(cnt) < 8000]
                for cnt in large_contours:
                        x, y, w, h = cv2.boundingRect(cnt)
                        frame_out = cv2.rectangle(fra, (x, y), (x+w, y+h), (0, 0, 200), 3)

                return thresh, frame_out     
        
        
              
                 #      
        
 
        return 