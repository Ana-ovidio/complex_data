import numpy as np 
from tqdm import tqdm
from estimation_dimension import *
from graphics import Graphics

def normalization (variation, y):
     normalizated_data = y/max(variation)
     normalizated_variations = variation/max(variation)
     return normalizated_data, normalizated_variations 

def variacoes (x, y):
    gp = Graphics(1800)
    variation = []
    X = []
    
    for i in range (1, len(y)):
        delta = y[i] - y[i-1]
        X.append(x[i])
        variation.append(delta)
        
    d_pos, d_neg = persistence(y, name =  'Distribuition of persistence',
                               plot_graphic=False)
    d_mean_persist = round(np.mean([d_pos, d_neg]),4)
    print(d_mean_persist)
    logx0list, logmhvlist, poly, Dref, R2 = refinament([x,y])
    d_mean_ref = round(np.mean(Dref), 4)
    print(d_mean_ref)
    gp.plot_variations(variation, X, name_color = 'skyblue',
                       title_graphic= 'Non-normalized')
    
    
    
    normalizated_data, normalizated_variations = normalization(np.array(variation),
                                                               np.array(y))
    d_pos, d_neg = persistence(normalizated_data, 
                               name= 'Distribuition of persistence', 
                               plot_graphic=False)
    d_mean_persist = round(np.mean([d_pos, d_neg]),4)
    logx0list, logmhvlist, poly, Dref, R2 = refinament([x,normalizated_data])
    d_mean_ref = round(np.mean(Dref), 4)
    
    gp.plot_variations(normalizated_variations, X, name_color = 'darkslategray',
                       title_graphic = 'Normalized')
    
    print('\n')
    print(len(variation))
    print(len(normalizated_variations))

    
    return normalizated_data
