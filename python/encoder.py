#!/usr/bin/env python3

import sys
import time

isRemaining = 0
K = int(sys.argv[2])
currentWord = ""
byteStringLeftover = ""
frequencyTable = []
lookupTable = []
treeInLine = ''
fileInLine = ''
trailingZeros = 0

class Node():
	def __init__(self, character, freq, left, right):
		self.character = character
		self.freq = freq
		self.left = left
		self.right = right

	def checkIfLeaf(self):
		return (self.left == None and self.right == None)


# my_bytes = [int(x, 2) for x in my_bytes]

# newFile = open("test.bin", "w+b")
# byteArray = bytearray(my_bytes)
# newFile.write(byteArray)

def processByteStringLeftover(file=None):
	global byteStringLeftover
	global currentWord
	global isRemaining
	global fileInLine

	temp_byteStringLeftover = byteStringLeftover
	temp_currentWord = currentWord
	temp_isRemaining = isRemaining
	temp_fileInLine = fileInLine

	while temp_byteStringLeftover:
		if len(temp_byteStringLeftover) >= K:
			temp_currentWord = temp_byteStringLeftover[0:K]
			temp_byteStringLeftover = temp_byteStringLeftover[K:] # arba len(byteStringLeftover) ?
			if file is not None:
				record = next((x for x in lookupTable if x['Character'] == temp_currentWord), None)
				if record != None:
					temp_fileInLine += record['Path']
			else:
				createFreqTable(temp_currentWord)
			temp_currentWord = ""
		else:
			temp_currentWord = temp_byteStringLeftover
			temp_isRemaining = K - len(temp_byteStringLeftover)
			temp_byteStringLeftover = ""
	byteStringLeftover = temp_byteStringLeftover
	currentWord = temp_currentWord
	isRemaining = temp_isRemaining
	fileInLine = temp_fileInLine
	fileInLine = "".join(temp_fileInLine)

def processByte(byte, file=None):
	global currentWord
	global byteStringLeftover
	global isRemaining
	global fileInLine

	temp_currentWord = currentWord
	temp_byteStringLeftover = byteStringLeftover
	temp_isRemaining = isRemaining
	temp_fileInLine = fileInLine

	processByteStringLeftover(file)
	binary_str = format(ord(byte), 'b').zfill(8)
	compareTo = K if isRemaining == 0 else isRemaining
	if compareTo <= 8:
		temp_currentWord += binary_str[:compareTo]
		temp_byteStringLeftover = binary_str[compareTo:8]
		if file is not None:
			# pass
			record = next((x for x in lookupTable if x['Character'] == temp_currentWord), None)
			if record != None:
				temp_fileInLine += record['Path']
		else:
   			createFreqTable(temp_currentWord)
		temp_currentWord = ""
		if temp_isRemaining != 0:
			temp_isRemaining = 0
	else:
		temp_currentWord += binary_str
		temp_isRemaining = compareTo - 8
	currentWord = temp_currentWord
	byteStringLeftover = temp_byteStringLeftover
	isRemaining = temp_isRemaining
	fileInLine = temp_fileInLine


def createFreqTable(byteString):
	record = next((x for x in frequencyTable if x['Sequence'] == byteString), None)
	if (record == None):
		record = { "Sequence": byteString, "Frequence": 1}
		frequencyTable.append(record)
	else:
		record["Frequence"] = record["Frequence"] + 1

def CreateTree():
	treeArray = []
	for record in frequencyTable:
		node = Node(record['Sequence'], record['Frequence'], None, None)
		treeArray.append(node)

	while len(treeArray) > 1:
		left = removeMinFreq(treeArray)
		right = removeMinFreq(treeArray)
		parent = Node(None,left.freq+right.freq,left,right)
		treeArray.append(parent)
	return treeArray[0]

def removeMinFreq(list):
	list.sort(key=lambda x: x.freq)
	returnNode = list[0]
	list.remove(returnNode)
	return returnNode

def buildCode(node, line):
	if(node.checkIfLeaf() == False):
		buildCode(node.left, line + "0")
		buildCode(node.right, line + "1")
	else:
		record = next((x for x in lookupTable if x['Character'] == node.character), None)
		if (record == None):
			record = { "Character": node.character, "Path": line}
			lookupTable.append(record)
		else:
			record["Path"] = line

def printTree(tree):
	global treeInLine
	if(tree != None):
		if (tree.left == None and tree.right == None):
			treeInLine = treeInLine + '0'
			treeInLine = treeInLine + tree.character
		else:
			treeInLine = treeInLine + '1'
			printTree(tree.left)
			printTree(tree.right)

def writeBytesToFile(fileToWrite, K, trailingZeros, treeInLine, fileInLine):
	K_binary = "{0:05b}".format(K)

	
	if trailingZeros != 0:
		trailingZeros_binary = "{0:03b}".format(trailingZeros)
	else:
		trailingZeros_binary = "000"

	firstByte = K_binary + trailingZeros_binary

	#print("FIRSTBYTE = ",firstByte)

	treeAndFileString = treeInLine + fileInLine
	treeAndFileString = [treeAndFileString[i:i+8] for i in range(0, len(treeAndFileString), 8)]

	finalByteArray = [firstByte] + treeAndFileString

	#print("K_binary = ", K_binary)
	#print("trailingZeros_binary = ", trailingZeros_binary)
	# print("finalByteArray = ", finalByteArray)

	finalByteArray = [int(x, 2) for x in finalByteArray]
	finalByteArray = bytes(finalByteArray)


	with open(fileToWrite+'.huf', 'wb') as w:
		w.write(finalByteArray)


with open(sys.argv[1], "rb") as f:
	start_time = time.time()
	print ("---------- CREATES FREQ TABLE ----------")
	b = f.read(1)
	count = 1
	while b != b"":
		#print ("---------- FIRST READ ----------")
		#print("BYTES COUNT = ", count)
		#print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
		#my_bytes.append(format(ord(b), 'b').zfill(8))
		processByte(b)
		count += 1
		b = f.read(1)
	processByteStringLeftover()
	if currentWord:
		#pass
		createFreqTable(currentWord)
	isRemaining = 0
	currentWord = ""
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
	print ("---------- BUILD TREE ----------")
	root = CreateTree()
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
	print ("---------- BUILD CODE ----------")
	buildCode(root,'')
	print(lookupTable)
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
	print ("---------- PRINT TREE ----------")
	printTree(root)
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
	print ("---------- WRITE FILE ----------")
	f.seek(0)
	b = f.read(1)
	print("---------- SECOND READ ----------")
	count = 1
	while b != b"":
		print("BYTE COUNT = ", count)
		processByte(b,"output")
		count += 1
		b = f.read(1)
	processByteStringLeftover("output")

	#print("LENGTH = ", len(treeInLine + fileInLine))

	if len(treeInLine + fileInLine) % 8 != 0:
		trailingZeros = 8 - (len(treeInLine + fileInLine) % 8)
	
	for i in range(0,trailingZeros):
		fileInLine = fileInLine + '0'

	#print (treeInLine + fileInLine)
	#print (lookupTable)
	writeBytesToFile(sys.argv[1], K, trailingZeros, treeInLine, fileInLine)
	print ("---------- END ----------")
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
