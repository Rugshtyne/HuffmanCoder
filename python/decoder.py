#!/usr/bin/env python3

import sys
import time

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

	firstByteFlag = 0
	try:
		with open(filename, "rb") as f:
			b = f.read(1)
			while b != b"":
				binary_str = format(ord(b), 'b').zfill(8)
				if firstByteFlag == 0:
					#print("K = ",binary_str[:5])
					#print("endingZeroes = ", binary_str[5:])
					K = int(binary_str[:5], 2)
					endingZeroes = int(binary_str[5:], 2)
					#print("K = ", K)
					#print("endingZeroes = ", endingZeroes)
					firstByteFlag = 1
				else:
					fileInLine += binary_str
				b = f.read(1)
			if endingZeroes != 0:
				fileInLine = fileInLine[:-endingZeroes]
			#print(fileInLine)
	except Exception as e:
		raise e

def restoreTree(tree):
	global fileInLine
	bit = fileInLine[:1]
	fileInLine = fileInLine[1:]
	if bit == "1":
		tree.left = Node(None,None,None,None)
		restoreTree(tree.left)
	else:
		tree.left = Node(fileInLine[:K], None, None, None)
		fileInLine = fileInLine[K:]

	bit = fileInLine[:1]
	fileInLine = fileInLine[1:]
	if bit == "1":
		tree.right = Node(None,None,None,None)
		restoreTree(tree.right)
	else:
		tree.right = Node(fileInLine[:K], None, None, None)
		fileInLine = fileInLine[K:]

def readRoot():
	global fileInLine
	bit = fileInLine[:1]
	fileInLine = fileInLine[1:]
	if bit == "1":
		return Node(None,None,None,None)
	else:
		return Node(fileInLine[:K], None, None, None)

def buildCode(node, line):
	if(node.checkIfLeaf() == False):
		buildCode(node.left, line + "0")
		buildCode(node.right, line + "1")
	else:
		record = next((x for x in lookupTable if x['Character'] == node.character), None)
		if (record == None):
			record = { "Character": node.character, "Path": line}
			lookupTable.append(record)

def decodeFile():
	global reverseFile
	global fileInLine

	currentSeq = ''
	for i in range(len(fileInLine)):
		currentSeq = currentSeq + fileInLine[:1]
		fileInLine = fileInLine[1:]
		record = next((x for x in lookupTable if x['Path'] == currentSeq), None)
		if (record != None):
			#print currentSeq
			reverseFile = reverseFile + record['Character']
			currentSeq = ''

def restoreFile():
	global reverseFile

	fileString = [reverseFile[i:i+8] for i in range(0, len(reverseFile), 8)]
	# print(fileString)

	fileName = sys.argv[1][:-4]
	fileName = fileName[:-4]+"_restored"+fileName[-4:]
	# print("FILENAME = ", fileName)

	finalByteArray = [int(x, 2) for x in fileString]
	finalByteArray = bytes(finalByteArray)


	with open(fileName, 'wb') as w:
		w.write(finalByteArray)

print ("---------- LOAD FILE ----------")
processFile(file)
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- BUILD ROOT ----------")
tree = readRoot()
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- BUILD TREE ----------")
restoreTree(tree)
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- BUILD CODE ----------")
buildCode(tree, '')
#print (lookupTable)
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- DECODE FILE ----------")
decodeFile()
#print (reverseFile)
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- RESTORE FILE ----------")
restoreFile()
print ("---------- END ----------")
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))