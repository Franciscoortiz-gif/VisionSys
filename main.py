import cv2
import skimage as sk
import diplib as dip
import autoadjust as aut
import removeblue as rm
import distances as ds
import matplotlib.pyplot as plt

def start():
    global cap
    cap = cv2.VideoCapture(0)

def main1():
    global cap
    # ret, image = cap.read()
def main():
    imag = cv2.imread("images/4.png")
    
    if imag is not None:
        img = cv2.resize(imag,(700,450))
        img1 = img.copy()
        adj = aut.autoadjustbrigandconst(img1)
        #hueco = rm.remove_blue(adj, img1)
        tapas = rm.detectTapes(adj, img1)
        cv2.imshow("Ajuste", adj)
        #cv2.imshow("Hueco", hueco)
        cv2.imshow("Tapas", tapas)
        
            
    
    
cap = None        
    
def mainloop():
    while ((cv2.waitKey(0)) & (0xFF)) != ord('q'):
        main()    
              
if __name__ == "__main__":
    mainloop()  
