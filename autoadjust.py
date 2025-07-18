import cv2
import numpy as np

def autoadjustbrigandconst(image):
    img = image.copy()
    amax = 160
    amin = 0


    
    alow = img.min()
    ahigh = img.max()
    # calculate alpha, beta
    alpha =((amax - amin) / (ahigh - alow))
    beta = amin - alow * alpha
    # perform the operation g(x,y)= α * f(x,y)+ β
    new_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    img2 = cv2.cvtColor(new_img, cv2.COLOR_BGR2YCrCb)
    y_channel, cr_channel, cb_channel = cv2.split(img2)
    
    # Perform contrast stretch on the Y channel
    y_channel_stretched = cv2.normalize(y_channel, None, 0, 160, cv2.NORM_MINMAX)
    
    # Merge the stretched Y channel back with Cr and Cb channels
    contrast_stretched_ycrcb = cv2.merge([y_channel_stretched, cr_channel, cb_channel])
    
    # Convert the image back from YCrCb to BGR color space
    contrasted = cv2.cvtColor(contrast_stretched_ycrcb, cv2.COLOR_YCrCb2BGR)
    
    imgc = contrasted.copy()
    yuvimg = cv2.cvtColor(imgc, cv2.COLOR_BGR2YUV)
    y, u,v =cv2.split(yuvimg)
    chanels = [y,u,v]
    his = cv2.equalizeHist(chanels[0],chanels[0])
    fin = cv2.merge(chanels[0], contrasted)

    return fin
