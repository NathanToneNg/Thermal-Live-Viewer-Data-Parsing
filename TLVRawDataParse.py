#!/usr/bin/env python3
import sys
import operator
import readline
import numpy
import scipy.io


#####
# Requires that filename is the name of a txt file full of hexadecimal characters
#
# Will not modify filename
#
# Gets the strings of Matrices at different times from filename and returns them as a list of strings
#
# Prints "File 'filename' not found if the file could not be found or opened.
#####
def retrieveStrings(filename):
	outerI = 0
	strList = []
	try:
		f = open(filename, 'r')
	except FileNotFoundError:
		print('File \'', filename, '\' not found.')
		exit(1)
	allData = f.read()
	i = allData.find('6464646464')
	while(i < len(allData) and i >= 0):
		i = i + 10
		tmpstr = allData[i:i + 19200]
		allData = allData[i+19200:]
		strList.append(tmpstr)
		outerI = outerI + 1
		i = allData.find('6464646464')
		#if(len(strList) == 30): #this is for a specific case if you know the data past a certain point doesn't matter
		#	return strList
	return strList

#####
# Requires that data is a string and should have 19200 characters if retrieved properly
#
# Will not modify data
#
# Gets the numerical temperature values from data and puts it into a 3d numpy matrix which
#	is used in other functions. The matrix will be 60 by 80.
#
# Prints "Filled." if the program filled the whole matrix. Prints "Did not fill" if the string 
#	returned was too small, which should not happen for the way retrieveStrings currently works.
#####
def createMatrix(data):
	Matrix = numpy.arange(4800)
	Matrix = Matrix.reshape((60,80))
	x = 0
	y = 0
	i = 0
	while True:
		if len(data) < i + 4:
			print('Did not fill')
			break
		chars = data[i:i + 4];
		num = (int(chars[0],16) * (16**3)) + (int(chars[1],16)  * (16**2)) + (int(chars[2],16) * 16) + int(chars[3],16)
		Matrix[y][x] = (num * 0.01) - 273.15 # (Data * calibration_slope) - calibration_offset
		x = x + 1;
		if x >= 80:
			x = 0;
			y = y + 1;
		if y >= 60:
			print('Filled.');
			break
		i = i + 4;
	return Matrix;

#####
# Requires that Matrix3 has been filled using createMatrix and that matFile is a .m file.
#
# Will not modify either of Matrix3 or the name matFile, but will put data into matFile 
# 	and will initialize it in the case that it is not initialized
#
# Gets the data points in Matrix3 and parses so that only the given percentile of highest 
#	temperature data will be taken for the average. Said averages will be placed into an
#	array of data values that are printed, put into the given matFile, and returned.
#
# Prints the array of average of temperature values for the given percentile or higher.
#####
def getAverageHighTemp(Matrix3,matFile, percentile):
	
	highTemps = [0] * Matrix3.shape[2];
	for z in range(1,Matrix3.shape[2]):
		counter = 0
		Matrix = numpy.arange(4800);
		Matrix = Matrix.reshape(60,80);
		for x in range(0,79):
			for y in range(0,59):
				Matrix[y][x] = Matrix3[y][x][z]
		summation = 0;
		#med = numpy.median(Matrix)
		med = numpy.percentile(Matrix, percentile);
		#print(med)
		for x in range(0,79):
			for y in range(0,59):
				if Matrix[y][x] >= med:
					summation += Matrix[y][x]
					counter += 1;
		if summation == 0:
			highTemps[z] = 0;
		else:
			highTemps[z] = summation / counter;
	print(highTemps);
	scipy.io.savemat(matFile,mdict={'arr': highTemps})
	return highTemps




def main(argv):
	filename = str(argv[1])
	strList = retrieveStrings(filename)
	Matrix3 = numpy.arange(4800 * len(strList))
	Matrix3 = Matrix3.reshape(60,80,len(strList));
	i = 0
	for data in strList:
		tmpMatrix = createMatrix(data)
		for x in range(0,79):
			for y in range(0,59):
				Matrix3[y][x][i] = tmpMatrix[y][x]
		i += 1;
	matFile = str(argv[2])
	highTemps = getAverageHighTemp(Matrix3, argv[2], 96);

	



if __name__ == '__main__': 
	main(sys.argv)
