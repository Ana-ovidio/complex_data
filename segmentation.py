import matplotlib.pyplot as plt
import numpy as np
from graphics import Graphics
from estimation_dimension import *
from tqdm import tqdm
import numpy as np

class Segmentation:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def variacoes (self, name_color):
        variacoes = []
        X = []
        
        for i in range (1, len(self.y)):
            delta = self.y[i] - self.y[1][i-1]
            X.append(self.x[i])
            variacoes.append(delta)
        variation = np.array(variacoes)
        
        plt.plot(X, variation,'o',color = name_color, markersize=.1)
        plt.xlabel("t")
        plt.ylabel('ΔW')
        plt.show()
    
        return variation
    
    def division_of_data (self, set_different_data):
        
        time = [self.x[50000], self.x[110000]] #Intervalos onde a dimensão 
                                                #fractal muda
        index= [50000, 110000] 

        first_dataset = []
        second_dataset = []
        thrid_dataset = []
        
        for i in range(index[0]):
            first_dataset.append(set_different_data[0][i]) 
            
        for i in range(index[0], index[1]):
            second_dataset.append(set_different_data[1][i])
            
        for i in range(index[1], len(self.x)):
            thrid_dataset.append(set_different_data[2][i])
        
        first_sub_dataset = []
        second_sub_dataset = []
        
        
        difference = first_dataset[index[0]-1] - second_dataset[0]
        
        for i in range(len(second_dataset)):
            first_sub_dataset.append(second_dataset[i] + difference)
        
        difference = first_sub_dataset[index[1]- index[0] - 1] - thrid_dataset[0]
        
        for i in range(len(thrid_dataset)):
            second_sub_dataset.append(thrid_dataset[i] + difference)
        
        y = first_dataset + first_sub_dataset + second_sub_dataset
        
        gp = Graphics(1800)
        gp.different_data(time, self.x, y)
        
        return y
    
    def detect_segment(self, d_persist, d_ref, input_dimensions, max_blocks):
        
        indexs_persist = []
        indexs_ref = []
        j = 0
        k = 0
        
        for i in range(max_blocks-1):
            if d_persist[i] >= input_dimensions[j]:
                indexs_persist.append(i-1)
                j=+1
                break
        for i in range(indexs_persist[0], max_blocks-1):
            if d_persist[i] <= input_dimensions[j] - 0.1:
                indexs_persist.append(i-1)
                j=+1
                break
       
            
        for i in range(max_blocks-1):
            if d_ref[i] <= input_dimensions[k]+0.01:
                indexs_ref.append(i-1)
                k=+1
                break
        for i in range(indexs_ref[0], max_blocks-1):
            if d_ref[i] <= input_dimensions[k]-0.1:
                indexs_ref.append(i-1)
                k=+1
                break
                  
      
        return indexs_persist, indexs_ref

    def estimation_D (self, data, max_blocks, x, input_dimensions,
                      f,g):
                            
        f.write('Blocks: %s\n\n'%max_blocks)
        g.write('Blocks: %s\n\n'%max_blocks)
        
        len_blocks = int(len(data)/ max_blocks)
        
        x_segment = []
        y_segment = []

        persist_d_list = []
        ref_d_list = []
        
        for j in range(max_blocks):
            for k in range(len_blocks):
                x_segment.append(self.x[k + len_blocks *j])
                y_segment.append(data[k + len_blocks *j]) 
            
            #Persist
            d_pos, d_neg = persistence(y_segment, name ='segment %s'%(j+1), plot_graphic = False) 
            
            d_mean_persistence = round(np.mean([d_pos, d_neg]),4)
            persist_d_list.append(d_mean_persistence)
            f.write('%s\n'%d_mean_persistence)
            
            #Ref
            set_x_and_y_segment = []
            set_x_and_y_segment.append(x_segment)
            set_x_and_y_segment.append(y_segment)
            
            logx0list, logmhvlist, poly, Dref, R2 = refinament(set_x_and_y_segment)
            
            Ref = []
            Ref.append(logx0list)
            Ref.append(logmhvlist)
            Ref.append(poly)
            
            d_mean_refinig = round(np.mean(Dref),4)
            ref_d_list.append(d_mean_refinig)
            g.write('%s\n'%d_mean_refinig)
            
            x_segment.clear()
            y_segment.clear()
            
        f.write('\n')
        g.write('\n')
                    
        return persist_d_list, ref_d_list
                
    def d_estimation_caller (self, data, all_max_blocks, x, input_dimensions):
        
        all_d_persist = []
        all_d_ref = []
        
        f = open('d_persistence','w')
        g = open('d_refining', 'w')
        
        indexs_persist = [[3, 7],[7,15], [18, 40]]
        indexs_ref = [[2, 8], [6,16], [18,41]]
        
        for i in tqdm(range(len(all_max_blocks))):
 
            max_blocks = all_max_blocks[i]
            
            persist_d_list, ref_d_list = \
            self.estimation_D(data,max_blocks,x,input_dimensions,
                              f,g)
            
            all_d_persist.append(persist_d_list)
            all_d_ref.append(ref_d_list)
            
            
            
            interval_of_blocks = [segment+1 for segment in range(max_blocks)]
            
            #Testar de maneira automática quais índices vão ser inseridos. 
            #indexs_persist, indexs_ref = \
                #self.detect_segment(persist_d_list, ref_d_list, 
                                    #input_dimensions, max_blocks)
            
                
            gp = Graphics(1800)
            gp.fractal_dimensions_segment(max_blocks, interval_of_blocks, 
                                          persist_d_list, ref_d_list,
                                          input_dimensions, indexs_persist[i], 
                                          indexs_ref[i])
            
            self.relative_error(persist_d_list, ref_d_list, indexs_persist[i], 
                                indexs_ref[i], input_dimensions, 
                                interval_of_blocks)
            
            gp.plot_segments(max_blocks, x, data)
            
        f.close()
        g.close()
        
        return all_d_persist, all_d_ref
    
    def relative_error (self, persist_list, ref_list, index_persist,
                        index_ref, input_dimensions, interval_of_blocks):
        
        relative_error_persist = []
        relative_error_ref = []
        
        j=0
        k=0
        
        for h in index_persist:
            persist_aux = persist_list[j:h+1]
            j = h+1   
            error_aux_persist = [round(abs(a-input_dimensions[k])/
                                      input_dimensions[k],3) for a in persist_aux]
            
            for t in error_aux_persist:
                relative_error_persist.append(100*t)              
            k = 1
            
        persist_aux = persist_list[j:len(persist_list)]
        error_aux_persist = [round(abs(a-input_dimensions[-1])/
                                   input_dimensions[-1],3) for a in persist_aux]
        for t in error_aux_persist:
            relative_error_persist.append(100*t)
        

        j=0
        k=0
       
        for h in index_ref:
           ref_aux = ref_list[j:h+1]
           j = h+1
           error_aux_ref = [round(abs(a-input_dimensions[k])/
                                      input_dimensions[k],3) for a in ref_aux]
 
           for u in error_aux_ref:
               relative_error_ref.append(100*u)
           k = 1
           
        ref_aux=ref_list[j:len(ref_list)]
        error_aux_ref = [round(abs(a-input_dimensions[-1])/
                               input_dimensions[-1],3) for a in ref_aux]
        for u in error_aux_ref:
            relative_error_ref.append(100*u)

        print('ref: %s\n %s' %(ref_aux, error_aux_ref))
        print('\n')

        gp = Graphics(1800)
        gp.plot_relative_error(interval_of_blocks,
                               relative_error_persist, relative_error_ref)
        
        
        
                