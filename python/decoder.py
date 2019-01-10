#!/usr/bin/env python3

import sys

file = sys.argv[1]

K = 9999
endingZeroes = 9999


def processFile(filename):
	global K
	global endingZeroes

	firstByteFlag = 0
	mainString = ""
	try:
		with open(filename, "rb") as f:
			b = f.read(1)
			while b != b"":
				binary_str = format(ord(b), 'b').zfill(8)
				if firstByteFlag == 0:
					print("K = ",binary_str[:5])
					print("endingZeroes = ", binary_str[5:])
					K = int(binary_str[:5], 2)
					endingZeroes = int(binary_str[5:], 2)
					print("K = ", K)
					print("endingZeroes = ", endingZeroes)
					firstByteFlag = 1
				else:
					mainString += binary_str
				b = f.read(1)
			mainString = mainString[:-endingZeroes]
			print(mainString)
	except Exception as e:
		raise e

processFile(file)