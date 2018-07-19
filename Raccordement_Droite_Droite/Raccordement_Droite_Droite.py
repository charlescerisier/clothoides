from tkinter import*
from math import*

#---------------------------------------------------------------------------------------------------------------------
#Affichage

#Fonctions permettant d'afficher les points sur le canvas car ces derniers ne sont pas exprimer en pixels



def scalex(x): 
    return x*(l-30)+30
    
def scaley(y):
    return h-y*(h-30)-30

#Fonctions permettant de recuperer les coordonnes des points dont on connait la position en pixels sur le canvas
def sclx(x):
    return (x-30)/(l-30)
def scly(y):
    return (h-30-y)/(h-30)

#Fonctions permettant de bouger les points I et D sur le canvas
def start_move(event):
    global moving,mousex,mousey,xi,l,h,d,xd,yd
    if (event.x>(scalex(xi)-10) and event.x<(scalex(xi)+10) and event.y>h-40 and event.y<h-20) \
    or (event.x>(scalex(xd)-5) and event.x<(scalex(xd)+5) and event.y>scaley(yd)-5 and event.y<scaley(yd)+5 ):
        moving=1
        mousex=event.x
        mousey=event.y
    else : 
        moving=0

def move(event):

    global mousex,mousey,moving,xi,yi,xd,yd,l,h,d
    if moving and event.x>30 and event.y>h-d-30:
        can.move("pointI",event.x-mousex,0)

        mousex=event.x
        xi=sclx(mousex)
    elif moving and event.x>30 and event.y<h-d-30:
        can.move("pointD",event.x-mousex,event.y-mousey)
        mousex,mousey=event.x,event.y
        xd,yd=sclx(mousex),scly(mousey)

def stop_move(event):
    global moving
    moving=0
    angle()
#---------------------------------------------------------------------------------------------------------------------------------
#Calcul

    
def angle(): #Fonction qui permet de calcuer l'angle entre les 2 droites que l'on veut raccorder
    global xi,xd,yi,yd,alpha,xk,yk
    if xd==xi:
        return
    if xi>xd:
        alpha=pi-(atan((yd-yi)/(xi-xd)))
        alphadeg=alpha*(180/pi)
        alphadeg=round(alphadeg,1)
        can.delete("alpha")
        can.create_text(scalex(xi)-5,scaley(yi)+8,text=("α=",alphadeg),tag="alpha")
        xk=xi-2*cos((pi-alpha)/2)
        yk=2*sin((pi-alpha)/2)
        can.create_oval(scalex(xk)-3,scaley(yk)-3,scalex(xk)+3,scaley(yk)+3,fill="yellow",tag="alpha")

    else:
        alpha=(atan((yd-yi)/(xd-xi)))
        alphadeg=alpha*(180/pi)
        alphadeg=round(alphadeg,1)
        can.delete("alpha")
        can.create_text(scalex(xi)-5,scaley(yi)-8,text=("α=",alphadeg),tag="alpha")
        xk=xi-2*cos((pi-alpha)/2)
        yk=2*sin((pi-alpha)/2)
        can.create_oval(scalex(xk)-3,scaley(yk)-3,scalex(xk)+3,scaley(yk)+3,fill="yellow",tag="alpha")
    
    can.delete("segment")
    can.create_line(scalex(xi),scaley(yi),scalex(xd),scaley(yd),fill="blue", tag="segment")
    can.create_line(scalex(xd),scaley(yd),scalex(xi+2*cos(alpha)),scaley(2*sin(alpha)),fill="blue", tag="segment")

    can.create_line(scalex(xi),scaley(yi),scalex(xk),scaley(yk),tag="segment",fill="orange")
    param(alpha)
    
#Fonction qui permet de trouver la symetrie orthogonale de C par rapport à la droite (AB)
def symetrie(A,B,C):
    u0=B[0]-A[0]
    u1=B[1]-A[1]
    u=(u0,u1 )

    v0=C[0]-A[0]
    v1=C[1]-A[1]
    v=(v0,v1)

    #w est le projeté orthogonal sur u orthogonal
    w0=B[1]-A[1]
    w1=A[0]-B[0]
    w=(w0,w1)

    p0=((w0*v0+w1*v1)*w0)/(w0**2+w1**2)
    p1=((w0*v0+w1*v1)*w1)/(w0**2+w1**2)
    p=(p0,p1)

    s0=C[0]-2*p0
    s1=C[1]-2*p1
    s=(s0,s1)
    return s

