# AirQualityByUAV
Code used for a project involving obtaining air quality measurements by UAV

TO OPERATE THE SYSTEM AS OF 7/11/2020:

- Ensure that both antennas on Raspberry Pi and the laptop are connected with an ethernet cable and powered up with 12-24V. Wait for the blue bars to turn on and indicate connection success.
- Run cmd and follow instructions in ConnectToRPi.txt for SSH if needed.
- After SSH has been succesful, the RPi can be controlled remotely.

For data streaming:
- run GetData.py to start fetching data to the laptop. Fetched data will be saved in the Data.txt file.
- After data fetching has been confirmed run AlphasenseStream.py, OPCStream.py, RHTStream.py and ParentStream.py to plot trasferred data from Alphasense, OPCN, RHT or all of them respectively.

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
