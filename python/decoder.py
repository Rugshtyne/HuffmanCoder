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
	# global K
	# global endingZeroes
	# global fileInLine

	temp_K = 0
	temp_endingZeroes = 0
	temp_fileInLine = ""

	firstByteFlag = 0
	count = 1
	try:
		with open(filename, "rb") as f:
			b = f.read(1)
			while b != b"":
				#print("PROCESSING FILE... ", count)
				binary_str = format(ord(b), 'b').zfill(8)
				if firstByteFlag == 0:
					#print("K = ",binary_str[:5])
					#print("endingZeroes = ", binary_str[5:])
					temp_K = int(binary_str[:5], 2)
					temp_endingZeroes = int(binary_str[5:], 2)
					#print("K = ", K)
					#print("endingZeroes = ", endingZeroes)
					firstByteFlag = 1
				else:
					temp_fileInLine += binary_str
				count += 1
				b = f.read(1)
			K = temp_K
			endingZeroes = temp_endingZeroes
			if temp_endingZeroes != 0:
				temp_fileInLine = temp_fileInLine[:-temp_endingZeroes]
			return temp_K, temp_endingZeroes, temp_fileInLine
			#fileInLine = temp_fileInLine
			#print(fileInLine)
	except Exception as e:
		raise e


def restoreTree(tree, fileInLine):
	#global fileInLine
	bit = fileInLine[:1]
	fileInLine = fileInLine[1:]
	if bit == "1":
		tree.left = Node(None,None,None,None)
		fileInLine = restoreTree(tree.left, fileInLine)
	else:
		tree.left = Node(fileInLine[:K], None, None, None)
		fileInLine = fileInLine[K:]

	bit = fileInLine[:1]
	fileInLine = fileInLine[1:]
	if bit == "1":
		tree.right = Node(None,None,None,None)
		fileInLine = restoreTree(tree.right, fileInLine)
	else:
		tree.right = Node(fileInLine[:K], None, None, None)
		fileInLine = fileInLine[K:]
	return fileInLine


def readRoot(fileInLine):
	#global fileInLine
	bit = fileInLine[:1]
	fileInLine = fileInLine[1:]
	if bit == "1":
		return Node(None,None,None,None), fileInLine
	else:
		return Node(fileInLine[:K], None, None, None), fileInLine

def buildCode(node, line):
	if(node.checkIfLeaf() == False):
		buildCode(node.left, line + "0")
		buildCode(node.right, line + "1")
	else:
		record = next((x for x in lookupTable if x['Character'] == node.character), None)
		if (record == None):
			record = { "Character": node.character, "Path": line}
			lookupTable.append(record)


def decodeFile(root, reverseFile):
	#global reverseFile
	temp_reverseFile = reverseFile
	tree = root
	fileInArray = fileInLine
	for i in range(0,len(fileInArray)):
		if (fileInArray[i] == '0'):
			tree = tree.left
		else:
			tree = tree.right
		#print (tree, i)
		if(tree.left == None and tree.right == None):
			temp_reverseFile += tree.character 
			tree = root
	return temp_reverseFile

def restoreFile():
	#global reverseFile

	fileString = [reverseFile[i:i+8] for i in range(0, len(reverseFile), 8)]
	# print(fileString)

	fileName = sys.argv[1][:-4]
	fileName = fileName[:-4]+"_restored"+fileName[-4:]
	# print("FILENAME = ", fileName)

	finalByteArray = [int(x, 2) for x in fileString]
	finalByteArray = bytes(finalByteArray)


	with open(fileName, 'wb') as w:
		w.write(finalByteArray)

start_time = time.time()
print ("---------- LOAD FILE ----------")
K, endingZeroes, fileInLine = processFile(file)
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- BUILD ROOT ----------")
tree, fileInLine = readRoot(fileInLine)
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- BUILD TREE ----------")
fileInLine = restoreTree(tree, fileInLine)
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- BUILD CODE ----------")
buildCode(tree, '')
lookupTable.sort(key=lambda x: x['Path'])
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- DECODE FILE ----------")
reverseFile = decodeFile(tree, reverseFile)
#print (reverseFile)
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- RESTORE FILE ----------")
restoreFile()
print ("---------- END ----------")
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))