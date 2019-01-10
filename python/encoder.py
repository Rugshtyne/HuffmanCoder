#!/usr/bin/env python3

import sys

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

	while byteStringLeftover:
		if len(byteStringLeftover) >= K:
			currentWord = byteStringLeftover[0:K]
			byteStringLeftover = byteStringLeftover[K:] # arba len(byteStringLeftover) ?
			if file is not None:
				record = [rec for rec in lookupTable if (rec['Character'] == currentWord)]
				if (len(record) > 0):
					fileInLine = fileInLine + record[0]['Path']
			else:
				createFreqTable(currentWord)
				# !!! createFreqTable(currentWord)
			currentWord = ""
		else:
			currentWord = byteStringLeftover
			isRemaining = K - len(byteStringLeftover)
			byteStringLeftover = ""

def processByte(byte, file=None):
	global currentWord
	global byteStringLeftover
	global isRemaining
	global fileInLine

	processByteStringLeftover(file)
	binary_str = format(ord(byte), 'b').zfill(8)
	compareTo = K if isRemaining == 0 else isRemaining
	if compareTo <= 8:
		currentWord += binary_str[:compareTo]
		byteStringLeftover = binary_str[compareTo:8]
		if file is not None:
			record = [rec for rec in lookupTable if (rec['Character'] == currentWord)]
			if (len(record) > 0):
				fileInLine = fileInLine + record[0]['Path']
		else:
   			createFreqTable(currentWord)
		currentWord = ""
		if isRemaining != 0:
			isRemaining = 0
	else:
		currentWord += binary_str
		isRemaining = compareTo - 8


def createFreqTable(byteString):
	record = [rec for rec in frequencyTable if (rec['Sequence'] == byteString)]
	if (len(record) == 0):
		record = { "Sequence": byteString, "Frequence": 1}
		frequencyTable.append(record)
	else:
		record[0]["Frequence"] = record[0]["Frequence"] + 1

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
		record = [rec for rec in lookupTable if (rec['Character'] == node.character)]
		if (len(record) == 0):
			record = { "Character": node.character, "Path": line}
			lookupTable.append(record)
		else:
			record[0]["Path"] = line

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


with open(sys.argv[1], "rb") as f:
	b = f.read(1)
	while b != b"":
		#my_bytes.append(format(ord(b), 'b').zfill(8))
		processByte(b)
		b = f.read(1)
	processByteStringLeftover(None)
	if currentWord:
		pass
		createFreqTable(currentWord)
	isRemaining = 0
	currentWord = ""
	root = CreateTree()
	buildCode(root,'')
	printTree(root)

	f.seek(0)
	b = f.read(1)
	while b != b"":
		processByte(b,"output")
		b = f.read(1)
	processByteStringLeftover("output")

	trailingZeros = len(treeInLine + fileInLine) % 8
	for i in range(0,trailingZeros):
		fileInLine = fileInLine + '0'

	print (treeInLine + fileInLine)