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
                #exte = imag.copy()
                blurred = cv2.GaussianBlur(image, (11, 11), 0)
                gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
                

                ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO + cv2.THRESH_OTSU + cv2.THRESH_BINARY)
                
                gamma = 2.56
                invGamma = 1.0 / gamma
                table = np.array([((i / 255.0) ** invGamma) * 255
                        for i in np.arange(0, 256)]).astype("uint8")
                # apply gamma correction using the lookup table
                gammacor = cv2.LUT(thresh, table)
                kernel = np.ones((5, 5), np.uint8) 
                closing = cv2.morphologyEx(gammacor, cv2.MORPH_OPEN, kernel, iterations=5)
                ret2, th2 = cv2.threshold(closing, 153.7, 255, cv2.THRESH_TOZERO + cv2.THRESH_BINARY)
                cont, hera = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
                contornos = cv2.drawContours(conts, cont, -1, (0, 255, 0), 3)
                efe = cv2.blur(contornos,(3,3))
                edges = cv2.Canny(efe,170,255)
                cont2, hera2 = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
                contornos2 = cv2.drawContours(conts2, cont2, -1, (0, 255, 0), 1)
                min_contour_area = 1000  # Define your minimum area threshold
                large_contours = [cnt for cnt in cont2 if cv2.contourArea(cnt) > min_contour_area and cv2.contourArea(cnt) < 8000]
                for cnt in large_contours:
                        x, y, w, h = cv2.boundingRect(cnt)
                        frame_out = cv2.rectangle(fra, (x, y), (x+w, y+h), (0, 115, 200), 3)

                return frame_out
        
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
        return frame_out,i


    
                
        
