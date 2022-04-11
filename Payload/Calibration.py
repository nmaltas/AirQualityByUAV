from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import constants #Constants for sensors defined here. Modify if needed.
#This code can be used to check pump functionality with data reading

from Sht1x import Sht1x as SHT1x
from ADCDifferentialPi import ADCDifferentialPi
from ADCPi import ADCPi
from threading import Timer
from datetime import datetime
import RPi.GPIO as GPIO
import time
import sys
import os
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)#pin number
GPIO.setup(22, GPIO.OUT)


sht1x1 = SHT1x(11,7) #(Data, CLock)
#sht1x2 = SHT1x(24,26) #(Data, CLock)
#sht1x2 = SHT1x(13,15)
#adc1 = ADCDifferentialPi(0x68, 0x69, 12)
adc2 = ADCDifferentialPi(0x6a, 0x6b, 12)
adc3 = ADCPi(0x6c, 0x6d, 12)
adc4 = ADCDifferentialPi(0x6e, 0x6f, 12)
#4 ADCs is the maximum compatability




    
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



def get_data():
    
    
    Temperature = float(sht1x1.read_temperature_C())
    
    DataOut = open('/home/pi/Shared/Data.txt', 'a')
    
    #For O3 Calibration
    ntOX = adjustOX(Temperature)
    OX1 = adc4.read_voltage(2) - ntOX *adc4.read_voltage(1)
    OX2 = -adc4.read_voltage(4) + ntOX *adc4.read_voltage(3)

    
    DataOut.write(str(time.time() - start_time)+' '+ str(Temperature ))
    DataOut.write(' %02f %02f %02f' %(OX1, OX2, sht1x1.read_humidity()) + '\n')
    
    # For RHTP Calibration
    
    DataOut.write(str(time.time() - start_time)+' '+ str(Temperature ))
    DataOut.write(' %02f %02f %02f' %(sht1x1.read_humidity(), adc3.read_voltage(3), adc3.read_voltage(4)))
    #DataOut.write(' %02f %02f' %(sht1x2.read_temperature_C(), sht1x2.read_humidity()) +
    DataOut.write('\n')
    

    DataOut.close()
    #print('Reading Complete\n')





#initialize
start_time = time.time()    #Storing the initial time for future reference
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)#pin number
GPIO.setup(22, GPIO.OUT)
print ('Hey!')
Pump = GPIO.LOW
GPIO.output(22, Pump)


while True:
    
    try:
        get_data()        
        
        # RHTP Calibration
        print("Temperature: ", sht1x1.read_temperature_C(), " C")
        print("Humidity: ", sht1x1.read_humidity())
        print("Pressure: ", str(adc3.read_voltage(3)))
        #print("Temperature: ", sht1x2.read_temperature_C(), " C")
        #print("Humidity: ", sht1x2.read_humidity())
        
        
        print("Pin 1 : %02f, Pin 2 : %02f" %(adc4.read_voltage(1), adc4.read_voltage(2)))
        print("Pin 3 : %02f, Pin 4 : %02f" %(adc4.read_voltage(3), adc4.read_voltage(4)))
        
    except:
        continue
    GPIO.output(22, Pump)
        
    time.sleep(0.09)