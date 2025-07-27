import cv2
import numpy as np

fina = None

def autoadjustbrigandconst(image):
    img = image.copy()
    amax = 180
    amin = 0
    
    alow = img.min()
    ahigh = img.max()
    # calculate alpha, beta
    alpha =((amax - amin) / (ahigh - alow))
    beta = amin - alow * alpha
    # perform the operation g(x,y)= α * f(x,y)+ β
    new_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    
    yb = cv2.cvtColor(new_img, cv2.COLOR_BGR2YCrCb)
    y,Cr,Cb = cv2.split(yb)
    ysrt = cv2.normalize(y,None,0,160,cv2.NORM_MINMAX)
    imyc = cv2.merge([ysrt,Cr,Cb])
    im1 = cv2.cvtColor(imyc, cv2.COLOR_YCrCb2BGR)
    return im1

