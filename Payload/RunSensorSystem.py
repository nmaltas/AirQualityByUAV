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
#GPIO.setup(22, GPIO.OUT)
sht1x1 = SHT1x(11,7) #(Data, CLock), Internal (Pipe Sensor)
sht1x2 = SHT1x(24,26) #(Data, CLock), External (Rod Sensor)
#adc1 = ADCDifferentialPi(0x68, 0x69, 12)
adc2 = ADCDifferentialPi(0x6a, 0x6b, 12)
adc3 = ADCPi(0x6c, 0x6d, 12)
adc4 = ADCDifferentialPi(0x6e, 0x6f, 12)
#4 ADCs is the maximum compatability
Refresh = 0

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

def get_data(Refresh, Time0, Hey):
    
    #Obtain Timestamp
    TimeStamp = '%0.3f' %(time.time() - Time0)
    
    #Reading TGS and Alphasense Sensors
    try:
        try:
            print("Hey!")
            Temperature = float(sht1x1.read_temperature_C())
            print(Temperature)
        except:
            print ('ERROR: Part 1. Temperature Reading Failure.')
            return Refresh
        
        kt = adjustNO(Temperature)
        ntNO2 = adjustNO2(Temperature)
        ntOX = adjustOX(Temperature)
    
        NO1 = -adc2.read_voltage(2) + (kt*(constants.NO1WE0/constants.NO1AE0)* adc2.read_voltage(1))/constants.SensitivityNO1
        NO2 = adc2.read_voltage(4) + (kt*(constants.NO2WE0/constants.NO2AE0)* adc2.read_voltage(3))/constants.SensitivityNO2
        NO21 = -adc2.read_voltage(6) - ntNO2 *adc2.read_voltage(5)
        NO22 = adc2.read_voltage(8) - ntNO2 *adc2.read_voltage(7)
        OX1 = adc4.read_voltage(2) - ntOX *adc4.read_voltage(1) #One of those is supposed to be negative. Check and correct later
        OX2 = -adc4.read_voltage(4) + ntOX *adc4.read_voltage(3)
        TGS1= adc3.read_voltage(1)
        TGS2= adc3.read_voltage(2)
        
        '''# Average Values for Streaming purposes only
        NO = (NO1 + NO2)/2
        NO_2 = (NO21 + NO22)/2       #ATTENTION HERE!!! POSSIBLE BUG HERE IF NOT HANDLED PROPERLY
        OX = (OX1 + OX2)/2
        TGS = (TGS1 + TGS2)/2
        '''
        StreamingAlphasense = ',%02f,%02f,%02f,%02f,%02f,%02f,%02f,%02f' %(TGS1, TGS2, NO1, NO2, NO21, NO22 , OX1, OX2)
        RawAlphasense = ',%02f,%02f,%02f,%02f,%02f,%02f,%02f,%02f' %(TGS1, TGS2, NO1, NO2, NO21, NO22, OX1, OX2,)
    except:
        print("ERROR: Part 1. Internal Temperature, Alphasense and TGS Sensors.")
        StreamingAlphasense = ',-5,-5,-5,-5,-5,-5,-5,-5' 
        RawAlphasense = ',-5,-5,-5,-5,-5,-5,-5,-5'
    #print ("After Alphasense sensors: ", (time.time() - Hey))
    #Reading Misc Sensors
    try:
        print("Hey!!")
        ExternalTemperature = sht1x2.read_temperature_C()
        print(ExternalTemperature)
        ExternalHumidity = sht1x2.read_humidity()
        Humidity = sht1x1.read_humidity()
        Pressure = adc3.read_voltage(3)
        ReferenceVoltage = adc3.read_voltage(4)
        
        RawMisc = ',%02f,%02f,%02f,%02f,%02f,%02f' %(ExternalTemperature, ExternalHumidity, Temperature, Humidity, Pressure, ReferenceVoltage)
        StreamingMisc = ',%02f,%02f,%02f,%02f' %(ExternalTemperature, ExternalHumidity, Pressure, ReferenceVoltage)
    except:
        print("ERROR: Part 2. Misc Sensors.")
        RawMisc = ',-5,-5,-5,-5,-5,-5'
        StreamingMisc = ',-5,-5,-5,-5'
    
    #print ("After Misc Sensors: ", (time.time() - Hey))
    #Read OPCN Sensors
    try:
    #run through each OPCN sensors reading their data
        OPCNData = ''
        for pro, r,p in zip(Sen,R,P): #loop through OPC
            OPCNData= OPCNData + ',' + pro.getData(p,r)
        
    except:
        print("ERROR: Part 3. OPCN Sensors.\n")
        i = 0
        OPCNData = ''
        while (i < 34):
            OPCNData = OPCNData + ',' + '-5'
            i = i + 1
    #print ("After OPC sensors: ", (time.time() - Hey))
    Refresh = Refresh + 1
    
    #Export the data for streaming
    StreamingOutput = TimeStamp +OPCNData + StreamingMisc + StreamingAlphasense + '\n'
