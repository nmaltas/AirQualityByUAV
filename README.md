# AirQualityByUAV
Code used for a project involving obtaining air quality measurements by UAV

########################## GROUND STATION ###################################

TO OPERATE THE SYSTEM AS OF 7/11/2020:

- Ensure that both antennas on Raspberry Pi and the laptop are connected with ethernet cable and powered up with 12-24V. Wait for the blue bars to turn on and indicate connection success.
- Run cmd and follow instructions in ConnectToRPi.txt for SSH if needed.
- After SSH has been succesful, the RPi can be controlled remotely.

For data streaming:
- run GetData.py to start fetching data to the laptop. Fetched data will be saved in the Data.txt file.
- After data fetching has been confirmed run AlphasenseStream.py, OPCStream.py, RHTStream.py and ParentStream.py to plot trasfered data from Alphasense, OPCN, RHT or all of them respectively.

ATTENTION! The maximum distance over which the streaming feature can work reliably has not yet been confirmed.

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Apart from the files mentioned above are mainly for either backup or experimental purpose.
The following list briefly outlines each one of them:

- SFTPExample.py                    : Example code from the paramiko python library, used for sftp to the Raspberry Pi.
- SSHAttempt.py                      : Experimental script to test ssh features.
- lolwut.py                                : General purpose experimental script to test the ssh feature.
- RTPlotting                              : Folder with experimental code for animating fecthed data with the matplotlib library.



@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

CHANGELOG:

3/11/2020
After finding the total runtime for each iteration to be ~3s, the reading frequency has changed to 1/3 Hz.

3/9/2020
The ParentStream.py is broken down in 2 seprate scripts that animate data individually for the 3 different groups of sensor. This makes it possible for better focusing on graphs when needed. AlphasenseStream.py, OPCStream.py and RHTStream.py have been made for this purpose, self-explanatory
names. ParentStream.py has been kept as backup and will be regularly updated to remain functional in case it is needed.

3/4/2020
As per request of professor Knopf, the functionality of the streaming algorithm has changed. Instead of streaming data and keeping the last 10 instances of readings in memory; now the algorithm accumulates data over time in a graph (which is not streaming). 
Once the script is killed, the accumulated data gets lost and the graph starts fresh.

3/2/2020
To operate the system more efficiently, the SFTP.py script has been broken down in 2 child scripts, each one taking care of SFTP and Animating separately. SFTP.py has been replaced by GetData.py and PlotData.py whose names are self-explanatory.

2/13/2020
SFTP.py now plots data from all sensors at a rate of 1 iteration per second.

2/5/2020
Instead of providing input every time connection is needed to the raspberrypi for SFTP, the user input has now been hard-coded into the script.

1/28/2020
Data streaming has now been made possible and SFTP.py is the script that needs to be run for this purpose.

11/17/2020
Small fix to handle a bug when NAN was coming up in the OPCN data resulting in a crash.





########################## PAYLOAD ###################################


TO OPERATE THE SYSTEM AS OF 8/25/2020:

Every necessary file for the payload operation is stored in the /home/Shared folder in Raspberry Pi. This is a folder that has permission to be accessed by all users.
- run with python3 : RunSensorSystem.py
- enter a variable in Operate, the variable can be either 'h' to turn the pumps on, 'l' to turn the pumps off or 't' to terminate the session and kill the script running.

When the pump is off, the system only performs checks every 1 second to see if the variable in Operate has changed.
When the 'h' variable is asserted, the pump turns on and collects data from all sensors in that order:
- Internal RHT sensor
- Alphasense and VOC sensors
- External RHT probe and pressure sensors
- OPCN sensors

It is important that the RHT sensor gets read before the Alphasense sensors so that its Temperature reading can be used to obtain the right values from the lookup table and calculate the sensors' output during the flight.

Each iteration of sensor reading takes approximately 3 seconds with the bottleneck being the OPCN sensors (~2 seconds).

The data collected is stored in 2 different files. 
- RawData.txt is where ALL of the data is being stored after each iteration and it never gets deleted. This is the main data storage where data is saved for after fight accessing.
- StreamData.txt is where only the data for live streaming are saved so that they can be accessed by the laptop. This file gets cleared and its data deleted every 100 iterations to optimize its remote access time during flight and conserve space. The streaming feature by definition only reads the latest
reading anyways.

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Files other than the RunSensorSystem.py and Operate are not to be accessed for the system's operation. They are either backup files with different versions of the code for test/calibration or experimental purposes or functional library files that are needed for the payload's operation.
The following list briefly outlines each one of them:

