import cv2
import numpy as np
import skimage as sk
import diplib as dip



def remove_blue(imag, realimg):
        img1 = imag.copy()
        cvgra = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        brigg = sk.exposure.adjust_gamma(cvgra, 2)
        p2, p98 = np.percentile(cvgra, (2, 98))
        imgeq = sk.exposure.rescale_intensity(brigg,in_range=(p2,p98))
        contras = sk.exposure.adjust_log(imgeq, 1)
        imgdip = np.asarray(contras).astype(np.uint8)
        #DIPLIB
        graydip = dip.ColorSpaceManager.Convert(imgdip, 'grey')
        blurdip = dip.Gauss(graydip, sigmas=np.array([2.0]))
        th = dip.RangeThreshold(blurdip, 150.0, 155.0)

        fin = np.array(th).astype(np.uint8)* 255
        return fin
        
def detectTapes(image, realimg):

        img = image.copy()
        img2 = image.copy()
        img3 = image.copy()
        frame_out = image.copy()
        #CV2
        labimg = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)
        l,a,b = cv2.split(labimg)
        clane = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(8,8))#Incrementa detalles
        l = clane.apply(l)
        labimg = cv2.merge((l,a,b))
        im = cv2.cvtColor(labimg, cv2.COLOR_LAB2BGR)
        
        gamm = sk.exposure.adjust_gamma(im, 4)
        inv = 255 - gamm
        contr = sk.exposure.adjust_log(inv,1)
        gray  = cv2.cvtColor(contr, cv2.COLOR_BGR2GRAY)
        th = cv2.inRange(gray, 100, 214)
        #DIPLIB
        dipth = np.array(th).astype(np.uint8)
        dpgr = dip.ColorSpaceManager.Convert(dipth, 'grey')
        dth = dpgr > 128
        mea = dip.EdgeObjectsRemove(dth)
        mea = dip.Label(dth, minSize=30)
        m = dip.MeasurementTool.Measure(mea, dpgr, ['Size']) 
        sel = m['Size'] > 1300
        sel.Relabel()
        circa = sel.Apply(mea)
        ms = np.array(circa).astype(np.uint8)*255
        dpgr2 = dip.ColorSpaceManager.Convert(ms, 'grey')
        dth2 = dpgr2 > 128
        ma2 = dip.EdgeObjectsRemove(dth2)
        ma2 = dip.Label(dth2, minSize=30)
        m2 = dip.MeasurementTool.Measure(ma2,dpgr2, ['Size'])
        sel2 = m2['Size'] < 2050
        cal2 = sel2.Apply(ma2)
        m2s = np.array(cal2).astype(np.uint8)*255 
        dpgr3 = dip.ColorSpaceManager.Convert(m2s, 'grey')
        dth3 = dpgr3 > 128
        ma3 = dip.EdgeObjectsRemove(dth3)
        ma3 = dip.Label(dth3, minSize=30)
        m3 = dip.MeasurementTool.Measure(ma3, dpgr3, ['Circularity'])
        sel3 = m3['Circularity'] < 0.4
        fin3 = sel3.Apply(ma3)
        m3s = np.array(fin3).astype(np.uint8)*255 
        cnt, _ = cv2.findContours(m3s, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        shor = sorted(cnt, key=cv2.contourArea, reverse=True)
        for c in shor[:4]:
                (x,y), radius = cv2.minEnclosingCircle(c)
                center = (int(x), int(y))
                radius = int(radius)
                frame = cv2.circle(realimg, center, radius, (255,0,0), 3)
        return frame
    
    
    #(>1300,<2050, Size), (<0.4,Circularity)
                
        
