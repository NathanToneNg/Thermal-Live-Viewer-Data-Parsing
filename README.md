#TLCParse
[Github](https://github.com/NathanToneNg/Thermal-Live-Viewer-Raw-Data-Parse)

This program will help to parse raw data from the [Thermal Live Viewer Program created by maxritter](https://github.com/maxritter/DIY-Thermocam). This assumes a calibration of [-273.15,0.01] and the raw data is stored in hexadecimal.



## Setting up

=====

* Open up the [Realterm program](https://realterm.sourceforge.io/)
* Make sure that the Thermal Live Viewer application is off
* Make sure that the camera is plugged into the USB port of the Windows computer


* Create a file sender file (ex. send.txt) and move it into the Realterm folder
* Similarly, create a receiver file (ex. data.txt) and move it into the Realterm folder
* In the sender file, type in the following without quotes: "ddddo"


* In the Realterm application, navigate to the Port tab:
..* Port: \10 (should be USB)
..* Baud Rate: 9600
..* Press change, and then reset open and leave it pressed again.

* Navigate to the Capture tab:
..* Leave the "print in hexadecimal" box checked

* Navigate to the Send tab:
..* 