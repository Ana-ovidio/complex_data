import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
from graphics import Graphics
    
def persistence (y, name, plot_graphic = True):
    sinal = []
    for i in range (1,len(y)):
        sub = y[i]- y[i-1]
        sinal.append(sub)
    i = 0
    varia_pos = []
    varia_neg = []
    
    while (sinal[i]<0):
        i+=1
    var_pos = sinal[i]
    
    i = 0
    
    while (sinal[i]>0):
        i+=1
    var_neg = - sinal [i]
    
    
    persist= []
    cont = 1
    for i in range(1, len(sinal)):
        if (sinal[i]>0 and sinal [i-1]>0) or (sinal[i]<0 and sinal[i-1]<0):
            cont+=1
            
        else:
            if sinal[i]<0:
                
                persist.append(cont)
                cont = 1
            else:
                
                persist.append(-cont)
                cont=1
                
    if persist[-1]<0:
        persist.append(cont)
    
    else:
        persist.append(-cont)
        
    maxpos= max([n for n in persist if n>0])
    maxneg= min([n for n in persist if n<0])
    
    persist_pos= [] #Recebe as persistencias de 1 ate max persistencia positiva em persist
    persist_neg= []
    qtdpos= [] #Recebe a quantidade de repetições de cada persistencia positiva
    qtdneg= []
    for i in range (1, maxpos+1):
        persist_pos.append(i)
        cont=0
        for j in range (len(persist)):
            if persist[j]==i:
                cont+=1
        qtdpos.append(cont)
    for i in range (1, abs(maxneg-1)):
        persist_neg.append(i)
        cont=0
        for j in range (len(persist)):
            if persist[j]==-i:
                cont+=1
        qtdneg.append((cont))
        
    tamanho_pos = len(persist_pos)
    tamanho_neg = len(persist_neg)
    contador1 = 0
    contador2 = 0
    
    for i in range(1, len(sinal)):
        if (sinal[i]>0 and sinal [i-1]>0) or (sinal[i]<0 and sinal[i-1]<0):
            if (sinal[i]>0 and sinal [i-1]>0):
                var_pos = var_pos + sinal[i]
            else:
                var_neg = var_neg - sinal[i]
        else:
            if sinal[i]<0:
    
                varia_pos.append(var_pos)
                contador1+=1
                if(contador1<tamanho_pos):
                    j = i
                    while (sinal[j]<0):
                        j+=1
                    var_pos = sinal[j]
            else:
                
                varia_neg.append(var_neg)
                contador2+=1
                if(contador2<tamanho_neg):
                    j = i
                    while (sinal[j]>0 and j <len(sinal)-1):
                        j+=1
                    var_neg = - sinal [j]
    if persist[-1]>0:
        varia_pos.append(var_pos)
    else:
        varia_neg.append(var_neg)

    #Retirando as persistencias com quantidade 0.
    
    posrem= [persist_pos[i] for i in range (len(persist_pos)) if qtdpos[i]==0]
    negrem= [persist_neg[i] for i in range (len(persist_neg)) if qtdneg[i]==0]
    
    #for i in range (len(persist_pos)):
        #if qtdpos[i]==0:
           # posrem.append(persist_pos[i])
    #for i in range (len(persist_neg)):
       # if qtdneg[i]== 0:
           # negrem.append(persist_neg[i])
           
    for i in range (len(posrem)):
        qtdpos.remove(0)
        persist_pos.remove(posrem[i])
    for i in range (len(negrem)):
        qtdneg.remove(0)
        persist_neg.remove(negrem[i])
    
    logqtdpos = np.log(qtdpos)
    logqtdneg = np.log(qtdneg)
    
    a_pos = np.polyfit(persist_pos, logqtdpos,1)[0]
    a_neg = np.polyfit(persist_neg, logqtdneg,1)[0]
    
    d_pos = round(1 - ((2 * a_pos) / 3),2)
    d_neg = round(1 - ((2 *  a_neg) / 3),2)
    
    if plot_graphic == True:
        gp = Graphics(1800)
        gp.plot_persistence(persist_pos, persist_neg, 
                          logqtdneg, logqtdpos, name)
    
    return d_pos, d_neg


def refinament(data):
    x=np.array(data[0])
    y=np.array(data[1])
    x0=x-x[0] 
    y0=y-y[0]
    ref=11
    mom=np.zeros((ref-1))
    hor=np.zeros((ref-1))
    ver=np.zeros((ref-1))
    dx0=np.zeros((ref-1))
    m=1.0 # Mass
    E=1.0 # Young modulus
    I=1.0 # Moment of inertia
    for step in range(1,ref):
