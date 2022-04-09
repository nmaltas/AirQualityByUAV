import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as plticker
import numpy as np 
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import linecache
import time


counter = 0
Temperature = []
Humidity = []
x = []

#Figure and subplots in it get declared here
fig, (Graph1, Graph2) = plt.subplots(2)

def Update(i, x, Temperature, Humidity):
    
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
   
    Temperature.append(float(DataList[34]))
    Temperature = Temperature[-10:]
    
    Humidity.append(float(DataList[35]))
    Humidity = Humidity[-10:]
     
    #Modifying the figure
    fig.set_facecolor('#a9a9a9')
    fig.suptitle('Runtime: ' + DataList[0] + ' s')
    #fig.set_tight_layout(True)
    
    
    
    #Preparing the lines graphs
    #LineGraph.clear() #DO NOT REMOVE THIS LINE. Clears previous data, so that the graph always shows the 10 most recent values.
    
    #Temperature Graph
    Graph1.plot( x, Temperature, '#FF6600')
    Graph1.set_facecolor('#000000')
    #VOCGraph.title.set_text('Temperature')
    Graph1.set_xlabel('Time (s)')
    Graph1.set_ylabel('Temperature (C)')
    
    #Humidity Graph
    Graph2.plot( x, Humidity, '#FF6600')
    Graph2.set_facecolor('#000000')
    #Graph2.title.set_text('Humidity %')
    Graph2.set_xlabel('Time (s)')
    Graph2.set_ylabel('Humidity %')
    
    time.sleep(3)
	
	
    

ani =  animation.FuncAnimation(fig, Update, fargs=(x, Temperature, Humidity), interval=1000)
plt.show()
