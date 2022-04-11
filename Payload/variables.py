# -*- coding: utf-8 -*-
"""
Created on 06/05/2019
@author: Daniel Jarvis
Variables for the sensors operation
"""
#All the needed varaibles
#RPI3 Name
RPINAME="RPi"
#Desired operation mode

#folder locations 
FOLDER = '/home/pi/Shared//' #for raw data
FOLDERCODE='/home/pi/Shared/' #For the scpirs locaton 
#Operation location, if using with GPS use area name, add inital lat and lon
LOC=['KNopfLab','Lat','lon'] #Add test name into this too, say aersol and calbration ...

#Intergration names
integration=1
#Check internet connect, URL to ping
URL = ''


MODE= "LOG"   #"GPS"   
#Note if GPS is on it takes up "/dev/ttyACM0" port, so for OPNC2 and N3 use be carfull and check /dev/

##Desired sensors to run on RPI3
OPCON="ON"
RUNSEN=["OPCN3"]  #add your OPC name for OPCN3 or OPCN2)
#RUNSEN=["OPCN3_7","OPCN3_N2"]
#Sensor ports for deried sensors, if you dont know check the /dev folder
#RUNPORT=["/dev/ttyACM0","/dev/ttyUSB0"]
RUNPORT=["/dev/ttyACM0"]
#Temp sensors port number, if a DHT11 or 22 is running get the por  
DHTON="OFF"
DHTNAMES=["DHT22_1"]
DHTPINS=[14] #check the pin
