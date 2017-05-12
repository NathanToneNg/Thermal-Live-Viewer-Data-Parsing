#!/usr/bin/env python3
import sys
import operator
import readline
import numpy
import scipy.io

def retrieveStrings(filename):
	outerI = 0;
	strList = [];
	try:
		f = open(filename, 'r');
	except FileNotFoundError:
		print('File \'', filename, '\' not found.');
		exit(1);
	allData = f.read();
	i = allData.find('6464646464');
	while(i < len(allData) and i >= 0):
		i = i + 10;
		tmpstr = allData[i:i + 19200];
		allData = allData[i+19200:];
		strList.append(tmpstr);
		outerI = outerI + 1;
		i = allData.find('6464646464');
		if(len(strList) == 30): #this is for a specific case if you know the data past a certain point doesn't matter
			return strList;
	return strList


def createMatrix(data):
	Matrix = numpy.arange(4800)
	Matrix = Matrix.reshape((60,80))
	x = 0
	y = 0
	i = 0
	while True:
		if len(data) < i + 4:
			print('Did not fill');
			break
		chars = data[i:i + 4];
		num = (int(chars[0],16) * (16**3)) + (int(chars[1],16)  * (16**2)) + (int(chars[2],16) * 16) + int(chars[3],16)
		Matrix[y][x] = (num * 0.01) - 273.15;
		x = x + 1;
		if x >= 80:
			x = 0;
			y = y + 1;
		if y >= 60:
			print('Filled.');
			break
		i = i + 4;
	return Matrix;

def getAverageHighTemp(Matrix3):
	
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
		med = numpy.percentile(Matrix, 90);
		#print(med)
		for x in range(0,79):
			for y in range(0,59):
				if Matrix[y][x] > med + 2:
					summation += Matrix[y][x]
					counter += 1;
		if summation == 0:
			highTemps[z] = 0;
		else:
			highTemps[z] = summation / counter;
	print(highTemps);
	scipy.io.savemat('highTemps.mat',mdict={'arr': highTemps})





def main(argv):
	filename = str(argv)
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
	getAverageHighTemp(Matrix3);

	#scipy.io.savemat('cameraData.mat',mdict={'3d': Matrix3})
	#print('Success: 3D Matrix stored in \'cameraData.mat\'.');
	

	# Matrix = numpy.arange(4800)
	# Matrix = Matrix.reshape((60,80))
	# x = 0;
	# y = 0;
	# z = 0;
	# filename = str(argv)
	# try:
	# 	f = open(filename, 'r');
	# except FileNotFoundError:
	# 	print('File \'', argv, '\' not found.');
	# 	exit(1);
	# while True:
	# 	chars = f.read(4);
	# 	if(len(chars) != 4) : break
	# 	if not chars: break
	# 	num = (int(chars[0],16) * (16**3)) + (int(chars[1],16)  * (16**2)) + (int(chars[2],16) * 16) + int(chars[3],16)
	# 	Matrix[y][x] = (num * 0.01) - 273.15;
	# 	x = x + 1;
	# 	if x >= 80:
	# 		x = 0;
	# 		y = y + 1;
	# 	if y >= 60:
	# 		print('Filled.');
	# 		break
	# print(Matrix);
	# #Matrix = numpy.arange(4800)
	# #Matrix = Matrix.reshape((80,60))
	# scipy.io.savemat('cameraData.mat',mdict={'arr': Matrix})
	# print('Success: Matrix stored in \'cameraData.mat\'.');

if __name__ == '__main__': 
	main(sys.argv[1])
