from tkinter import*
from math import*
import time

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#affichage
def posxy(event):
    global h, d
    can.delete("position")
    can.create_text(500,20,text="x={0},y={1}".format(event.x-d,h-event.y-d),tag="position")
    can.create_text(500,40,text="devers={0}".format("2%"),tag="devers")

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


#Fonction qui permet d'afficher un cercle de rayon r
def cercle():
    global r,h,d,l
    can.delete("positioncentre","affichagerayon")

    if r>=0.5*y0 and r<=y0:
        can.delete("cercle")
        can.create_oval(scalex(x0)-2,scaley(y0)-2,scalex(x0)+2,scaley(y0)+2,fill="red",tag="cercle",outline="black")
        can.create_oval(scalex(x0-r),scaley(y0-r),scalex(x0+r),scaley(y0+r),tag="cercle",outline="Black")
        can.create_text(500,60,text=("x0={0} y0={1}".format(scalex(x0)-30,h-scaley(y0)-30)),tag="positioncentre")
        can.create_text(500,80,text=("Rayon : {}".format(r*100)),tag="affichagerayon")
        param()

#Fonctions permettant de bouger le centre du cercle
def start_move(event):
    global moving,mousex,mousey,x0,y0
    if event.x>(scalex(x0)-15) and event.x<(scalex(x0)+15) and event.y>scaley(y0)-15 and event.y<scaley(y0)+15:
        moving=1
        mousex=event.x
        mousey=event.y
    else:
        moving=0

def move(event):
    global mousex,mousey,moving,x0,y0,h,d,l
    if moving and event.x>r*(l-30)+30 and event.x<l-r*(l-30) and event.y<h-r*(h-30)-30 and event.y>h-2*r*(h-30)-30:
        can.move("cercle",event.x-mousex,event.y-mousey)
        mousex=event.x
        mousey=event.y
        x0=(event.x-d)/(l-d)
        y0=(h-d-event.y)/(h-d)

def stop_move(event):
    global moving
    if moving:
        moving=0
        param()

#Lorsque on choisit une vitesse et donc le rayon qui lui est associée, cette fonction permet
#de retourner le rayon que l'on utilisera par la suite ainsi que les limites ou l'on peut placer le centre du cercle sur le
#canvas

def rayon(rayon):
    global r,x0,y0
    r=rayon/100
    can.delete("lim_centre_cercle")
    can.create_line(30, h-r*(h-30)-30, l, h-r*(h-30)-30,tags="lim_centre_cercle")
    can.create_line(30, h-2*r*(h-30)-30, l,h-2*r*(h-30)-30,tags="lim_centre_cercle")
    x0,y0=sclx(30+l/2),scly(h-1.5*r*(h-30)-30)
    can.delete("cercle","clothoide","K")
    cercle()
    can.update()




#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Calcul

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
def intc2(t):#cacul de la composante x de la clothoide par serie entière
    global A
    q=t
    somme=t
    for n in range(50):
        q=-q*(A/2)**2*t**4*(4*n+1)/((2*n+1)*(2*n+2)*(4*n+5))
        somme+=q
    return somme

def ints2(t):#cacul de la composante y de la clothoide par serie entière
    global r,A
    q,somme=(A/2)*(t**3)/3,(A/2)*(t**3)/3
    for n in range(50):
        q=-q*(A/2)**2*t**4*(4*n+3)/((2*n+2)*(2*n+3)*(4*n+7))
        somme+=q
    return somme

#Cette fonction permet la recherche du 0 d'une fonction
def dichotomie(g,a,b,p):
    global approx
    approx=10**(-p)
    while (b-a>=approx):
        m=(a+b)/2
        if (g(a)*g(m))<=0:
            b=m
        else:
            a=m
    return m

#Fonction qui permet de calculer les paramètres de la clothoide
def param():
    global time1
    time1=time.clock()
    global q,A,tm,t0,approx,r,y0,x0,h,d
    f=lambda a: r*cos(a)-y0+2*a*r*ints(a)
    to=dichotomie(f,0,pi,14)

    somme=intc(to)

    q=x0+r*sin(to)-2*to*r*somme
    A=1/(2*to*r**2)
    tm=2*to*r
    t0=0
    showclothoide()

#Fonction permettant d'afficher la clothoide
def showclothoide():
    global q,A,tm,t0
    can.delete("clothoide","K")
    while t0<=tm:
        x=q+intc2(t0)
        y=ints2(t0)
        if t0!=0:
            can.create_line(scalex(x),scaley(y),scalex(xcl),scaley(ycl),tag="clothoide",fill="blue")
        xcl,ycl=x,y
        t0+=0.001
    can.create_oval(scalex(x)-3,scaley(y)-3,scalex(x)+3,scaley(y)+3,fill="yellow",tag="K")
    #can.create_oval(q-3,h-d-3,q+3,h-d+3,fill="yellow",tag="K")
    time2=time.clock()
    print("temps",round(time2-time1,2))



#-------------------------------------------------------------------------------------------------------------------------------------------------
#Interface Tkinter

h=600 #hauteur du canvas
l=600 #largeur du canvas
d=30  #decalge du à l'axe
fen=Tk()
fen.title("Clothoides")
fen.resizable(width=False,height=False)
can=Canvas(fen,width=600,height=600,bg="light grey")
can.pack(side=LEFT)
toolbox=Canvas(fen,width=60,height=600,bg="white")
toolbox.pack()

#On importe les photos
im50=PhotoImage(file="50p.gif")
im70=PhotoImage(file="70p.gif")
im90=PhotoImage(file="90p.gif")
im110=PhotoImage(file="110p.gif")
im130=PhotoImage(file="130p.gif")

#Affichage des boutons
lim50=Button(toolbox,padx=5,pady=5,command= lambda: rayon(10), image = im50)
lim50.pack()
lim70=Button(toolbox,padx=5,pady=5,command= lambda: rayon(20), image = im70)
lim70.pack()
lim90=Button(toolbox,padx=5,pady=5,command= lambda: rayon(30), image = im90)
lim90.pack()
lim110=Button(toolbox,padx=5,pady=5,command= lambda: rayon(35), image = im110)
lim110.pack()
lim130=Button(toolbox,padx=5,pady=5,command= lambda: rayon(40), image = im130)
lim130.pack()

can.create_line(d,0,d,h)
can.create_line(0,h-d,l,h-d)
can.create_line(d,2,20,12)
can.create_line(d,2,40,12)
can.create_line(l,h-d,590,560)
can.create_line(l,h-d,590,580)
can.create_oval((28,568,32,572),fill="black")


global x0,y0
x0=0
y0=0
rayon(30)

can.bind("<ButtonPress>",start_move)
can.bind("<Button1-Motion>",move)
can.bind("<ButtonRelease>",stop_move)
can.bind("<Motion>",posxy)

fen.mainloop()
