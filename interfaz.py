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
    global cap, onceopr
    onceopr = False
    cap = cv2.VideoCapture(2)
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
    hueco.grid(column=2, row=1,columnspan=5, rowspan=12)
    bril.grid_forget()
    estruct.grid_forget()
    tapa.grid_forget()

def captu():
    global adj, capture
    capture = adj.copy()
    

def tapass():
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
    global armin,armax, norhue2, capture
    global onceopr, name
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            
            name += 1
            cv2.imwrite("images/"+str(name)+".png", frame)
            """limdown = int(doslid.get())  
            if rYmin and rYmax:
                try:
                    r1 = int(rYmin.get())
                    r2 = int(rYmax.get())
                    if r2 > r1:
                        #Valores de la exposicion de la erosion de autorecorte
                        experomin = int(rYmin.get())
                        experomax = int(rYmax.get())
                    else:
                        experomin = 35
                        experomax = 165
                except:
                    experomin = 35
                    experomax = 165
            ##Control de brillos
            #adj = au.autoadjustbrigandconst(frame,experomin,experomax)
            
            #Deteccion de Huecos en el paquete
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
            
            thhh = float(thhue.get())
            thhh2 = float(norhue.get())"""
            """if onceopr == False:
                huecos, cont= removeblue.remove_blue(adj, thhh, thhh2)
                tapas, mask, p3blu1, p3th1,p3blu2,p3con = removeblue.detectTapes(adj)
                nostruc = distances.isdestructured(mask, adj)
                capture = adj.copy()
                onceopr = True
        
            if capture is not None:
                huecos, cont = removeblue.remove_blue(capture, thhh, thhh2)
                tapas, mask, p3blu1, p3th1,p3blu2,p3con = removeblue.detectTapes(capture)
                nostruc = distances.isdestructured(mask, capture)
            
            
            images = [adj,huecos,tapas,nostruc,p3blu1,p3th1,mask,p3blu2,p3con]
                
            im = Image.fromarray(images[ap])
            img = ImageTk.PhotoImage(image=im)
            
            vid.configure(image=img)
            vid.image = img
            m = Image.fromarray(cont)
            img1 = ImageTk.PhotoImage(image=m)
            
            vid2.configure(image=img1)
            vid2.image = img1
            vid.after(100, show)"""
            
        else:vid.image = "",cap.release() 
    else:
        image = cv2.imread("images/1.png")

def end():
    global cap
    cap.release()
    

    
cap = None
name = 0
limdown = 174
capture = None
images = []
onceopr = False
ap = 0
root = Tk()
root.title("Inicio Configuracion de Sistema Vision")
doslid = DoubleVar()
per = DoubleVar()
bl1 = DoubleVar()
thhue = DoubleVar()
norhue = DoubleVar()
norhue2 = DoubleVar()
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
btnTaps = Button(root, text="Cantidad botellas", width=45, command=tapass)
btnTaps.grid(column=2, row=8, padx=5, pady=5)
btnStruct = Button(root, text="Estructura", width=45, command=struc)
btnStruct.grid(column=3, row=8, padx=5, pady=5)
btnSave = Button(root, text="Guardar", width=20,command=save)
btnSave.grid(column=3, row=0)
btncap = Button(root, text="Capturar", width=20,command=captu)
btncap.grid(column=4, row=0)

vid = Label(root)
vid.grid(column=0, row=1, columnspan=3, rowspan=3)
vid2 = Label(root)
vid2.grid(column=0, row=4, columnspan=3, rowspan=3)
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

mnrxlbl = Label(bril, text="Minimo erosion de autorecorte")
mxrxlbl = Label(bril, text="Maximo erosion de autorecorte")
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

btnhuec = Button(hueco, text="huecos", command=hue)
btnhuec.grid(column=4, row=0)
thre = Scale(hueco,from_=0, to=255,orient=HORIZONTAL,label="Ajustar Threshold",
            length=250, resolution=1,variable=thhue )
thre.grid(column=0, row=1,columnspan=3)
norre = Scale(hueco,from_=0, to=255,orient=HORIZONTAL,label="Ajustar Normalize MinMax",
            length=250, resolution=1,variable=norhue )
norre.grid(column=0, row=2,columnspan=3)
norre2 = Scale(hueco,from_=0, to=255,orient=HORIZONTAL,label="Ajustar Normalize MinMax",
            length=250, resolution=1,variable=norhue2 )
norre2.grid(column=0, row=3,columnspan=3)
kere = Scale(hueco,from_=1, to=255,orient=HORIZONTAL,label="Ajustar Kernel Erosion",
            length=250, resolution=1,variable=kerhue )
kere.grid(column=0, row=4,columnspan=3)
lblite = Label(hueco,text="Iteraciones erosion")
lblite.grid(column=1,row=5)
iters = Entry(hueco)
iters.grid(column=1,row=6)
lblarmax = Label(hueco,text="Area maxima huecos")
lblarmax.grid(column=1,row=7)
armax = Entry(hueco)
armax.grid(column=1,row=8)
lblarmin = Label(hueco,text="Iteraciones erosion")
lblarmin.grid(column=1,row=9)
armin = Entry(hueco)
armin.grid(column=1,row=10)

##Pantalla3

btnTaps1 = Button(tapa, text="Botellas", command=tapass)
btnTaps1.grid(column=5, row=0)

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