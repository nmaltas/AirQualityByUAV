from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals 

import time
from threading import Timer
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

def get_data():
    Temperature = float(sht1x1.read_temperature_C())
    
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
    
    print(',%02f,%02f,%02f,%02f,%02f,%02f,%02f,%02f' %(TGS1, TGS2, NO1, NO2, NO21, NO22 , OX1, OX2))





#initialize
start_time = time.time()    #Storing the initial time for future reference
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)#pin number
GPIO.setup(22, GPIO.OUT)
print ('Hey!')
Pump = GPIO.LOW
GPIO.output(22, Pump)

while True:
    get_data()
    
    time.sleep(1)


