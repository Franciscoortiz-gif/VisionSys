import cv2
import numpy as np

def autoadjustbrigandconst(image):
    img = image.copy()
    img3 = image.copy()
    amax = 200
    amin = 0
    kernel = np.ones((5,5), np.uint8)
    
    alow = img.min()
    ahigh = img.max()
    # calculate alpha, beta
    alpha =((amax - amin) / (ahigh - alow))
    beta = amin - alow * alpha
    # perform the operation g(x,y)= α * f(x,y)+ β
    new_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    
    yb = cv2.cvtColor(new_img, cv2.COLOR_BGR2YCrCb)
    y,Cr,Cb = cv2.split(yb)
    ysrt = cv2.normalize(y,None,0,185,cv2.NORM_MINMAX)
    imyc = cv2.merge([ysrt,Cr,Cb])
    im1 = cv2.cvtColor(imyc, cv2.COLOR_YCrCb2BGR)
    gr = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    equa = cv2.equalizeHist(gr)
    imgfin = cv2.cvtColor(equa, cv2.COLOR_GRAY2BGR)
    return imgfin
