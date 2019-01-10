#!/usr/bin/env python3

import sys

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
					print("K = ",binary_str[:5])
					print("endingZeroes = ", binary_str[5:])
					K = int(binary_str[:5], 2)
					endingZeroes = int(binary_str[5:], 2)
					print("K = ", K)
					print("endingZeroes = ", endingZeroes)
					firstByteFlag = 1
				else:
					fileInLine += binary_str
				b = f.read(1)
			fileInLine = fileInLine[:-endingZeroes]
			print(fileInLine)
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


def buildCode(node, line):
	if(node.checkIfLeaf() == False):
		buildCode(node.left, line + "0")
		buildCode(node.right, line + "1")
	else:
		record = [rec for rec in lookupTable if (rec['Character'] == node.character)]
		if (len(record) == 0):
			record = { "Character": node.character, "Path": line}
			lookupTable.append(record)

def decodeFile():
	global reverseFile
	global fileInLine

	currentSeq = ''
	for i in range(len(fileInLine)):
		currentSeq = currentSeq + fileInLine[:1]
		fileInLine = fileInLine[1:]
		record = [rec for rec in lookupTable if (rec['Path'] == currentSeq)]
		if (len(record) == 1):
			#print currentSeq
			reverseFile = reverseFile + record[0]['Character']
			currentSeq = ''


processFile(file)
tree = Node(None,None,None,None)
restoreTree(tree)
buildCode(tree, '')
print (lookupTable)
decodeFile()
print (reverseFile)
