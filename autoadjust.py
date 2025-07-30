import cv2
import numpy as np
import skimage as sk
   
##Este va a ser el final para ajustar la imagen a lo que necesito en luz y eliminacion
#de basura 
def autoadjustbrigandconst(image,exeromn,exeromx):
    global frame_out
    img1 = image.copy()
    img2 = image.copy()
    img3= image.copy()
    #frame_out = image.copy()
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    im = sk.exposure.rescale_intensity(img, in_range=(35, 165))
    
    #Eleva el contraste e incrementa las tonalidades claras 
    seed_fill = np.copy(im)
    seed_fill[1:-1, 1:-1] = im.max()
    mask_fill = im
    filled_image = sk.morphology.reconstruction(seed_fill, mask_fill, method='erosion')
    ##Convertir de formato Flotante a Entero y convirtiendo el formato de skimage para opencv
    filim = img - filled_image
    fill = np.copy(filim).astype(np.uint8)
    cvimg = sk.util.img_as_ubyte(fill)
    cvimg = cv2.blur(cvimg,(3,3))
    #Buscando aislar el paquete del fondo
    _, th = cv2.threshold(cvimg, None, 255, cv2.THRESH_OTSU)
    con, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #draw = cv2.drawContours(img3,con,-1,(255,0,0), 2)
    
    large_contours = [cnt for cnt in con if cv2.contourArea(cnt) > 2000]
    
    #Tomando el contorno mas grande (El Paquete)
    #Dato curioso skimage invierte las coordenadas del formato Opencv x=y y=X
    for cnt in large_contours:
        x,y,h,w = cv2.boundingRect(cnt)
        yend = y+w
        xend = x+h
        x = x -25
        frame = img3[x:yend,y:xend]
    
    newfrgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    newfrgray = sk.exposure.rescale_intensity(newfrgray, in_range=(5, 185))
        
    seed = np.copy(newfrgray)
    seed[2:-1, 3:-1] = newfrgray.min()
    mask = newfrgray
    filled = sk.morphology.reconstruction(seed, mask, method='dilation')
    ##Convertir de formato Flotante a Entero y convirtiendo el formato de skimage para opencv
    filim2 = newfrgray - filled
    fill2 = np.copy(filim2).astype(np.uint8)
    cvimg2 = sk.util.img_as_ubyte(fill2)
    
        
    return frame,cvimg2

frame_out = None