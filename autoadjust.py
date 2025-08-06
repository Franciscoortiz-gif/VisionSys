import cv2
import numpy as np
import skimage as sk
import diplib as dip
   
##Este va a ser el final para ajustar la imagen a lo que necesito en luz y eliminacion
#de basura 
def autoadjustbrigandconst(image):
    #CV2
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgl = 255-img
    seed = np.copy(imgl)
    seed[1:-1, 1:-1] = imgl.max()
    mask = imgl
    filled = sk.morphology.reconstruction(seed, mask, method='erosion')
    fill = np.array(filled).astype(np.uint8)
    im1 = fill - imgl
    iml2 = np.asarray(im1).astype(np.uint8)
    #DIPLIB
    gra = dip.ColorSpaceManager.Convert(iml2, 'grey')
    gra.SetPixelSize(1,"um")
    blur = dip.Gauss(gra, sigmas=np.array([2.0]))
    th = dip.BackgroundThreshold(blur, distance=7.85, sigma=4.95)
    th = dip.EdgeObjectsRemove(th)
    th = dip.Label(th, minSize=30)
    m = dip.MeasurementTool.Measure(th,gra,['Size', 'Solidity'])
    sel = m['Size'] > 1500 
    larobj = sel.Apply(th)
    #CV2
    outwater = np.array(larobj).astype(np.uint8) * 255
    man = cv2.bitwise_and(image, image,mask=outwater)
    ma = cv2.cvtColor(man, cv2.COLOR_BGR2GRAY)
    ker = np.array([9,9]).astype(np.uint8)
    fin = cv2.erode(ma, ker, iterations=5)
    fin2 = cv2.inRange(fin, 80 ,255)  
    di = np.array(fin2).astype(np.uint8)
    digra = dip.ColorSpaceManager.Convert(di, 'grey')
    th = dip.OtsuThreshold(digra)
    tt = dip.EdgeObjectsRemove(th)
    tt = dip.EdgeObjectsRemove(tt)
    tt = dip.Label(tt, minSize=30)
    mea = dip.MeasurementTool.Measure(tt, digra,['Size', 'Solidity'])
    sel1 = mea['Size'] > 1500 
    logsw = sel1.Apply(tt) 
    finn = np.array(logsw).astype(np.uint8) * 255
    dil = cv2.dilate(finn, ker, iterations=3)
    man1 = cv2.bitwise_and(image, image,mask=dil)
    return man1
