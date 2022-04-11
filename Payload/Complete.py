from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import constants #Constants for sensors defined here. Modify if needed.
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
sht1x2 = SHT1x(24,26) #(Data, CLock)
#adc1 = ADCDifferentialPi(0x68, 0x69, 12)
adc2 = ADCDifferentialPi(0x6a, 0x6b, 12)
adc3 = ADCPi(0x6c, 0x6d, 12)
adc4 = ADCPi(0x6e, 0x6f, 12)
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

    
#initialize
start_time = time.time()    #Storing the initial time for future reference
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)#pin number
GPIO.setup(22, GPIO.OUT)
print ('Hey!')
Pump = GPIO.LOW
GPIO.output(22, Pump)

#Main Loop
while True:
    UserInput = open('/home/pi/Shared/Operate', 'r')
    Instruction = UserInput.read(1)
    if (Instruction == 'l'):
        print("Pump is OFF")
        Pump = GPIO.LOW
        GPIO.output(22, Pump)
        time.sleep(1)
        continue
    elif (Instruction == 'h'):
        print("Pump is ON")
        
        if (Pump == GPIO.LOW):
            Pump = GPIO.HIGH
            GPIO.output(22, Pump)
            
    elif (Instruction == 't'):
        print("TERMINATING PROGRAM")
        Pump = GPIO.LOW
        GPIO.output(22, Pump)
        time.sleep(1)
        break
    else:
        print(" ERROR: INVALID INPUT BY USER")
        time.sleep(1)
        continue
    UserInput.close()
    
    
    #Take readings
    try:
        Refresh = get_data(Refresh)
    
    except:
        print("ERROR: Could not read sensors.")
        continue
    
    time.sleep(0.1)

Pump = GPIO.LOW
GPIO.output(22, Pump)
print('End of program')
