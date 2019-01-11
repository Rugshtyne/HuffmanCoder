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
codes = []

class Node():
	path = ''
	def __init__(self, character, freq, left, right):
		self.character = character
		self.freq = freq
		self.left = left
		self.right = right

# my_bytes = [int(x, 2) for x in my_bytes]

# newFile = open("test.bin", "w+b")
# byteArray = bytearray(my_bytes)
# newFile.write(byteArray)

def processByteStringLeftover(file=None, root=None):
	global byteStringLeftover
	global currentWord
	global isRemaining

	while byteStringLeftover:
		if len(byteStringLeftover) >= K:
			currentWord = byteStringLeftover[0:K]
			byteStringLeftover = byteStringLeftover[K:] # arba len(byteStringLeftover) ?
			if file is not None:
				buildCode(root, '',currentWord)
			else:
				createFreqTable(currentWord)
			currentWord = ""
		else:
			currentWord = byteStringLeftover
			isRemaining = K - len(byteStringLeftover)
			byteStringLeftover = ""

def processByte(byte, file=None, root=None):
	global currentWord
	global byteStringLeftover
	global isRemaining

	processByteStringLeftover(file, root)
	binary_str = format(ord(byte), 'b').zfill(8)
	compareTo = K if isRemaining == 0 else isRemaining
	if compareTo <= 8:
		currentWord += binary_str[:compareTo]
		byteStringLeftover = binary_str[compareTo:8]
		if file is not None:
			buildCode(root, '',currentWord)
		else:
   			createFreqTable(currentWord)
		currentWord = ""
		if isRemaining != 0:
			isRemaining = 0
	else:
		currentWord += binary_str
		isRemaining = compareTo - 8


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

def buildCode(node, line, word):
	global fileInLine
	if(node.left != None and node.right	!= None):
		buildCode(node.left, line + "0", word)
		buildCode(node.right, line + "1", word)
	else:
		if(node.character == word):
			fileInLine += line


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

	

	#print("trailingZeros = ",trailingZeros)

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
		#my_bytes.append(format(ord(b), 'b').zfill(8))
		processByte(b)
		#count += 1
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
	#buildCode(root,'')
	#print(lookupTable)
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
	print ("---------- PRINT TREE ----------")
	printTree(root)
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
	print ("---------- WRITE FILE ----------")
	f.seek(0)
	b = f.read(1)
	count = 1
	while b != b"":
		#print("BYTE COUNT = ", count)
		processByte(b,"output", root)
		count += 1
		b = f.read(1)
	processByteStringLeftover("output",root)
	if len(treeInLine + fileInLine) % 8 != 0:
		trailingZeros = 8 - (len(treeInLine + fileInLine) % 8)
	
	for i in range(0,trailingZeros):
		fileInLine = fileInLine + '0'

	writeBytesToFile(sys.argv[1], K, trailingZeros, treeInLine, fileInLine)
	print ("---------- END ----------")
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
