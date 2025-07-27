import numpy as np
import cv2
import removeblue
import distances
import failseal
import autoadjust as au
#import RPi.GPIO as GPIO
import configparser
import sys
from tkinter import *
from PIL import ImageTk, Image


def start():
    global cap
    cap = cv2.VideoCapture(0)
    show()
    
def readValues():
    global doslid,per,bl1,thhue,norhue,kerhue,rXmin,rXmax,rYmin,rYmax,iters,armax,armin
    conf = configparser.ConfigParser()
    conf.read('config.ini') 
    ##Ajuste de brillo precarga de valores   
    doslid.set(conf.get('Brigness', 'Limit'))
    per.set(conf.get('Brigness', 'darkness'))
    bl1.set(conf.get('Brigness', 'Blurred'))
    rXmin.insert(0,conf.get('Brigness', 'RXMin'))
    rXmax.insert(0,conf.get('Brigness', 'RXMax'))
    rYmin.insert(0,conf.get('Brigness', 'RYmin'))
    rYmax.insert(0,conf.get('Brigness', 'RYMax'))
    thhue.set(conf.get('Cuts', 'Th1val'))
    norhue.set(conf.get('Cuts', 'NormalizeVal'))
    kerhue.set(conf.get('Cuts', 'kernel'))
    iters.insert(0, conf.get('Cuts','Iteraciones'))
    armin.insert(0, conf.get('Cuts','areaminima'))
    armax.insert(0, conf.get('Cuts','areamaxima'))

def adjus():
    global ap,bril,hueco,estruct,tapa
    ap = 0
    bril.grid(column=2, row=1,columnspan=3, rowspan=6)
    hueco.grid_forget()
    estruct.grid_forget()
    tapa.grid_forget()
    

def hue():
    global ap,bril,hueco,estruct,tapa
    ap = 1
    hueco.grid(column=2, row=1,columnspan=5, rowspan=6)
    bril.grid_forget()
    estruct.grid_forget()
    tapa.grid_forget()

def tapas():
    global ap
    ap = 2
    tapa.grid(column=2, row=1,columnspan=3, rowspan=6)
    bril.grid_forget()
    estruct.grid_forget()
    hueco.grid_forget()

def struc():
    global ap
    ap = 3
    estruct.grid(column=2, row=1,columnspan=3, rowspan=6)
    bril.grid_forget()
    hueco.grid_forget()
    tapa.grid_forget()

def hueth():
    global ap
    ap = 4

def huenorm():
    global ap
    ap = 5
    
def hueerosi():
    global ap
    ap = 6
    
def huecont():
    global ap
    ap = 7

def save():
    global doslid,per,bl1,thhue,norhue,kerhue,rXmin,rXmax,rYmin,rYmax,iters,armax,armin
    conf = configparser.ConfigParser()
    if rXmin:
        try:rxmn = int(rXmin.get())
        except:rxmn = 0
    else:rxmn = 0
    if rXmax:
        try:rxmx = int(rXmax.get())
        except: rxmx = 960
    else: rxmx = 960
    if rYmin:
        try:rymn = int(rYmin.get())
        except:rymn = 0
    else:rymn = 0
    if rYmax:
        try:rymx = int(rYmax.get())
        except: rymx = 540
    else: rymx = 540
    if iters:
        try:iterss = int(iters.get())
        except:iterss = 1
    if armax:
        try: armx = int(armax.get())
        except: armx = 20000
    if armin:
        try: armn = int(armin.get())
        except: armn = 800
    conf['Brigness'] = {'Limit': int(doslid.get()), 'darkness': float(per.get()),
                        'Blurred': int(bl1.get()),'RXMin': rxmn, 'RXMax': rxmx,
                        'RYmin': rymn, 'RYMax': rymx}
    conf['Cuts'] = {'Th1val': int(thhue.get()), 'NormalizeVal': int(norhue.get()),
                    'Iteraciones': iterss, 'Kernel': int(kerhue.get()), 'AreaMinima':armn, 
                    'AreaMaxima': armx}
    with open('config.ini', 'w') as configfile:
        conf.write(configfile)
    
