import matplotlib.pyplot as plt
import numpy as np 
import random

x = [i for i in range (10)]
y_integer = [i for i in range(20)]
y = [1, 2, 3, 2, 1, 2, 3, 4, 5, 4]
plt.figure(figsize=(6, 2), dpi = 1800)
plt.title('Persistence Method', size = 10)
plt.grid(linestyle = '--')
plt.plot(x,y,color='darkblue', linewidth=1, marker = 'o', markersize = 2)
plt.show()


len_blocks = int(len(y)/ 4)
vertical_lines = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5,
                  7, 7.5, 8, 8.5, 9, 9.5, 10]
x = [i for i in range (10)]
y = [1, 4, 2, 1, 3, 4, 3, 2, 1, 3]
plt.figure(figsize=(6, 2), dpi = 1800)
plt.grid(linestyle = '--')
plt.title('Refinement Method', size = 10)
plt.plot(x,y,color='darkblue', linewidth=1, marker = 'o', markersize = 2)
for i in vertical_lines:
    plt.vlines(x = i, ymin = 0, ymax = 5, linewidth=1, color = 'darkorange')
plt.show()