Supporting Library Files:
- variables.py                  : Contains variables that are needed for the OPCN sensor's operation.
- constants.py                  : Lookup table library for alphasense output calculation
- ADCDifferentialPi.py     : Library for ADCDifferential board operation.
- ADCPi.py                        : Library for ADC board operation.
- DHT.py                           : Needed for the DHT sensor of the OPCN sensor.
- GPS2.py                          : Needed for the gps operation of the OPCN sensor.
- MulOPCData.py                : Needed for OPCN sensor reading.
- opcn2_rec.py                  : Library operating the OPCN2 sensors
- opcn3_rec.py                  : Library operating the OPCN3 sensors
- sds_rec.py                      : Necessary for OPCN sensor operation
- Sht1x.py                         : Library needed for the operation of both the internal and external Sht1x RHT sensors.
- status.py                         : Code needed for OPCN operation.

Misc and backup files:
- AlphasenseConfigure.py        : Experimental and backup code for Alphasense sensor operation and output calculation.
- Attempt1.py                           : Backup code for the whole system operation as of 11/4/2019
- Calibration.py                        : Code used for the calibration of the ozone sensors on 12/7/2019
- Complete1.py                           : Backup Code for the whole system's operation as of 12/2/2019
- Complete .py                           : Backup Code for the whole system's operation as of 12/22/2019
- RHTest.py                               : Simple dummy code made for running and testing the RHT sensors.
- RunSensorSystem1.py              : Backup code for the whole system's operation while having the pumps operating together. As of 2/13/2020
- RunSensorSystem2.py              : Backup code for the whole system's operation while having the pumps operating individually. As of 2/13/2020
- start.py                                   : Example code for running OPCN sensors.
- KNopfLab_RPi_OPCN3_20200129.csv   : Example of OPCN sensor output. Mainly used as a template for exporting OPCN data in RawData.txt and StreamData.txt.
- OPC-N3_python-master            : Foder where the original OPCN example python scripts are kept for reference purposes.
- etc                                           : After the first Raspberry Pi has been damaged, its etc system folder has been backed up here.

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

CHANGELOG:

8/25/2020
Changed RunSensorSystem to accomodate new internal RHT sensor functionality. Also reverted 7/18/2020 changes.

8/24/2020
Made changes to Sht1x.py and verified Landen's changes to make internal RHT sensor operational again.

8/2/2020
Created RHTest.py for Sht1x sensor experimentation.

7/18/2020
Made changes to RunSensorSystem.py to use external RHT sensor for Alphasense output calculation.

7/13/2020
RunSensorSystem.py now supports the 2 pumps running together again because of inability to provide proper hardware to accomodate their seprate operation.

QUARANTINE

5/19/2020
Small changes to RunSensorSystem.py in attempt to improve algorithm iteration runtime.

3/11/2020
RunSensorSystem.py now can operate the pumps separately. RunSensorSystem1.py and RunSensorSystem2.py are created as backup for simultaneous and separate operation respectively. The Operate file variable format is different for each case. While h, l, t are still used for both pumps with the same
purpose, a 2-lenght string needs to be read from it instead of a single character.

2/24/2020
Minor changes made to RunSensorSystem.py to optimize the data saving process and calculate runtime after every iteration. The bottleneck of the algorithm is clearly the OPCN sensor reading with ~2s runtime out of the total ~3s.

2/21/2020
RunSensorSystem.py now clears the StreamData.txt file after 100 iterations, down from 500.

2/19/2020
Fixed a bug that would not allow the saving of temperature data with 2 decimals. Minor problem with float to int conversion before converting to string with %02f.

2/18/2020
Now StreamData.txt and RawData.txt data are stored in different order to better accomodate their intended purpose.

2/15/2020
Changed the order of data being saved in priority order.

2/11/2020
To better protect the flow of the script from crashes the whole get_data function has been placed in a protective try/except block. The code inside it has been divided into 3 different blocks of code to better troubleshout the script in case of failure. Error codes have been designed. Data reading
of -5 is determined to be the system's default error code in case of failure, along with an appropriate error message for each case.

2/2/2020
RunSensorSystemnow can operate and read OPCN sensors.

1/29/2020
Complete overhaul of the RunSensorSystem.py file to store data separately for offline and remote access.

12/4/2019
Created separate code specifically for ozone sensor calibration. Calibration.py

11/28/2019
Moved and concetrated all relevant files in the Shared folder of the RaspberryPi to be accessed remotely by the laptop if needed. All other files in the DRONE folder are left where they where for backup purposes. The main code file for the payload's operation is now RunSensorSystem.py

11/15/2019
The internal RHT Sht1x sensor occasionally randomly becomes non-responsive, which crashes the whole script. It has been placed in a protective try/except block to ensure the script keeps running if that happens. So far the sensor responds on the next iteration of the algorithm.

11/13/2019
Fixed minor bugs in the get_data function of Complete.py that didn't allow for proper output calculation. Measured calculation time to be ~0.03 seconds. It can be done during flight without affecting sampling that needs to be ~ 1 second, since it is smaller by 2 orders of magjitude.

11/12/2019
Added alphasense sensor output calculation to Complete.py

11/01/2019
Overhaul of Complete.py to accomodate all sensors but for the OPCN.

10/12/2019
Complete.py is the code made capable to read the Operate file where the operational variables are stored. Pumps can be turned on and off successfully, along with the sensors being run properly.


