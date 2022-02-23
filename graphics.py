import numpy as np
import matplotlib.pyplot as plt 


class Graphics:
    
    def __init__(self,dpi_image):
        self.dpi_image = dpi_image
        
    def plot_variations (self, variations, x, name_color, title_graphic):
        
        plt.figure(dpi=self.dpi_image)
        plt.plot(x, variations,'o',color = name_color, markersize=.1)
        plt.xlabel("t")
        plt.ylabel('ΔW')
        plt.title('%s' %title_graphic)
        plt.savefig('results/' + 'Variation_' +  title_graphic + '.png')
        plt.show()
        
    def plot_weierstrass (self, t, W, limits, name):
        plt.figure(dpi=self.dpi_image)
        plt.plot(t,W,linewidth=.5,color='darkblue')
        #plt.title(" Mandelbrot- Weierstrass functions data for D = "+ "%s" 
                  #%name)
        plt.title('%s' %name, size = 10)
        plt.xlabel("t")
        plt.ylabel("W(t)")
        plt.grid(linestyle='--')
        plt.ylim(limits[0], limits[1])
        plt.savefig('results/' + 'Weierstrass_' +  name + '.png')
        plt.show()
        
    def plot_persistence (self, persist_pos, persist_neg, 
                          logqtdneg, logqtdpos, name):
        a_pos = np.polyfit(persist_pos, logqtdpos,1)[0]
        b_pos = np.polyfit(persist_pos, logqtdpos,1)[1]
        a_neg = np.polyfit(persist_neg, logqtdneg,1)[0]
        b_neg = np.polyfit(persist_neg, logqtdneg,1)[1]
        
        xxp = []
        yyp = []
        
        for i in range (len(persist_pos)):
            xxp.append(persist_pos[i])
            yyp.append(a_pos*persist_pos[i] + b_pos)
        
        
        xxn = []
        yyn = []
        
        for i in range (len(persist_neg)):
            xxn.append(persist_neg[i])
            yyn.append(a_neg*persist_neg[i] + b_neg)
        
        a_mais =  round(a_pos, 4)
        a_menos = round(a_neg,4)
        plt.plot(xxn,yyn,color='orange')
        plt.plot(xxp,yyp,color='blue')
        plt.plot (persist_pos, logqtdpos, '^', color = 'blue')
        plt.plot (persist_neg, logqtdneg,'v', color = 'orange' )
        plt.legend(['Slope of ups = %s' %a_mais, 'Slope os downs = %s' %a_menos])
        plt.grid(linestyle='--')
        plt.xlabel('persistence')
        plt.ylabel('log(quantity)')
        plt.title("Frequency distributions of persistences for data from   %s" %name )
        plt.show()
    
    def different_data (self, time, x, y):
        plt.figure(dpi=self.dpi_image)
        plt.ylim(min(y)-1, max(y)+1)
        plt.vlines(x=time[0], ymin=min(y)-1, ymax=max(y)+1, linewidth=1, 
                   color='darkred')
        plt.vlines(x=time[1], ymin=min(y)-1, ymax=max(y)+1, linewidth=1, 
                   color='darkred')
        plt.plot(x,y, linewidth=.3, color = "darkblue")
        plt.title("Weierstrass function associeted with differents dimensions", 
                  size=10)
        plt.xlabel("t")
        plt.ylabel("W(t)")
        plt.grid(linestyle='--')
        plt.savefig('results/' + 'diferents_data'  + '.png')
        plt.show()
         
    def fractal_dimensions_segment (self, max_blocks, segments, all_d_persist, 
                                    all_d_ref,input_dimensions,index_persist,
                                    index_ref):
        
        plt.figure(dpi=self.dpi_image)
        plt.title("D from persistence", size = 10)
        plt.plot(segments, all_d_persist, linewidth=1, marker='o', markersize=2,
                 color='mediumvioletred')
        plt.hlines(y=input_dimensions[0], xmin=0, xmax=max_blocks, linewidth=1,
                  color='black', linestyle='--')
        plt.hlines(y=input_dimensions[1], xmin=0, xmax=max_blocks, linewidth=1,
                  color='black', linestyle='--')
        plt.hlines(y=input_dimensions[2], xmin=0, xmax=max_blocks, linewidth=1,
                  color='black', linestyle='--')
        
        plt.vlines(x=segments[index_persist[0]+1], ymin= 1, 
                   ymax=2, linewidth=1,
                   color= 'darkred')
        plt.vlines(x=segments[index_persist[1]+1], ymin= 1, 
                   ymax=2, linewidth=1,
                   color= 'darkred')
        
        plt.text(segments[index_persist[0]]+1.5,1.9,'%s' %(index_persist[0] + 2), 
                 size = 'small', weight = 'bold')
        plt.text(segments[index_persist[1]]+1.5,1.9,'%s' %(index_persist[1] + 2), 
                 size = 'small', weight = 'bold')
        
        plt.ylim(1,2)
        plt.grid(linestyle='--')
        plt.xlabel('Segments')
        plt.ylabel('D')
        plt.savefig('results/' + 'Dpersis_' + str(max_blocks) + '.png')
        plt.show()
        
         
        plt.figure(dpi=self.dpi_image)
        plt.title("D from refinement", size = 10)
        plt.plot(segments,all_d_ref, linewidth=1, marker='o', markersize=2,
                 color='royalblue')
        plt.hlines(y=input_dimensions[0], xmin=0, xmax=max_blocks, linewidth=1,
                  color='black', linestyle='--')
        plt.hlines(y=input_dimensions[1], xmin=0, xmax=max_blocks, linewidth=1,
                  color='black', linestyle='--')
        plt.hlines(y=input_dimensions[2], xmin=0, xmax=max_blocks, linewidth=1,
                  color='black', linestyle='--')
        
        plt.vlines(x=segments[index_ref[0]+1], ymin= 1, 
                   ymax=2, linewidth=1,
                   color= 'darkred')
        plt.vlines(x=segments[index_ref[1]+1], ymin= 1, 
                   ymax=2, linewidth=1,
                   color= 'darkred')
        
        plt.text(segments[index_ref[0]]+1.5,1.9,'%s' %(index_ref[0]+2), 
                 size = 'small', weight = 'bold')
        plt.text(segments[index_ref[1]]+1.5,1.9,'%s' %(index_ref[1]+2), 
                 size = 'small', weight = 'bold')
        
        
        plt.ylim(1,2)
        plt.grid(linestyle='--')
        plt.xlabel('Segments')
        plt.ylabel('D')
        plt.savefig('results/' + 'Dref_' +  str(max_blocks) + '.png')
        plt.show()
        

    def plot_segments (self,max_blocks,x, y,):
        len_blocks = int(len(y)/ max_blocks)
        fig, ax = plt.subplots(dpi=self.dpi_image)
        for i in range(1,max_blocks):
            ax.vlines(x=x[i* len_blocks], ymin= min(y), ymax=max(y), 
                      linewidth=1, color='olive')
            
        plt.plot(x,y, linewidth=.3, color = "darkblue")
        plt.title("%s blocks" %max_blocks, size = 10)
        plt.xlabel("t")
        plt.ylabel("W(t)")
        plt.savefig('results/' + str(max_blocks) + '.png')
        plt.show()

    def plot_relative_error (self, interval_of_blocks, relative_error_persist,
                             relative_error_ref):
        
        max_blocks = len(interval_of_blocks)
        fig, (ax1,ax2) = plt.subplots(nrows=2, sharex=True, dpi = 1800)
        plt.subplots_adjust(hspace=0.15)
        plt.xlabel('Segments', family = 'cursive')
        plt.suptitle('Relative errors (%)', size= 10, family = 'cursive')
        
        ax1.plot(interval_of_blocks, relative_error_persist, linewidth=1, 
                 color= 'mediumvioletred', marker ='o', markersize = 2, 
                 label = 'Error from persistence')
        ax2.plot(interval_of_blocks, relative_error_ref, linewidth=1, 
                 color= 'royalblue',marker ='o', markersize = 2,
                 label = 'Error from refinement')
        
        ax1.grid(linestyle = '--')
        ax2.grid(linestyle = '--')
        
        ax1.legend(fontsize= 'x-small')
        ax2.legend(fontsize= 'x-small')
        
        ax1.set_ylim(0, 10)
        ax2.set_ylim(0, 10)
        
        plt.savefig('results/' + 'relative_error_' + str(max_blocks) + '.png')
        plt.show()
        

        