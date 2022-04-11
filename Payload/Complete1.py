#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals 
from __future__ import print_function
import threading as th
import multiprocessing as mp
import serial
import time
import struct
import datetime
import sys
import os.path
import variables as V

MODE=V.MODE
    
from opcn2_rec import Opcn2
from opcn3_rec import Opcn3
from sds_rec import SDS011 as sds
import constants #Constants for sensors defined here. Modify if needed.
from Sht1x import Sht1x as SHT1x
from ADCDifferentialPi import ADCDifferentialPi
from ADCPi import ADCPi
from threading import Timer
import RPi.GPIO as GPIO
import os


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)#pin number
GPIO.setup(22, GPIO.OUT)

sht1x1 = SHT1x(11,7) #(Data, CLock)
sht1x2 = SHT1x(24,26) #(Data, CLock)
#adc1 = ADCDifferentialPi(0x68, 0x69, 12)
adc2 = ADCDifferentialPi(0x6a, 0x6b, 12)
adc3 = ADCPi(0x6c, 0x6d, 12)
adc4 = ADCPi(0x6e, 0x6f, 12)
#4 ADCs is the maximum compatability
StreamingRefresh = 0

#LOOK-UP TABLE FOR THE ALPHASENSE SENSOR CONSTANTS
def adjustNO(T):
    if (T <= (-15)):
        return 1.8
    elif ((T>(-15)) & (T <= (-5))):
        return 1.4
    elif ((T>(-5)) & (T <= (15))):
        return  1.1
    elif ((T>(15)) & (T <= (25))):
        return 1
    elif ((T>(25)) & (T <= (45))):
        return 0.9
    else :
        return 0.8
  
def adjustNO2(T):
    if (T <= (5)):
        return 1.3
    elif ((T>(5)) & (T <= (15))):
        return 1
    elif ((T>(15)) & (T <= (25))):
        return  0.6
    elif ((T>(25)) & (T <= (35))):
        return 0.4
    elif ((T>(35)) & (T <= (45))):
        return 0.2
    else :
        return -1.5

def adjustOX(T):
    if (T <= (-15)):
        return 0.9
    elif ((T>(-15)) & (T <= (-5))):
        return 1
    elif ((T>(-5)) & (T <= (5))):
        return  1.3
    elif ((T>(5)) & (T <= (15))):
        return 1.5
    elif ((T>(15)) & (T <= (25))):
        return 1.7
    elif ((T>(25)) & (T <= (35))):
        return 2
    elif ((T>(35)) & (T <= (45))):
        return 2.5
    else :
        return 3.7

