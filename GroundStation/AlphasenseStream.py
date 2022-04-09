#Script to plot the data from the Alphasense sensors
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as plticker
import numpy as np 
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import linecache
import time


counter = 0
TGS1 = []
TGS2 = []
NO1 = []
NO2 = []
NO21 = []
NO22 = []
OX1 = []
OX2 = []
x = []

#Figure and subplots in it get declared here
fig, ((VOCGraph, NOGraph), (NO2Graph, OXGraph)) = plt.subplots(2, 2)
    

def Update(i, x, TGS1, TGS2, NO1, NO2, NO21, NO22, OX1, OX2):
    
    #Fresh data is obtained from the RaspberryPi
    Data = open("Data.txt" , 'r')
    
    for line in Data:
        pass
    last = line
    
    Data.close()
        
    DataList = last.split(',')
    
    #Saving runtime of this session
    Runtime = float(DataList[0])
    x.append(Runtime)
    x = x[-10:]  #Hold up to 10 most recent values
        
    #Data gets handled and prepared accordingly to be plotted    
   
    TGS1.append(float(DataList[38]))
    TGS1 = TGS1[-10:]
    TGS2.append(float(DataList[39]))
    TGS2 = TGS2[-10:]
    
    NO1.append(float(DataList[40]))
    NO1 = NO1[-10:]
    NO2.append(float(DataList[41]))
    NO2 = NO2[-10:]
    
    NO21.append(float(DataList[42]))
    NO21 = NO21[-10:]
    NO22.append(float(DataList[43]))
    NO22 = NO22[-10:]
    
    OX1.append(float(DataList[44]))
    OX1 = OX1[-10:]
    OX2.append(float(DataList[45]))
    OX2 = OX2[-10:]
    
    #Modifying the figure
    fig.set_facecolor('#a9a9a9')
    fig.suptitle('Runtime: ' + DataList[0] + ' s')
    fig.set_tight_layout(True)
   
    
    
    #Preparing the lines graphs
    #LineGraph.clear() #DO NOT REMOVE THIS LINE. Clears previous data, so that the graph always shows the 10 most recent values.
    
    #VOC Graph
    VOCGraph.plot( x, TGS1, '#FF6600')
    VOCGraph.plot( x, TGS2, '#00FF00')
    VOCGraph.legend(['1', '2'], loc='upper left')
    VOCGraph.set_facecolor('#000000')
    VOCGraph.title.set_text('VOC')
    VOCGraph.set_xlabel('Time (s)')
    VOCGraph.set_ylabel('V')
    
    #NO Graph
    NOGraph.plot( x, NO1, '#FF6600')
    NOGraph.plot( x, NO2, '#00FF00')
    NOGraph.legend(['1', '2'], loc='upper left')
    NOGraph.set_facecolor('#000000')
    NOGraph.title.set_text('NO')
    NOGraph.set_xlabel('Time (s)')
    NOGraph.set_ylabel('ppb')
    
    #NO2 Graph
    NO2Graph.plot( x, NO21, '#FF6600')
    NO2Graph.plot( x, NO22, '#00FF00')
    NO2Graph.legend(['1', '2'], loc='upper left')
    NO2Graph.set_facecolor('#000000')
    NO2Graph.title.set_text('NO2')
    NO2Graph.set_xlabel('Time (s)')
    NO2Graph.set_ylabel('ppb')
    
    #OX Graph
    OXGraph.plot( x, OX1, '#FF6600')
    OXGraph.plot( x, OX2, '#00FF00')
    OXGraph.legend(['1', '2'], loc='upper left')
    OXGraph.set_facecolor('#000000')
    OXGraph.title.set_text('Ozone')
    OXGraph.set_xlabel('Time (s)')
    OXGraph.set_ylabel('ppb')
    
    time.sleep(3)
	
	
    

ani =  animation.FuncAnimation(fig, Update, fargs=(x, TGS1, TGS2, NO1, NO2, NO21, NO22, OX1, OX2), interval=1000)
plt.show()