#TIME,OPC,EXTERNAL TEMPERATURE,EXTERNAL HUMIDITY,PRESSURE,REFERENCE VOLTAGE,TGSx2,NOx2,NO2x2,OXx2
#s,OPC,C,%,V,V,V,V,ppb,ppb,ppb,ppb,ppb,ppb
    
    if (Refresh >= 100):
        DataOut = open('/home/pi/Shared/StreamData.txt', 'w')
        DataOut.write(StreamingOutput)
        DataOut.flush()
        DataOut.close()
        Refresh = 0
    else:
        DataOut = open('/home/pi/Shared/StreamData.txt', 'a')
        DataOut.write(StreamingOutput)
        DataOut.close()
    
    #Export the raw data
    
#TIME,EXTERNAL TEMPERATURE,EXTERNAL HUMIDITY,INTERNAL TEMPERATURE,INTERNAL HUMIDITY,PRESSURE,REFERENCE VOLTAGE,TGS1,TGS2,NO1,NO2,NO21,NO22,OX1,OX2
#s,C,%,C,%,V,V,V,V,ppb,ppb,ppb,ppb,ppb,ppb
    RawOutput = TimeStamp + RawMisc + RawAlphasense + OPCNData + '\n'
   
    DataOut = open('/home/pi/Shared/RawData.txt', 'a')
    DataOut.write(RawOutput)
    DataOut.close()
    print("Reading Complete. Runtime: "+ str(time.time()-Time0))
    #print ("After Writing: ",time.time() - Hey)
    return Refresh


  
#Global varaibles
FOLDER=V.FOLDER #Folder location for data save
LOCATION=V.LOC[0] #RPI3 operation location
lat=V.LOC[1]#location latatuide
lon=V.LOC[2]#location longatuide
RPI=V.RPINAME

#initialize
Start = time.time()    #Storing the initial time for future reference
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)#pin number
GPIO.setup(22, GPIO.OUT)
print ('Hey!')
Pump = GPIO.LOW
GPIO.output(22, Pump)

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
        
    while True:
        Hey = time.time()
        UserInput = open('/home/pi/Shared/Operate', 'r')
        Instruction = UserInput.read(1)
        UserInput.close()
         #For separate pump operation
        if (Instruction == 'l'):
            print("Pump is OFF")
            Pump = GPIO.LOW
            #GPIO.output(22, Pump)
            time.sleep(1)
            #continue
        elif (Instruction == 'h'):
            print("Pump is ON")
            
            if (Pump == GPIO.LOW):
                Pump = GPIO.HIGH
                #GPIO.output(22, Pump)
                Time0 = time.time() #Time when measurement started
                
        elif (Instruction == 't'):
            GPIO.output(22, GPIO.LOW)
            print("TERMINATING PROGRAM")
            time.sleep(1)
            break
        else:
            print(" ERROR: INVALID INPUT BY USER")
            time.sleep(1)
            #continue
        GPIO.output(22, Pump)
        if (Pump == GPIO.LOW):
            continue
        
        
        #Take readings
        try:
            Refresh = get_data(Refresh, Time0, Hey)
                
        
        except:
            print("ERROR: Could not read sensors.")
            continue
        
        IterationTime = time.time()- Hey
        print("Iteration time:", IterationTime)

Pump = GPIO.LOW
GPIO.output(22, Pump)
print('End of program')