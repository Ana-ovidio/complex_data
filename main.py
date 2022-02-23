from fractal_functions import *
from segmentation import Segmentation
from estimation_dimension import *
from tqdm import tqdm
from normalizations import variacoes
from graphics import Graphics


gp = Graphics(1800)
input_dimensions = [1.3, 1.7, 1.5]
all_y = []

'''
x, y = functions_call('Weierstrass', D=1.5)
normalizated_data = variacoes(x, y)

limits = [min(normalizated_data), max(normalizated_data)]
gp.plot_weierstrass(x, y, limits, name = 'Non-normalized')
gp.plot_weierstrass(x, normalizated_data.tolist(), limits, name = 'Normalized')
'''

for i in tqdm(input_dimensions):
   x, y = functions_call('Weierstrass', i)
   all_y.append(y)


seg = Segmentation(x, all_y)
data = seg.division_of_data(all_y)

all_max_blocks = [10, 20, 50]

all_d_persist, all_d_ref = \
    seg.d_estimation_caller(data, all_max_blocks, x, input_dimensions) 
    
