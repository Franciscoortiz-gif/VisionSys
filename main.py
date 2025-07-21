import numpy as np
import cv2 as cv
import removeblue
import distances
import failseal
import autoadjust
#import RPi.GPIO as GPIO
import sys

filename = ['images/IMG_3677.JPG','images/IMG_3680.JPG','images/IMG_3682.JPG' ,'images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3681.JPG','images/IMG_3685.JPG','images/IMG_3686.JPG']

for x in filename:
    
    image = cv.imread(x)
    image = cv.resize(image, (960, 540)) 
    if image is not None:
        adj = autoadjust.autoadjustbrigandconst(image)
        #Imagen recortada a solo lo que me importa
        dist,di = distances.distancemask(adj)
        #DETECCION DE HUECOS
        result, th = removeblue.remove_blue(dist) 
        #Deteccion de cuantos galones hay
        tapes, masktapes = removeblue.detectTapes(dist)
        
        structered = distances.isdestructured(masktapes, dist) 
        failsea = failseal.seilfailed('images/bottle2.png', dist)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        if tapes is not None:
            tapas = tapes
        else:
            tapas = image
        
        
        cv.imshow('resuldo', result)
        cv.imshow('tapas'+' Botellas encontradas', tapas)
        cv.imshow('Is Structured', structered)
        cv.imshow('hueco', th)
        #cv.imshow('Is Fail Seal', failsea)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        print("No se encontro ninguna imagen")
        sys.exit()
    
    
    
   
    
