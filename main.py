import numpy as np
import cv2 as cv
import removeblue

filename = ['bottle1.jpeg','bottle2.jpeg','bottle3.jpeg','bottle4.jpeg']

for x in filename:
    image = cv.imread(x)
    img = image.copy()
    kernel = [ [0, -1, 0], [-1, 5, -1], [0, -1, 0] ] #Para ignorar brillos y el plastico
    kernel2 = [ [-3, 12, -3], [-5, 16, -5], [0, 3, 0] ] #Kernel para deteccion de huecos
    lowerbriggness =  np.array([190,190,190])
    upperbrigness =  np.array([255,255,255])


    hsv1 = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    darkness = cv.inRange(hsv1, lowerbriggness, upperbrigness)
    unbrig = cv.bitwise_and(img, img,mask=darkness)


    kernel = np.array(kernel)
    kernel2 = np.array(kernel2)
    blur = cv.blur(image, (2,2))
    dst = cv.filter2D(image, -1, kernel)
    _, thresh = cv.threshold(dst, 125, 130, cv.THRESH_BINARY_INV)
    

    
    #Deteccion de huecos
    """    res= cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imshow('grayscale',res)
    cv.waitKey(0)
    cv.destroyAllWindows()
    """    

    filter2 = cv.filter2D(thresh, -1, kernel2)
    _, th = cv.threshold(filter2, 127, 135, cv.THRESH_BINARY)
    hsv = cv.cvtColor(th, cv.COLOR_BGR2GRAY)
    mask = cv.inRange(hsv, 130, 255) 
    applymask = cv.bitwise_and(th,th,mask=mask)

    cv.imshow('original image', image)
    cv.imshow('thresh', th)
    cv.imshow('white filter', applymask)
    cv.imshow('sin brillo', unbrig)
    cv.waitKey(0)
    cv.destroyAllWindows()