#        print "step= %s"%step
        momsum=0.0
        horsum=0.0
        versum=0.0
        for i in range(0,(len(x0)-step),step):
            length = math.sqrt((x0[i+step]-x0[i])**2 + (y0[i+step]-y0[i])**2)
            momsum += length/(E*I)
            horsum += length*(y0[i+step]**2 + math.fabs(y0[i+step]*y0[i]) + y0[i]**2)/(E*I)
            versum += length*(x0[i+step]**2 + math.fabs(x0[i+step]*y0[i]) + x0[i]**2)/(E*I)
        dx0[step-1]=step
        mom[step-1]=momsum
        hor[step-1]=horsum
        ver[step-1]=versum
    logx0=np.zeros(ref-1)
    logmom=np.zeros(ref-1)
    loghor=np.zeros(ref-1)
    logver=np.zeros(ref-1)
    for i in range(0,len(mom)):
        logx0[i]=np.log(dx0[i])
        logmom[i]=np.log(math.sqrt(m*mom[i]))
        loghor[i]=np.log(math.sqrt(m*hor[i]))
        if(math.sqrt(m*ver[i])!=0.0):
            logver[i]=np.log(math.sqrt(m*ver[i])) 
    logx0list=np.array(logx0).tolist()
    logmomlist=np.array(logmom).tolist()
    loghorlist=np.array(loghor).tolist()          
    logverlist=np.array(logver).tolist()   
    polym=np.polyfit(logx0list,logmomlist,1)
    polyh=np.polyfit(logx0list,loghorlist,1)
    polyv=np.polyfit(logx0list,logverlist,1)

    Drefmom=1-2*polym[0]
    Drefhor=1-2*polyh[0]
    Drefver=1-2*polyv[0]
    
    R2M, R2H, R2V = __R2_score_MHV(logx0list, logmomlist, polym, loghorlist, polyh, logverlist, polyv)
    
    logx0list=[logx0list]
    logmhvlist=[logmomlist, loghorlist, logverlist]
    poly=[polym, polyh, polyv]
    Dref=[Drefmom, Drefhor, Drefver]
    R2=[R2M, R2H, R2V]
    
    return logx0list, logmhvlist, poly, Dref, R2

def __R2_score_MHV ( logx0list, logmomlist, Dm, loghorlist, Dh, logverlist, Dv):
    
    y_trueM = logmomlist
    y_predM = np.add((np.multiply(Dm[0],logx0list)),Dm[1])
    y_trueH = loghorlist
    y_predH = np.add((np.multiply(Dh[0],logx0list)),Dh[1])
    y_trueV = logverlist
    y_predV = np.add((np.multiply(Dv[0],logx0list)),Dv[1])
    
    R2M=r2_score(y_trueM,y_predM)
    R2V=r2_score(y_trueV,y_predV)
    R2H=r2_score(y_trueH,y_predH)
    
    return (R2M, R2H, R2V)

def plot_log_ref (Ref,name):

    method = 'Dynamics with refining'
    xlabel = 'ln(step)'
    ylabel ='ln(period)'
    
    logx0list=Ref[0][0]
    logmomlist=Ref[1][0]
    loghorlist=Ref[1][1]
    logverlist=Ref[1][2]
    
    plt.plot(logx0list,logmomlist,'^r',label="mom")
    plt.plot(logx0list,loghorlist,'og',label="hor")
    plt.plot(logx0list,logverlist,'sb',label="ver")
    
    a_mom=Ref[2][0][0]
    b_mom=Ref[2][0][1]
    a_hor=Ref[2][1][0]
    b_hor=Ref[2][1][1]
    a_ver=Ref[2][2][0]
    b_ver=Ref[2][2][1]
    
    xx_mom=[]
    yy_mom=[]
    for i in range(len(logx0list)):
        xx_mom.append(logx0list[i])
        yy_mom.append(a_mom*logx0list[i]+b_mom)
    plt.plot(xx_mom,yy_mom,color= 'r', markersize=.3)
    
    xx_hor=[]
    yy_hor=[]
    for i in range(len(logx0list)):
        xx_hor.append(logx0list[i])
        yy_hor.append(a_hor*logx0list[i]+b_hor)
    plt.plot(xx_hor,yy_hor,"g", markersize=.3)
    
    xx_ver=[]
    yy_ver=[]
    for i in range(len(logx0list)):
        xx_ver.append(logx0list[i])
        yy_ver.append(a_ver*logx0list[i]+b_ver)
    plt.plot(xx_ver,yy_ver,"b", markersize=.3)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.gcf().set_size_inches(12, 8) # alterar tamanho
    plt.legend(['%s'%round(a_mom,4), '%s'%round(a_hor,4), '%s'%round(a_ver,4)])
    plt.title(method+" (%s)"%name)
    plt.grid(linestyle='--')
    plt.savefig("ref "+name+".png", dpi=900)
    plt.show()
            
        

