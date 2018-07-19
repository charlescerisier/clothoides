from tkinter import*
from math import *
from time import *
from threading import Thread



fen = Tk()
can_width,can_height = 600,600
can=Canvas(fen,width=can_width,height=can_height)
tBox = Label(can,width=20, height=1)
tBox_w= can.create_window(can_width,10, anchor=NE, window=tBox)
can.pack()

anim =False
size = 600

def scalex(x):
    return x*(size)
def scaley(y):
    return can_height-y*(size)

def intc2(t):
    global A
    q=t
    somme=t
    for n in range(50):
        q=-q*t**4*(4*n+1)/((2*n+1)*(2*n+2)*(4*n+5))
        somme+=q
    return somme

def ints2(t):
    global r,A
    q,somme=(t**3)/3,(t**3)/3
    for n in range(50):
        q=-q*t**4*(4*n+3)/((2*n+2)*(2*n+3)*(4*n+7))
        somme+=q
    return somme

def euler(iterat = 55, color="red",x0=0,y0=can_height,pas=0.01, trapeze=False):
    clear_button()
    can.delete("lines")
    time0=time()
    t=0
    iterat = iterat *(0.1/pas)
    tmax = iterat*pas
    x1,x2,y1, y2 = 0,0,0,0

    
    #normalement size devrait valoir 0.1

    while t < tmax :
        
        if trapeze :

            x2 += size*pas*((cos(t**2)+cos((t-pas)**2))/2)
            y2 += -size*pas*((sin(t**2)+sin((t-pas)**2))/2)
            bTrap.config(bg="spring green")

        else :
    
            x2 += size*pas*cos(t**2) 
            y2 += -size*pas*sin(t**2)
            bEuler.config(bg="spring green")


        can.create_line(x0+x1,y0+y1,x0+x2,y0+y2,fill=color,tag="lines")

        x1,y1=x2,y2

        t+=pas
    tf =round(time()-time0,3)
    tBox.config(text="temps : "+ str(tf) + " seconde(s)")
    tBox.update()
    can.update()


def serie_entiere(iterat=100,color="red",size=50,x0=0,y0=can_height,pas=0.1):
    clear_button()
    can.delete("lines")
    bSerie.config(bg="spring green")
    time0=time()

    t=0
    tm = 5.5
    while t<tm:
        x=intc2(t)
        y=ints2(t)
        if t!=0:
            can.create_line(scalex(x),scaley(y),scalex(xcl),scaley(ycl),tag="lines",fill=color)
            #can.create_line(x,y,xcl,ycl,tag="lines",fill=color)
        xcl,ycl=x,y
        t+=0.01




    tf =round(time()-time0,3)
    tBox.config(text="temps : "+ str(tf) + " seconde(s)")
    can.update()

def clear_button():
    for obj in bList:
        obj.config(bg="white")
'''
def start():

    bStart.config(text="STOP ANIMATION")

    while anim :
        euler()
        sleep(1)
        euler(trapeze=True)
        sleep(1)
        serie_entiere()
        sleep(1)
'''
'''
def start():
    i=0
    for i in range(5) : 

        bStart.config(text="STOP ANIMATION")

        euler()
        sleep(1)
        euler(trapeze=True)
        sleep(1)
        serie_entiere()
        sleep(1)
        i+=1
'''
def start():
    global anim
    anim = not anim

    if anim :
        bStart.config(text="STOP ANIMATION")
        anim_thread = Animation()
        anim_thread.start()
    else : 
        bStart.config(text="START ANIMATION")

class Animation(Thread):

    def __init__(self):
        Thread.__init__(Thread)

    def run(self):

        
        while anim :
            euler()
            can.update()
            sleep(1)
            if not anim : 
                break
            euler(trapeze=True)
            can.update()
            sleep(1)
            if not anim : 
                break
            serie_entiere()
            can.update()
            sleep(1)
        del self
    

y_buf_side=10

bEuler = Button(can, width=22,text="EULER",command= lambda : euler(), font="Helvetica 10 bold")
bEuler_w = can.create_window(10, y_buf_side, anchor=NW, window=bEuler)

y_buf_side+=30

bTrap = Button(can, width=22,text="TRAPEZE",command= lambda : euler(trapeze=True), font="Helvetica 10 bold")
bTrap_w = can.create_window(10, y_buf_side, anchor=NW, window=bTrap)

y_buf_side+=30

bSerie = Button(can, width=22,text="SERIE ENTIERE",command= lambda : serie_entiere() , font="Helvetica 10 bold")
bSerie_w = can.create_window(10, y_buf_side, anchor=NW, window=bSerie)

y_buf_side+=40

bStart= Button(can, width=22,text="START ANIMATION",command= lambda : start() , font="Helvetica 10 bold", bg="white")
bStart_w = can.create_window(10, y_buf_side, anchor=NW, window=bStart)

bList = [bEuler, bTrap, bSerie]

clear_button()

fen.mainloop()
