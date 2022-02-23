import math 
from graphics import Graphics

def Weierstrass (D, f,T,npoints,dom,m,name,show_graphic =False):
    
    dt = 1.*dom/npoints
    W = []
    t = []
    for K in range (npoints+1):
        t.append(T+ K*dt)
        Wf = 0.0 
        for j in range (0,m):
            Wf += math.sin((pow(f,j))*t[K]) / (f**(j*(2-D))) #Somatório dos senos da função de Weierstrass 
        W.append(Wf)
        
    if show_graphic==True:
        gp = Graphics(1800)
        gp.plot_weierstrass(t, W, name)
    return t, W

def functions_call (function, D):
    if (function == 'Weierstrass'):
        x,y= Weierstrass(D, f=1.5, T=10, npoints = 2**17, dom = 10, m=100, name ="%s"%D)
    return x, y    