def show():
    global cap, limdown, doslid, per, images, bl1, rYmax,rYmin,rXmax, rXmin, ap,thhue,norhue, iters,kerhue
    global armin,armax
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.resize(frame, (960,540))
            adj = au.autoadjustbrigandconst(frame)
            ##Control de brillos
            limdown = int(doslid.get())  
            porcent = float(per.get())
            porcentreal = 0.0
            rymn = 0 
            rymx = 0
            if porcent > 0:porcentreal = porcent / 100.0  
            porblu = int(bl1.get())
            if rYmin and rYmax:
                try:
                    r1 = int(rYmin.get())
                    r2 = int(rYmax.get())
                    if r2 > r1:
                        rymn = int(rYmin.get())
                        rymx = int(rYmax.get())
                    else:
                        rymn = 0
                        rymx = 540
                except:
                    rymn = 0
                    rymx = 540
            if rXmin and rXmax:
                try:
                    r3 = int(rXmin.get())
                    r4 = int(rXmax.get())
                    if r4 > r3:
                        rxmn = int(rXmin.get())
                        rxmx = int(rXmax.get())
                    else:
                        rxmn = 0
                        rxmx = 960
                except:
                    rxmn = 0
                    rxmx = 960
            i = distances.distancemask(adj, limdown, porcentreal, porblu, rymn, rymx,rxmn, rxmx)
            #Deteccion de Huecos en el paquete
            thval = int(thhue.get())
            normva = int(norhue.get())
            if iters:
                try:iterss = int(iters.get())
                except:iterss = 1
            
            kern = int(kerhue.get())
            if armin:
                try:aremin = int(armin.get())
                except:aremin = 800
            if armax:
                try:aremax = int(aremax.get())
                except:aremax = 20000
            huecos, th,norm,eros,const = removeblue.remove_blue(i,thval,normva,iterss,
                                                                kern,aremin,aremax)
            tapas, mask = removeblue.detectTapes(i)
            nostruc = distances.isdestructured(mask, i)
            images = [i,huecos,tapas,nostruc,th,norm,eros,const]
            im = Image.fromarray(images[ap])
            img = ImageTk.PhotoImage(image=im)
            vid.configure(image=img)
            vid.image = img
            vid.after(10, show)
        else:vid.image = "",cap.release() 
 

def end():
    global cap
    cap.release()
    

    
cap = None
limdown = 174
images = []
ap = 0
root = Tk()
root.title("Inicio Configuracion de Sistema Vision")
doslid = DoubleVar()
per = DoubleVar()
bl1 = DoubleVar()
thhue = DoubleVar()
norhue = DoubleVar()
kerhue = DoubleVar()

btnIniciar = Button(root, text="Iniciar", width=45, command=start)
btnIniciar.grid(column=0, row=0, padx=5, pady=5)
bril = Frame(root)
bril.grid(column=2, row=1,columnspan=3, rowspan=6)
hueco = Frame(root)
tapa = Frame(root)
estruct = Frame(root)
btnFinalizar = Button(root, text="Finalizar", width=45, command=end)
btnFinalizar.grid(column=1, row=0, padx=5, pady=5)
btnBrig = Button(root, text="Ajustar brillo", width=45, command=adjus)
btnBrig.grid(column=0, row=8, padx=5, pady=5)
btnHuec = Button(root, text="huecos", width=45, command=hue)
btnHuec.grid(column=1, row=8, padx=5, pady=5)
btnTaps = Button(root, text="Cantidad botellas", width=45, command=tapas)
btnTaps.grid(column=2, row=8, padx=5, pady=5)
btnStruct = Button(root, text="Estructura", width=45, command=struc)
btnStruct.grid(column=3, row=8, padx=5, pady=5)
btnSave = Button(root, text="Guardar", width=20,command=save)
btnSave.grid(column=3, row=0)

