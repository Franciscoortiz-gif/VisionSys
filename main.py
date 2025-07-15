import numpy as np
import cv2 as cv
import removeblue
import distances

filename = ['images/IMG_3677.JPG','images/IMG_3680.JPG','images/IMG_3682.JPG' ,'images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3683.JPG','images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3684.JPG','images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3685.JPG','images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3686.JPG']

for x in filename:
    image = cv.imread(x)
    image = cv.resize(image, (960, 540)) 
    #DETECCION DE HUECOS
    result= removeblue.remove_blue(image) 
    #Deteccion de cuantos galones hay
    tapes, i = removeblue.detectTapes(image)
    
    dist = distances.distancemask(image)
    
    if tapes is not None:
        tapas = tapes
    else:
        tapas = image
    
    bote = str(i)
    
    cv.imshow('resuldo', result)
    cv.imshow('tapas'+' Botellas encontradas' + bote, tapas)
    cv.imshow('Distancia', dist)
    cv.waitKey(0)
    cv.destroyAllWindows()
   
    