def get_data(Refresh):
    #clear the console
    #os.system('clear')
    try:
        Temperature = float(sht1x1.read_temperature_C())
        
        kt = adjustNO(Temperature)
        ntNO2 = adjustNO2(Temperature)
        ntOX = adjustOX(Temperature)
    
        NO1 = (adc2.read_voltage(2) - kt*(constants.NO1WE0/constants.NO1AE0)* adc2.read_voltage(1))/constants.SensitivityNO1
        NO2 = (adc2.read_voltage(4) - kt*(constants.NO2WE0/constants.NO2AE0)* adc2.read_voltage(3))/constants.SensitivityNO2
        NO21 = adc2.read_voltage(6) - ntNO2 *adc2.read_voltage(5)
        NO22 = adc2.read_voltage(8) - ntNO2 *adc2.read_voltage(7)
        OX1 = adc4.read_voltage(2) - ntOX *adc4.read_voltage(1) #One of those is supposed to be negative. Check and correct later
        OX2 = adc4.read_voltage(4) - ntOX *adc4.read_voltage(3)
    
        NO = (NO1 + NO2)/2
        NO_2 = (NO21 + NO22)/2       #ATTENTION HERE!!! POSSIBLE BUG HERE IF NOT HANDLED PROPERLY
        OX = (OX1 + OX2)/2
        TGS = (adc3.read_voltage(1) + adc3.read_voltage(2))/2
    except:
        print("ERROR: Part 1. Alphasense Sensors.")
        
    #TIME, INTERNAL TEMPERATURE, INTERNAL HUMIDITY, PRESSURE, TGS AVG, NO AVG, NO2 AVG, OX AVG, EXTERNAL TEMPERATURE, EXTERNAL HUMIDITY
    #s, C, %, V, , ppb, ppb, ppb, ppb, C, %
    StreamingOutput = str(time.time() - start_time)+' %02f %02f %02f %02f %02f %02f %02f %02f %02f\n' %(Temperature, sht1x1.read_humidity(), adc3.read_voltage(3), TGS, NO, NO_2, OX, sht1x2.read_temperature_C(), sht1x2.read_humidity())
    Refresh = Refresh + 1
    
    if (Refresh >= 5):
        DataOut = open('/home/pi/Shared/StreamData.txt', 'w')
        DataOut.write(StreamingOutput)
        DataOut.close()
        Refresh = 0
    else:
        DataOut = open('/home/pi/Shared/StreamData.txt', 'a')
        DataOut.write(StreamingOutput)
        DataOut.close()
    
    #TIME, INTERNAL TEMPERATURE, INTERNAL HUMIDITY, PRESSURE, TGS1, TGS2, NO1, NO2, NO21, NO22, OX1, OX2, EXTERNAL TEMPERATURE, EXTERNAL HUMIDITY
    #s, C, %, V, , , ppb, ppb, ppb, ppb, ppb, ppb, ppb, ppb, C, % 
    RawOutput = str(time.time() - start_time)+'%02f %02f %02f %02f %02f %02f %02f %02f %02f %02f %02f %02f %02f\n' %(Temperature, sht1x1.read_humidity(), adc3.read_voltage(3), adc3.read_voltage(1), adc3.read_voltage(2), NO1, NO2, NO21, NO22, OX1, OX2, sht1x2.read_temperature_C(), sht1x2.read_humidity())
    
    DataOut = open('/home/pi/Shared/RawData.txt', 'a')
    DataOut.write(RawOutput)
    DataOut.close()
    print("Reading Complete. Runtime: "+ str(time.time()-start_time))
    return Refresh


  
#Global varaibles
FOLDER=V.FOLDER #Folder location for data save
LOCATION=V.LOC[0] #RPI3 operation location
lat=V.LOC[1]#location latatuide
lon=V.LOC[2]#location longatuide
RPI=V.RPINAME

#OPCN Initialization
if __name__ == "__main__":
    #run sensors
    runsen=V.RUNSEN
    inter=V.integration#Interval time between readings 
   
    P=V.RUNPORT
    R=V.RUNSEN
    #Array for operational sensors class calls
    opsen=[]
    for r in R:
        if "OPCN2" in r:
            opsen.append(Opcn2)
        elif "OPCN3" in r:
            opsen.append(Opcn3)
        elif "SDS" in r:
            opsen.append(sds)
    
    #get the processes to run
    print("Starting AQ RPI, Mode:", V.MODE)
    print("**************************************************")
    print("integration time (seconds)",inter)
    print("**************************************************")
    #processes=[mp.Process(target=c,args=(p,r)) for c,p ,r in zip(opsen,P,R)]
    
    #run all the processes
    if V.OPCON=="ON":
        Sen=[]
        for sen, p, r in zip(opsen,P,R):
            Start=sen(p,r) #initiate the sensors
            Sen.append(Start)
            print(r," Ready")
        print(len(Sen))
    time.sleep(4)
    points=0 #data point longer 
    Time0 = time.time()
    
    while True:
        #Set starting time
        StartTime = datetime.datetime.now()
        
        #Open the Output File
        f = open("OPCN3Output.txt", 'a')
        
        #Make a string of data
        Data= str(time.time() - Time0)
        
        #run through each sensors reading there data
        for pro, r,p in zip(Sen,R,P): #loop through OPC
            newdata=pro.getData(p,r)
            Data=Data + " " + newdata
            print ("Hey!")
            #print all data and write it to the file
                    
        print(Data,file=f)
        points=points+1#add a point to point arraw
        #prase to csv
        f.flush()
        f.close()   
        
        secondsToRun = (datetime.datetime.now()-StartTime).total_seconds() % inter
        time.sleep(inter-secondsToRun)

        
        
        