vid = Label(root)
vid.grid(column=0, row=1, columnspan=2, rowspan=7)
##Pantalla 1
adjdowlim = Scale(bril, from_=0, to=255,orient=HORIZONTAL,label="Ajustar Eliminacion de Brillos",
            length=200, resolution=1,variable=doslid)
adjdowlim.grid(column=0, row=0, padx=5,pady=5)
percent = Scale(bril, from_=0, to=100,orient=HORIZONTAL,label="Porcentaje de oscurecimiento",
                length=200, resolution=1,variable=per)
percent.grid(column=0, row=1, padx=5,pady=5, ipadx=1)
difu = Scale(bril, from_=2, to=50,orient=HORIZONTAL,label="Blur",
                length=200, resolution=1,variable=bl1)
difu.grid(column=0, row=3, padx=5,pady=5)

mnrxlbl = Label(bril, text="Recorte minimo en X")
mxrxlbl = Label(bril, text="Recorte maximo en X")
rXmin = Entry(bril)
rXmax = Entry(bril)
mnrxlbl.grid(column=0,row=4)
rXmin.grid(column=0, row=5)
mxrxlbl.grid(column=1,row=4)
rXmax.grid(column=1, row=5)
mnrylbl = Label(bril, text="Recorte minimo en Y")
mxrylbl = Label(bril, text="Recorte maximo en Y")
mnrylbl.grid(column=0,row=6)
mxrylbl.grid(column=1,row=6)
rYmin = Entry(bril)
rYmax = Entry(bril)
rYmin.grid(column=0, row=7)
rYmax.grid(column=1, row=7)

##Pantalla2
btnthhue = Button(hueco, text="Threshold", command=hueth)
btnthhue.grid(column=0,row=0)
btnnormhue = Button(hueco, text="Normalize", command=huenorm)
btnnormhue.grid(column=1,row=0)
btnerohue = Button(hueco, text="Erosion", command=hueerosi)
btnerohue.grid(column=2,row=0)
btnconhue = Button(hueco, text="Contornos", command=huecont)
btnconhue.grid(column=3,row=0)
btnhuec = Button(hueco, text="huecos", command=hue)
btnhuec.grid(column=4, row=0)
thre = Scale(hueco,from_=0, to=255,orient=HORIZONTAL,label="Ajustar Threshold",
            length=250, resolution=1,variable=thhue )
thre.grid(column=0, row=1,columnspan=3)
norre = Scale(hueco,from_=0, to=255,orient=HORIZONTAL,label="Ajustar Normalize MinMax",
            length=250, resolution=1,variable=norhue )
norre.grid(column=0, row=2,columnspan=3)
kere = Scale(hueco,from_=1, to=255,orient=HORIZONTAL,label="Ajustar Kernel Erosion",
            length=250, resolution=1,variable=kerhue )
kere.grid(column=0, row=3,columnspan=3)
lblite = Label(hueco,text="Iteraciones erosion")
lblite.grid(column=1,row=4)
iters = Entry(hueco)
iters.grid(column=1,row=5)
lblarmax = Label(hueco,text="Area maxima huecos")
lblarmax.grid(column=1,row=6)
armax = Entry(hueco)
armax.grid(column=1,row=7)
lblarmin = Label(hueco,text="Iteraciones erosion")
lblarmin.grid(column=1,row=8)
armin = Entry(hueco)
armin.grid(column=1,row=9)

##Pantalla3

root.rowconfigure(0,weight=1)
root.rowconfigure(2,weight=1)
root.rowconfigure(3,weight=1)
root.rowconfigure(4,weight=1)
root.rowconfigure(5,weight=1)
root.rowconfigure(6,weight=1)
root.rowconfigure(7,weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)
root.columnconfigure(6, weight=1)


if __name__ == "__main__":
    start()
    readValues()
    root.mainloop()