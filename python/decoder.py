#!/usr/bin/env python3

import sys

sys.setrecursionlimit(1500)

file = sys.argv[1]

K = 8
endingZeroes = 4
fileInLine = ''
lookupTable = []
reverseFile = ''

class Node():
	def __init__(self, character, freq, left, right):
		self.character = character
		self.freq = freq
		self.left = left
		self.right = right

	def checkIfLeaf(self):
		return (self.left == None and self.right == None)


def processFile(filename):
	global K
	global endingZeroes
	global fileInLine

	temp_fileInLine = fileInLine

	firstByteFlag = 0
	try:
		with open(filename, "rb") as f:
			b = f.read(1)
			count = 0
			while b != b"":
				print ("BYTE COUNT = ", count)
				print(b)
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
					temp_fileInLine += binary_str
				b = f.read(1)
				count += 1
			if endingZeroes != 0:
				temp_fileInLine = temp_fileInLine[:-endingZeroes]
			fileInLine = temp_fileInLine
			print(temp_fileInLine)
	except Exception as e:
		raise e

def restoreTree(tree):
	global fileInLine
	global K

	temp_K = K

	bit = fileInLine[:1]
	fileInLine = fileInLine[1:]
	if bit == "1":
		tree.left = Node(None,None,None,None)
		restoreTree(tree.left)
	else:
		tree.left = Node(fileInLine[:temp_K], None, None, None)
		fileInLine = fileInLine[temp_K:]

	bit = fileInLine[:1]
	fileInLine = fileInLine[1:]
	if bit == "1":
		tree.right = Node(None,None,None,None)
		restoreTree(tree.right)
	else:
		tree.right = Node(fileInLine[:temp_K], None, None, None)
		fileInLine = fileInLine[temp_K:]

def readRoot():
	global fileInLine
	bit = fileInLine[:1]
	fileInLine = fileInLine[1:]
	if bit == "1":
		return Node(None,None,None,None)
	else:
		return Node(fileInLine[:K], None, None, None)

def buildCode(node, line):
	global lookupTable
	temp_lookupTable = lookupTable

	if(node.checkIfLeaf() == False):
		buildCode(node.left, line + "0")
		buildCode(node.right, line + "1")
	else:
		record = [rec for rec in temp_lookupTable if (rec['Character'] == node.character)]
		if (len(record) == 0):
			record = { "Character": node.character, "Path": line}
			temp_lookupTable.append(record)
	lookupTable = temp_lookupTable

def decodeFile():
	global reverseFile
	global fileInLine
	global lookupTable

	temp_lookupTable = lookupTable
	temp_fileInLine = fileInLine
	temp_reverseFile = reverseFile

	currentSeq = ''
	count = 0

	print("LENGTH FILEINLINE = ", len(temp_fileInLine))
	input("PRESS ENTER")
	for i in range(len(temp_fileInLine)):
		print("INSIDE LENGTH FILEINLINE = ", len(temp_fileInLine))
		print("INSIDE DECODEFILE = ",count)
		currentSeq = currentSeq + temp_fileInLine[:1]
		temp_fileInLine = temp_fileInLine[1:]
		# record = next((x for x in frequencyTable if x['Sequence'] == byteString), None)
		# if (len(record) == 1):
		# 	#print currentSeq
		# 	temp_reverseFile = temp_reverseFile + record[0]['Character']
		# 	currentSeq = ''
		count += 1
	fileInLine = temp_fileInLine
	reverseFile = temp_reverseFile

def restoreFile():
	temp_reverseFile = reverseFile

	fileString = [temp_reverseFile[i:i+8] for i in range(0, len(temp_reverseFile), 8)]
	# print(fileString)

	fileName = sys.argv[1][:-4]
	fileName = fileName[:-4]+"_restored"+fileName[-4:]
	# print("FILENAME = ", fileName)

	finalByteArray = [int(x, 2) for x in fileString]
	finalByteArray = bytes(finalByteArray)


	with open(fileName, 'wb') as w:
		w.write(finalByteArray)


processFile(file)
tree = readRoot()
restoreTree(tree)
buildCode(tree, '')
print (lookupTable)
decodeFile()
print (reverseFile)
restoreFile()