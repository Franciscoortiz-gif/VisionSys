import cv2
import numpy as np

def remove_blue(image):
        """
                 Retirar color azul
        """
 
                 #      
        blue_c, green_c, red_c = cv2.split(image)
 
                 # Más entrante un parámetro cv2.thresh_otsu, y configura la trilla de umbral a 0, el algoritmo encontrará el umbral óptimo
        thresh, ret = cv2.threshold(blue_c, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                 #Efecto #       95%
        filter_condition = int(thresh * 0.95)
 
        _, blue_thresh = cv2.threshold(blue_c, filter_condition, 255, cv2.THRESH_BINARY)
 
                 # Girar la imagen de nuevo a 3 canales
        result_img = np.expand_dims(blue_thresh, axis=2)
        result_img = np.concatenate((result_img, result_img, result_img), axis=-1)
 
        return result_img