#Fonctions permettant de touver les paramètre q,A,tm de la clothoide
def intc(t):
    q=1
    somme=1
    for n in range(50):
        q=(q*(-t**2*(4*n+1)))/((2*n+1)*(2*n+2)*(4*n+5))
        somme+=q
    return somme

def ints(t):
    global r
    q,somme=t/3,t/3
    for n in range(50):
        q=(q*(-t**2*(4*n+3)))/((2*n+2)*(2*n+3)*(4*n+7))
        somme+=q
    return somme


#Fonctions qui permettent de tracer la clothoide avec les paramètres calculer précedemment 
def intc2(t):
    global A
    q=t
    somme=t
    for n in range(50):
        q=-q*(A/2)**2*t**4*(4*n+1)/((2*n+1)*(2*n+2)*(4*n+5))
        somme+=q
    return somme


def ints2(t):
    global r,A
    q,somme=(A/2)*(t**3)/3,(A/2)*(t**3)/3
    for n in range(50):
        q=-q*(A/2)**2*t**4*(4*n+3)/((2*n+2)*(2*n+3)*(4*n+7))
        somme+=q
    return somme


#Fonction qui permet de calculer les paramètres de la clothoide
def param(alpha):
    global xk,yk,xi,yi
    global xi,R,A,tm,t0
    betta=(pi-alpha)/2
    gamma=pi/2-betta
    R=(tan(betta)*xi)/(2*gamma*(ints(gamma)+tan(betta)*intc(gamma)))
    A=1/(2*gamma*R**2)
    tm=2*gamma*R
    t0=0
    showclothoide()
 
#Fonction permettant d'afficher la clothoide   
def showclothoide():
    global q,A,tm,t0,xk,yk,xi,yi
    can.delete("clothoide")
    while t0<=tm:
        can.delete("pointK")
        x=intc2(t0)
        y=ints2(t0)
        S=symetrie((xk, yk), (xi, yi), (x, y)) #symétrie orthogonale de la demis-clothoide par rapport à la bisectrice
        xs,ys=S[0],S[1]

        if t0!=0:
            can.create_line(scalex(x),scaley(y),scalex(xcl),scaley(ycl),tag="clothoide",fill="blue")
            can.create_line(scalex(xs),scaley(ys),scalex(xs2),scaley(ys2),tag="clothoide",fill="red")
        xcl,ycl=x,y
        xs2,ys2=xs,ys
        can.create_oval(scalex(x)-3,scaley(y)-3,scalex(x)+3,scaley(y)+3,fill="yellow",tag="pointK")
        can.create_text(scalex(xk)-7,scaley(yk)-7,text="K")
        t0+=0.001


    

    


#-------------------------------------------------------------------------------------------------------------------------------------------------
#Interface Tkinter 

h=600 #hauteur du canvas
l=600 #largeur du canvas
d=30  #decalge du à l'axe
fen=Tk()
fen.title("Raccordement Droite Droite")
fen.geometry("600x600")
fen.resizable(width=False,height=False)
can=Canvas(fen,width=640,height=600,bg="light grey")
can.pack(side=LEFT)
toolbox=Canvas(fen,width=100,height=600,bg="white")
toolbox.pack()

#Affichage des axes 
can.create_line(d,0,d,h)
can.create_line(0,h-d,l,h-d)
can.create_line(d,2,20,12)
can.create_line(d,2,40,12)
can.create_line(l,h-d,590,560)
can.create_line(l,h-d,590,580)
can.create_oval((28,568,32,572),fill="black")


#Point I
global xi
xi=0.8
yi=0
can.create_oval((scalex(xi)-2,h-32,scalex(xi)+2,h-28),fill="green",tag="pointI",outline="green")

#Point D
xd=0.6
yd=0.4
i=can.create_oval(scalex(xd)-3,scaley(yd)-3,scalex(xd)+3,scaley(yd)+3,fill="red",tag="pointD")
can.create_text(xd,yd-8,text=("(",xd-d,h-yd-d,")"),tag="posxd")

angle()

can.bind("<ButtonPress>",start_move)
can.bind("<Button1-Motion>",move)
can.bind("<ButtonRelease>",stop_move)


fen.mainloop()
 