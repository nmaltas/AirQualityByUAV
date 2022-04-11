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


#GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)#pin number
sht1x1 = SHT1x(11,7) #(Data, CLock), Internal (Pipe Sensor)

Temperature= sht1x1.read_temperature_C()
Humidity = sht1x1.read_humidity()


#4 ADCs is the maximum compatibility

print("Hey")
print("Reading RHT")
print("Temperature = %02f, Humidity = %02f" %(Temperature, Humidity))
