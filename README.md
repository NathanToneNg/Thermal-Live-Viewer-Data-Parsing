# TLVParse
[Github](https://github.com/NathanToneNg/Thermal-Live-Viewer-Data-Parsing)

This program will help to retrieve, parse, and interpret raw data from the [Thermal Live Viewer Program created by maxritter](https://github.com/maxritter/DIY-Thermocam). This assumes the camera has been set up and is using a calibration of [-273.15,0.01] and the raw data is stored in hexadecimal. If your calibration is different, instructions to fix how data is parsed will be below in the Calibration section.



## Setting up

* Open up the [Realterm program](https://realterm.sourceforge.io/)
* Make sure that the Thermal Live Viewer application is off
* Make sure that the camera is plugged into the USB port of the Windows computer


* Create a file sender file (ex. send.txt) and move it into the Realterm folder
* Similarly, create a receiver file (ex. data.txt) and move it into the Realterm folder
* In the sender file, type in the following without quotes: "dddddo"

* In the Realterm application, navigate to the **Port tab**:
    * **Port**: \10 (should be USB)
    * **Baud Rate**: 9600
    * Press **Change**, and then reset open and leave it pressed again. 
    	* If no pop-up occurs, then everything is good.
	* Navigate to the Send tab and enter the number '100' into the left of the top **Send Numbers** button. Then press the **Send Numbers** button. If the letter 'd' is returned, then it is set up properly.
	
* Navigate to the **Capture tab**:
	* Below the **Stop capture** button is a button with ellipses. Select that button and select the receiver file you created.
	* Click on the **Capture as Hex** button and leave it checked.
	* Press on the **Start Overwrite** button when you are ready, or press **Start Append** If you want to keep that data you already have. Note that we have no timestamps implemented, so this may cause confusion.
		*The whole box should light up red.
	
* Navigate to the **Send tab**:
	* Below **Dump File to Port** is another button with ellipses. Select that button and select the send file you created.
	* By the button **Repeats**, turn the 1 into a 0 (subtext is "_Send file repeatedly_"). 
		* If data should be retrieved a known amount of times, that number may be entered instead.
	* Select the edit box to the right of it and turn the 0 into 300 (subtext is "_Sets the delay..._")
		* Note that this creates an experimental rate of 3 times a second after combining the natural delay and artificial delay. 
		* Larger or smaller delays can also work after testing for the corresponding artificial delay? however, small amounts may result in data overlapping and thus becoming invalid.
	* Finally, when you are ready to retrieve data, press the **Send File** button next to the ellipses button at the exact moment you are ready to start. 
		* With these settings, data matrices will be received at a rate of 3 times a second, experimentally accurate up to a minute. 
		
* After taking all the data needed, navigate to the capture tab and press "Stop capture"

## Measurements after Setup
* Before retrieving additional data, be sure to move or copy the data retrieval file so that the data is not overwritten.
* Navigate to the **Send tab** and send '100' by the top **Send Numbers** button, and make sure that the letter 'd' is returned.
* Select the same or a new data retrieval file within the **Capture tab** **...** button. 
* Press on the **Start Overwrite** button when you are ready, or press **Start Append** If you want to keep that data you already have. Note that we have no timestamps implemented, so this may cause confusion.
		*The whole box should light up red.
* Finally, when you are ready to retrieve data, press the **Send File** button next to the ellipses button at the exact moment you are ready to start. 


## Finishing Up
* Navigate back to the **Send tab** and enter the number "200" next to the top **Send Numbers** button, and then press that **Send Numbers** button. 
* Note that if later programs give the warning "_Put the camera in live mode_," this is probably the missed step, and should be done to fix it.



## Data Analysis
* Move the filled receiver file to the folder with the TLVRawDataParse.py program
* The TLVRawDataParse.py can be run with the following syntax:
	[python3](https://www.python.org/download/releases/3.0/) TLVRawDataParse.py [input file] [output .mat file]
    (_Note that python3 as well as the numpy libraries are needed_)
* The data should now be stored within the output .mat file name. This file has an array of the average high temperature points over time and can be opened in Matlab to further analyze. If done with the 300ms delay between sends as recommended, the experimental rate of data values is 3 per second.
* Additionally, those high data points are returned to the main function in the TLVRawDataParse.py program, and can be analyzed in python or printed to a csv folder or however is best for usage. 
* The method for determining which points are "high temperature points" uses a percentile function. This can be modified within the source code where the percentile function is used.



---

## Additional Info

* Other commands that can be sent through Realterm may be found [here](https://github.com/maxritter/DIY-Thermocam/blob/master/Documents/SerialProtocol_15.pdf)
* One other way to send data if it is less often is by returning the whole data set (150), from which may be parsed calibration data as well as time. Unfortunately, at send rates too often, data is not written quickly enough and can result in errors. (Our findings are that at any lower than 250 ms delay results are not reliable).

### Calibration 

* Calibration data can be found by sending the number 114 from Realterm to the Thermal Live Viewer program, and will return 4 character, or 8 hexadecimal characters. This uses LSB first, MSB at the end, 4 bytes each for the calibration slope and then the calibration offset. 
    (_Note that the data is returned as floats_)
    	*Additional information about the specific formatting may be found [here](https://github.com/maxritter/DIY-Thermocam/blob/master/Documents/SerialProtocol_15.pdf).

* After obtaining the calibration values, the TLVRawDataParse.py program can be easily modified by finding the createMatrix function and changing the line
					_Matrix[y][x] = (num * 0.01) - 273.15_ 
	by replacing the 0.01 with your calibration slope and 273.15 with your calibration offset.
	
	
---
Questions for these files can be sent to nathantoneng@gmail.com, questions about the hardware and underlying program should be sent to maxritter.

