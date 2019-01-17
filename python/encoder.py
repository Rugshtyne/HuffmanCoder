#!/usr/bin/env python3

import sys
import time

isRemaining = 0
K = int(sys.argv[2])
currentWord = ""
byteStringLeftover = ""
frequencyTable = []
treeInLine = []
fileInLine = []
trailingZeros = 0
codes = []
dictionary = {}
reqBits = 0

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

def processByteStringLeftover(temp_currentWord, temp_byteStringLeftover,  temp_isRemaining, temp_fileInLine, file=None, root=None):
	while temp_byteStringLeftover:
		if len(temp_byteStringLeftover) >= K:
			temp_currentWord = temp_byteStringLeftover[0:K]
			temp_byteStringLeftover = temp_byteStringLeftover[K:] # arba len(byteStringLeftover) ?
			if file is not None:
				temp_fileInLine.append(buildCode(temp_currentWord))
			else:
				createFreqTable(temp_currentWord)
			temp_currentWord = ""
		else:
			temp_currentWord = temp_byteStringLeftover
			temp_isRemaining = K - len(temp_byteStringLeftover)
			temp_byteStringLeftover = ""
	return temp_currentWord, temp_byteStringLeftover, temp_isRemaining

def processByte(temp_currentWord, temp_byteStringLeftover, temp_isRemaining, temp_fileInLine, byte, file=None, root=None):

	temp_currentWord, temp_byteStringLeftover, temp_isRemaining = processByteStringLeftover(temp_currentWord, temp_byteStringLeftover, temp_isRemaining, temp_fileInLine, file, root)

	binary_str = format(ord(byte), 'b').zfill(8)
	compareTo = K if temp_isRemaining == 0 else temp_isRemaining
	if compareTo <= 8:
		temp_currentWord += binary_str[:compareTo]
		temp_byteStringLeftover = binary_str[compareTo:8]
		if file is not None:
			temp_fileInLine.append(buildCode(temp_currentWord))
		else:
   			createFreqTable(temp_currentWord)
		temp_currentWord = ""
		if temp_isRemaining != 0:
			temp_isRemaining = 0
	else:
		temp_currentWord += binary_str
		temp_isRemaining = compareTo - 8
	return temp_currentWord, temp_byteStringLeftover, temp_isRemaining

def createFreqTable(byteString):
	if(len(byteString) < K):
		global reqBits
		reqBits = K - len(byteString)
		for i in range(0,K - len(byteString)):
			byteString = byteString + '0'
	record = next((x for x in frequencyTable if x['Sequence'] == byteString), None)
	if (record == None):
		record = { "Sequence": byteString, "Frequence": 1}
		frequencyTable.append(record)
	else:
		record["Frequence"] = record["Frequence"] + 1

def CreateTree():
	treeArray = []
	shortestFlag = 0
	sortedTable = sorted(frequencyTable, key = lambda i: len(i['Sequence']))
	for record in sortedTable:
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

def buildCode(word):
	return dictionary[word]


def buildDict(node, s, dictionary):
	if node.character:
		if not s:
			dictionary[node.character] = "0"
		else:
			dictionary[node.character] = s
	else:
		buildDict(node.left, s+"0", dictionary)
		buildDict(node.right, s+"1", dictionary)


def printTree(treeInLine, tree):
	#global treeInLine
	#print("PIRMAS treeInLine: ", treeInLine)
	if(tree != None):
		if (tree.left == None and tree.right == None):
			treeInLine.append('0')
			treeInLine.append(tree.character)
		else:
			treeInLine.append('1')
			printTree(treeInLine, tree.left)
			printTree(treeInLine, tree.right)


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
		# print(currentWord)
		currentWord, byteStringLeftover, isRemaining = processByte(currentWord, byteStringLeftover, isRemaining, fileInLine, b)
		#count += 1
		b = f.read(1)
	currentWord, byteStringLeftover, isRemaining = processByteStringLeftover(currentWord, byteStringLeftover, isRemaining, fileInLine)
	if currentWord:
		createFreqTable(currentWord)
	isRemaining = 0
	currentWord = ""
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
	print ("---------- BUILD TREE ----------")
	root = CreateTree()
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
	print ("---------- BUILD DICIONARY -----")
	buildDict(root, "", dictionary)
	#print(dictionary)
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
	# print ("---------- BUILD CODE ----------")
	# #buildCode(root,'')
	#print(dictionary)
	#print(frequencyTable)
	# print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
	print ("---------- PRINT TREE ----------")
	printTree(treeInLine, root)
	treeInLine = "".join(treeInLine)
	#print("TREE: ", treeInLine)
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
	print ("---------- WRITE FILE ----------")
	f.seek(0)
	b = f.read(1)
	count = 1
	while b != b"":
		currentWord, byteStringLeftover, isRemaining = processByte(currentWord, byteStringLeftover, isRemaining, fileInLine, b,"output", root)
		count += 1
		b = f.read(1)

	#Prisegam nulius prie paskutinio
	if(len(currentWord) < K):
		# print("LAST WORD IN WRITE:")
		# print(currentWord)
		for i in range(0,K - len(currentWord)):
			currentWord = currentWord + '0'
	currentWord, byteStringLeftover, isRemaining = processByteStringLeftover(currentWord, byteStringLeftover, isRemaining, fileInLine, "output",root)
	fileInLine = "".join(fileInLine)


	reqBits_binary = "00000"
	if reqBits != 0:
		reqBits_binary = "{0:05b}".format(reqBits)

	treeInLine = reqBits_binary + treeInLine
	
	if len(treeInLine + fileInLine) % 8 != 0:
		trailingZeros = 8 - (len(treeInLine + fileInLine) % 8)
	
	for i in range(0,trailingZeros):
		fileInLine = fileInLine + '0'

	writeBytesToFile(sys.argv[1], K, trailingZeros, treeInLine, fileInLine)
	print ("---------- END ----------")
	print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
