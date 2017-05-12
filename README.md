#H TLCParse
[Github](https://github.com/NathanToneNg/Thermal-Live-Viewer-Raw-Data-Parse)

This program will help to retrieve, parse, and interpret raw data from the [Thermal Live Viewer Program created by maxritter](https://github.com/maxritter/DIY-Thermocam). This assumes the camera has been set up and is using a calibration of [-273.15,0.01] and the raw data is stored in hexadecimal. If your calibration is different, instructions to fix how data is parsed will be below in the Calibration section.



## Setting up

* Open up the [Realterm program](https://realterm.sourceforge.io/)
* Make sure that the Thermal Live Viewer application is off
* Make sure that the camera is plugged into the USB port of the Windows computer


* Create a file sender file (ex. send.txt) and move it into the Realterm folder
* Similarly, create a receiver file (ex. data.txt) and move it into the Realterm folder
* In the sender file, type in the following without quotes: "dddddo"


* In the Realterm application, navigate to the Port tab:
    * Port: \10 (should be USB)
    * Baud Rate: 9600
    * Press change, and then reset open and leave it pressed again.

* Navigate to the Capture tab:
    * Leave the "print in hexadecimal" box checked

* Navigate to the Send tab:
    * 
    
    
    
    
    
## Receiving Data

* Ensure that there is full connection between the computer and the camera by sending the number "100" in the Send tab. If there is a full connection, the letter "d" should appear in return on the console.

* When ready, navigate to the Capture tab and select the Overwrite button, or the Append button if data should append to the file not replace it. The tab should turn red.

* Navigate to the Send tab and 


## Data Analysis

* Move the filled receiver file to the folder with the TLVRawDataParse.py program
* The TLVRawDataParse.py can be run with the following syntax:
	[python3](https://www.python.org/download/releases/3.0/) TLVRawDataParse.py [input file] [output .mat file]
    (_Note that python3 as well as the numpy libraries are needed_)
* The data should now be stored within the output .mat file name. This file has an array of the average high temperature points over time and can be opened in Matlab to further analyze. If done with the 300ms delay between sends as recommended, the experimental rate of data values is 3 per second.
* Additionally, those high data points are returned to the main function in the TLVRawDataParse.py program, and can be analyzed in python or printed to a csv folder or however is best for usage. 



---

## Additional Info

* Other commands that can be sent through Realterm may be found [here](https://github.com/maxritter/DIY-Thermocam/blob/master/Documents/SerialProtocol_15.pdf)
* One other way to send data if it is less often is by returning the whole data set (150), from which may be parsed calibration data as well as time. Unfortunately, at send rates too often, data is not written quickly enough and can result in errors. (Our findings are that at any lower than 250 ms delay results are not reliable).

### Calibration 

* Calibration data can be found by sending the number 114 from Realterm to the Thermal Live Viewer program, and will return 4 character, or 8 hexadecimal characters. This uses LSB first, MSB at the end, 4 bytes each for the calibration slope and then the calibration offset. 
    (_Note that the data is returned as floats_)
    	*Additional information about the specific formatting may be found [here](https://github.com/maxritter/DIY-Thermocam/blob/master/Documents/SerialProtocol_15.pdf).

*After obtaining the calibration values, the TLVRawDataParse.py program can be easily modified by finding the createMatrix function and changing the line
<center> _Matrix[y][x] = (num * 0.01) - 273.15_ <\center>
	by replacing the 0.01 with your calibration slope and 273.15 with your calibration offset.
	
---
Questions can be sent to nathantoneng@gmail.com

