import cv2
import numpy as np
import sys



def remove_blue(imag):
        if imag is None:
                print("image not found")
                sys.exit()
        else:
                image = imag.copy()
                conts = imag.copy()
                conts2 = imag.copy()
                fra = imag.copy()
                frame_out = imag.copy()
                """ gamma = 1.5
                #exte = imag.copy()
                invGamma = 1.0 / gamma
                table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

                # Apply the lookup table to the image
                im2 = cv2.LUT(image, table)
                blurred = cv2.GaussianBlur(im2, (3, 3), 0)
                gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
                ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_TOZERO + cv2.THRESH_BINARY)
        
                
                kernel = np.ones((5, 5), np.uint8) 
                closing = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=5)    
                ret2, th2 = cv2.threshold(closing, 159.8, 255,cv2.THRESH_BINARY)"""
                bl = cv2.blur(image, (3,3))
                edges = cv2.Canny(bl, 120, 255)
                cont, hera = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
                con = cv2.drawContours(conts2, cont, -1, (255,0,255), 3)
                min_contour_area = 500  # Define your minimum area threshold
                large_contours = [cnt for cnt in cont if cv2.contourArea(cnt) > min_contour_area and cv2.contourArea(cnt) < 18000]
                for cnt in large_contours:
                        x, y, w, h = cv2.boundingRect(cnt)
                        frame_out = cv2.rectangle(fra, (x, y), (x+w, y+h), (60, 115, 200), 3)

                return frame_out, edges
        
                #ret, th = cv2.threshold(gray,110, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU )

        
def detectTapes(image):

        img = image.copy()
        frame = image.copy()
        frame_out = image.copy()
        i = 0
        
        # build a lookup table mapping the pixel values [0, 255] to
        gamma = 2.56
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                for i in np.arange(0, 256)]).astype("uint8")
        # apply gamma correction using the lookup table
        gammacor = cv2.LUT(img, table)
        
        blur = cv2.blur(gammacor, (5,5))
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        ret, th = cv2.threshold(gray,197.5, 255, cv2.THRESH_TOZERO + cv2.THRESH_BINARY)
        blu2 = cv2.blur(th, (3,3))
        kernel = np.ones((25, 25), np.uint8) 
        closing = cv2.morphologyEx(blu2, cv2.MORPH_OPEN, kernel)
        cont2, hera2 = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        min_contour_area = 6000  # Define your minimum area threshold
        large_contours = [cnt for cnt in cont2 if cv2.contourArea(cnt) > min_contour_area and cv2.contourArea(cnt) < 13000 ]
        for cnt in large_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                frame_out = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 200), 3)
                i = len(large_contours)
        
        frame_out = cv2.putText(frame_out, "Botellas encontradas "+str(i), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0),2)
        
        return frame_out, closing


    
                
        
