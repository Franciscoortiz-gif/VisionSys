import numpy as np
import cv2 as cv
import removeblue

filename = ['images/bottle1.jpeg','images/bottle2.jpeg','images/bottle3.jpeg','images/bottle4.jpeg','images/IMG_3677.JPG','images/IMG_3680.JPG','images/IMG_3682.JPG' ,'images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3683.JPG','images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3684.JPG','images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3685.JPG','images/IMG_3683.JPG', 'images/IMG_3684.JPG','images/IMG_3686.JPG']

for x in filename:
    image = cv.imread(x)
    image = cv.resize(image, (960, 540)) 
    result, imag= removeblue.remove_blue(image) 
    
    cv.imshow('resuldo', result)
    cv.imshow('original', imag)
    cv.waitKey(0)
    cv.destroyAllWindows()
    """  
    img = image.copy()
    kernel = [ [0, -1, 0], [-1, 5, -1], [0, -1, 0] ] #Para ignorar brillos y el plastico
    kernel2 = [ [-3, 12, -3], [-5, 16, -5], [0, 3, 0] ] #Kernel para deteccion de huecos


    kernel = np.array(kernel)
    kernel2 = np.array(kernel2)
    blur = cv.blur(image, (2,2))
    dst = cv.filter2D(image, -1, kernel)
    _, thresh = cv.threshold(dst, 125, 130, cv.THRESH_BINARY_INV)
    

    
    #Deteccion de huecos
      res= cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imshow('grayscale',res)
    cv.waitKey(0)
    cv.destroyAllWindows()
     

    filter2 = cv.filter2D(thresh, -1, kernel2)
    _, th = cv.threshold(filter2, 127, 135, cv.THRESH_BINARY)
    hsv = cv.cvtColor(th, cv.COLOR_BGR2GRAY)
    mask = cv.inRange(hsv, 130, 255) 
    applymask = cv.bitwise_and(th,th,mask=mask)

    cv.imshow('original image', image)

    cv.imshow('thresh', th)
    cv.imshow('white filter', applymask)
     """  
    
