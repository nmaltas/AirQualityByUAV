import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as plticker
import numpy as np 
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import linecache
import time


counter = 0
BarLabels = ('0.405', '0.56', '0.83', '1.15', '1.5', '2', '2.65', '3.5', '4.6', '5.85', '7.25', '9', '11', '13', '15', '17', '19', '21', '23.5', '26.5', '29.5', '17.5', '35.5', '38.5')
BarData = []
LineData1 = []
LineData2 = []
LineData3 = []
x = []

#Figure and subplots in it get declared here
fig, (BarGraph, LineGraph) = plt.subplots(2)
    

def Update(i, x, BarLabels, BarData, LineData1, LineData2, LineData3):
    #Data variable memory gets reserved and previous data gets cleared
    BarData = []
    
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
    a=1
    
    while (a < 25):
        bin = DataList[a]
        BarData.append(int(bin))
        a = a + 1
   
    LineData1.append(float(DataList[30]))
    LineData1 = LineData1[-10:]
    LineData2.append(float(DataList[31]))
    LineData2 = LineData2[-10:]
    LineData3.append(float(DataList[32]))
    LineData3 = LineData3[-10:]
    
    #Modifying the figure
    fig.set_facecolor('#a9a9a9')
    #fig.suptitle('Runtime: ' + DataList[0] + ' s')
    fig.set_tight_layout(True)
    
    #Preparing the bar graph
    BarGraph.clear() #DO NOT REMOVE THIS LINE. Clears previous data, so that the graph always shows the 10 most recent values.
    BarGraph.bar(BarLabels, BarData, align= 'center', color = '#FF6600')
    BarGraph.set_yticks(np.arange(0, 120, 20)) #Y AXIS TICK VALUES. (**[FROM]**, **[TO]**, **[STEP]**)
    BarGraph.title.set_text('Runtime: ' + DataList[0] + ' s')
    BarGraph.set_facecolor('#000000')
    BarGraph.set_xlabel('Particle Diameter (um)')
    BarGraph.set_ylabel('Particle Count (ppm)')
 
    
    
    #Preparing the lines graph
    #LineGraph.clear() #DO NOT REMOVE THIS LINE. Clears previous data, so that the graph always shows the 10 most recent values.
    LineGraph.plot( x, LineData1, 'blue')
    LineGraph.plot( x, LineData2, '#FF6600')
    LineGraph.plot( x, LineData3, 'red')
   
    LineGraph.legend(['PM1', 'PM2.5', 'PM10'], loc='upper left')
    LineGraph.set_facecolor('#000000')
    LineGraph.title.set_text('Particle Mass Concentation')
    LineGraph.set_xlabel('Time (s)')
    LineGraph.set_ylabel('(um/cubic meter)')
    time.sleep(3)
	
	
    

ani =  animation.FuncAnimation(fig, Update, fargs=(x, BarLabels, BarData, LineData1, LineData2, LineData3), interval=1000)
plt.show()
