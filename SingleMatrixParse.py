#!/usr/bin/env python3
import sys
import operator
import readline
import numpy
import scipy.io

# def retrieveStrings(str):
# 	filename = str(argv)
# 	outerI = 0;
# 	try:
# 		f = open(filename, 'r');
# 	except FileNotFoundError:
# 		print('File \'', argv, '\' not found.');
# 		exit(1);
# 	allData = f.read();
# 	i = allData.find('6464646464');
# 	while(i < allData.size() and i > 0)
# 		i = i + 10;
# 		tmpstr = allData.substr(i, i + 19200);
# 		allData = allData.substr( + 19200);
# 		if outerI = 0:
# 			strList = tmpstr;
# 		else:
# 			strList.append(tmpstr);
# 		outerI = outerI + 1;
# 		i = allData.find('6464646464');


# def createMatrix(data):



def main(argv):

	Matrix = numpy.arange(4800)
	Matrix = Matrix.reshape((60,80))
	x = 0;
	y = 0;
	z = 0;
	filename = str(argv)
	try:
		f = open(filename, 'r');
	except FileNotFoundError:
		print('File \'', argv, '\' not found.');
		exit(1);
	while True:
		chars = f.read(4);
		if(len(chars) != 4) : break
		if not chars: break
		num = (int(chars[0],16) * (16**3)) + (int(chars[1],16)  * (16**2)) + (int(chars[2],16) * 16) + int(chars[3],16)
		Matrix[y][x] = (num * 0.01) - 273.15;
		x = x + 1;
		if x >= 80:
			x = 0;
			y = y + 1;
		if y >= 60:
			print('Filled.');
			break
	print(Matrix);
	#Matrix = numpy.arange(4800)
	#Matrix = Matrix.reshape((80,60))
	scipy.io.savemat('cameraData.mat',mdict={'arr': Matrix})
	print('Success: Matrix stored in \'cameraData.mat\'.');

if __name__ == '__main__': # Note
	main(sys.argv[1])
