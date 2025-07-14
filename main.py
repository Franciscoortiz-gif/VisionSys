import numpy as np
import cv2 as cv
import removeblue

filename = ['images/bottle1.jpeg','images/bottle2.jpeg','images/bottle3.jpeg','images/bottle4.jpeg','images/IMG_3677.JPG','images/IMG_3680.JPG','images/IMG_3682.JPG' ,'images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3683.JPG','images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3684.JPG','images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3685.JPG','images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3686.JPG']

for x in filename:
    image = cv.imread(x)
    image = cv.resize(image, (960, 540)) 
    #DETECCION DE HUECOS
    result= removeblue.remove_blue(image) 
    tapes = removeblue.detectTapes(image)
    
    cv.imshow('resuldo', result)
    cv.imshow('tapas', tapes)
    cv.waitKey(0)
    cv.destroyAllWindows()
   
    
