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

TGS1 = []
TGS2 = []
NO1 = []
NO2 = []
NO21 = []
NO22 = []
OX1 = []
OX2 = []

Temperature = []
Humidity = []

x = []

#Figure and subplots in it get declared here
fig, Parent = plt.subplots(2, 4)
    

def Update(i, x, BarLabels, BarData, LineData1, LineData2, LineData3, TGS1, TGS2, NO1, NO2, NO21, NO22, OX1, OX2, Temperature, Humidity):
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
    
    Temperature.append(float(DataList[34]))
    Temperature = Temperature[-10:]
    
    Humidity.append(float(DataList[35]))
    Humidity = Humidity[-10:]
        
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
    
    LineData1.append(float(DataList[30]))
    LineData1 = LineData1[-10:]
    LineData2.append(float(DataList[31]))
    LineData2 = LineData2[-10:]
    LineData3.append(float(DataList[32]))
    LineData3 = LineData3[-10:]
    
    #Modifying the figure
    fig.set_facecolor('#a9a9a9')
    fig.suptitle('Runtime: ' + DataList[0] + ' s')
    fig.set_tight_layout(True)
   
    
    
    #Preparing the lines graphs
    #LineGraph.clear() #DO NOT REMOVE THIS LINE. Clears previous data, so that the graph always shows the 10 most recent values.
    
    #Temperature Graph
    Parent[0, 0].clear()
    Parent[0, 0].plot( x, Temperature, '#FF6600')
    Parent[0, 0].set_facecolor('#000000')
    #Parent[0, 0].title.set_text('Temperature')
    Parent[0, 0].set_xlabel('Time (s)')
    Parent[0, 0].set_ylabel('Temperature (C)')
    
    #Humidity Graph
    Parent[0, 1].clear()
    Parent[0, 1].plot( x, Humidity, '#FF6600')
    Parent[0, 1].set_facecolor('#000000')
    #Parent[0, 1].title.set_text('Humidity %')
    Parent[0, 1].set_xlabel('Time (s)')
    Parent[0, 1].set_ylabel('Humidity %')
        
    #VOC Graph
    Parent[0, 2].clear()
    Parent[0, 2].plot( x, TGS1, '#FF6600')
    Parent[0, 2].plot( x, TGS2, '#00FF00')
    #VOCGraph.legend(['1', '2'], loc='upper left')
    Parent[0, 2].set_facecolor('#000000')
    Parent[0, 2].title.set_text('VOC')
    Parent[0, 2].set_xlabel('Time (s)')
    Parent[0, 2].set_ylabel('TBD')
    
    #NO Graph
    Parent[0, 3].clear()
    Parent[0, 3].plot( x, NO1, '#FF6600')
    Parent[0, 3].plot( x, NO2, '#00FF00')
    #Parent[0, 3].legend(['1', '2'], loc='upper left')
    Parent[0, 3].set_facecolor('#000000')
    Parent[0, 3].title.set_text('NO')
    Parent[0, 3].set_xlabel('Time (s)')
    Parent[0, 3].set_ylabel('ppb')
    
    #NO2 Graph
    Parent[1, 0].clear()
    Parent[1, 0].plot( x, NO21, '#FF6600')
    Parent[1, 0].plot( x, NO22, '#00FF00')
    #Parent[1, 0].legend(['1', '2'], loc='upper left')
    Parent[1, 0].set_facecolor('#000000')
    Parent[1, 0].title.set_text('NO2')
    Parent[1, 0].set_xlabel('Time (s)')
    Parent[1, 0].set_ylabel('ppb')
    
    #OX Graph
    Parent[1, 1].clear()
    Parent[1, 1].plot( x, OX1, '#FF6600')
    Parent[1, 1].plot( x, OX2, '#00FF00')
    #Parent[1, 1].legend(['1', '2'], loc='upper left')
    Parent[1, 1].set_facecolor('#000000')
    Parent[1, 1].title.set_text('Ozone')
    Parent[1, 1].set_xlabel('Time (s)')
    Parent[1, 1].set_ylabel('ppb')
    
    #Bar Graph
    Parent[1, 2].clear() #DO NOT REMOVE THIS LINE. Clears previous data, so that the graph always shows the 10 most recent values.
    Parent[1, 2].bar(BarLabels, BarData, align= 'center', color = '#FF6600')
    Parent[1, 2].set_yticks(np.arange(0, 120, 20)) #Y AXIS TICK VALUES. (**[FROM]**, **[TO]**, **[STEP]**)
    #Parent[1, 2].title.set_text('Runtime: ' + DataList[0] + ' s')
    Parent[1, 2].set_facecolor('#000000')
    Parent[1, 2].set_xlabel('Particle Diameter (um)')
    Parent[1, 2].set_ylabel('Particle Count (ppm)')
 
    #PMC graph
    Parent[1, 3].clear() #DO NOT REMOVE THIS LINE. Clears previous data, so that the graph always shows the 10 most recent values.
    Parent[1, 3].plot( x, LineData1, 'blue')
    Parent[1, 3].plot( x, LineData2, '#FF6600')
    Parent[1, 3].plot( x, LineData3, 'red')
   
    #Parent[1, 3].legend(['PM1', 'PM2.5', 'PM10'], loc='upper left')
    Parent[1, 3].set_facecolor('#000000')
    Parent[1, 3].title.set_text('Particle Mass Concentation')
    Parent[1, 3].set_xlabel('Time (s)')
    Parent[1, 3].set_ylabel('(um/cubic meter)')
    time.sleep(3)
	
	
    

ani =  animation.FuncAnimation(fig, Update, fargs=(x, BarLabels, BarData, LineData1, LineData2, LineData3, TGS1, TGS2, NO1, NO2, NO21, NO22, OX1, OX2, Temperature, Humidity), interval=1000)
plt.show()
