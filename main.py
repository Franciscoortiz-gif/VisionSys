import numpy as np
import cv2
import removeblue
import distances
import failseal
import autoadjust as au
#import RPi.GPIO as GPIO
import sys
from tkinter import *
from PIL import ImageTk, Image


def start():
    global cap
    cap = cv2.VideoCapture(0)
    show()
    
def show():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.resize(frame, (960,540))
            adj = au.autoadjustbrigandconst(frame)
            i = distances.distancemask(adj)
            im = Image.fromarray(i)
            img = ImageTk.PhotoImage(image=im)
            vid.configure(image=img)
            vid.image = img
            vid.after(10, show)
            print("termino")
        else:
            vid.image = ""
            cap.release() 
            print("fallo")
            

def end():
    global cap
    cap.release()
    
cap = None
root = Tk()

btnIniciar = Button(root, text="Iniciar", width=45, command=start)
btnIniciar.grid(column=0, row=0, padx=5, pady=5)

btnFinalizar = Button(root, text="Finalizar", width=45, command=end)
btnFinalizar.grid(column=1, row=0, padx=5, pady=5)

vid = Label(root)
vid.grid(column=0, row=1, columnspan=2)


if __name__ == "__main__":
    start()
    root.mainloop()