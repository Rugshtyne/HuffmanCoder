#!/usr/bin/env python3

import sys
import time

file = sys.argv[1]

K = 8
endingZeroes = 4
fileInLine = ''
reverseFile = ''
reqBits = 0
class Node():
	def __init__(self, character, freq, left, right):
		self.character = character
		self.freq = freq
		self.left = left
		self.right = right

	def checkIfLeaf(self):
		return (self.left == None and self.right == None)


def processFile(filename):
	temp_K = 0
	temp_endingZeroes = 0
	temp_fileInLine = ""

	firstByteFlag = 0
	reqBitsFlag = 0
	count = 1
	try:
		with open(filename, "rb") as f:
			b = f.read(1)
			while b != b"":
				#print("PROCESSING FILE... ", count)
				binary_str = format(ord(b), 'b').zfill(8)
				if (reqBitsFlag == 0 and firstByteFlag == 1):
					print("REQFLAG")
					reqBits = int(binary_str[:5], 2)
					binary_str = binary_str[5:]
					temp_fileInLine += binary_str
					reqBitsFlag = 1
				elif firstByteFlag == 0:
					print("firstByteFlag")
					#print("K = ",binary_str[:5])
					#print("endingZeroes = ", binary_str[5:])
					temp_K = int(binary_str[:5], 2)
					temp_endingZeroes = int(binary_str[5:], 2)
					#print("K = ", K)
					#print("endingZeroes = ", endingZeroes)
					firstByteFlag = 1
				else:
					print("GOOD")
					temp_fileInLine += binary_str
				b = f.read(1)
			K = temp_K
			endingZeroes = temp_endingZeroes
			print(temp_fileInLine)
			if temp_endingZeroes != 0:
				temp_fileInLine = temp_fileInLine[:-temp_endingZeroes]
			return temp_K, temp_endingZeroes, temp_fileInLine, reqBits
	except Exception as e:
		raise e


def restoreTree(tree, fileInLine):
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
	bit = fileInLine[:1]
	fileInLine = fileInLine[1:]
	if bit == "1":
		return Node(None,None,None,None), fileInLine
	else:
		return Node(fileInLine[:K], None, None, None), fileInLine[K:]

def decodeFile(root, reverseFile):
	temp_reverseFile = reverseFile
	tree = root
	for i in range(0,len(fileInLine)):
		if (fileInLine[i] == '0'):
			tree = tree.left
		else:
			tree = tree.right
		#print (tree, i)
		if(tree.left == None and tree.right == None):
			#print("word: ", tree.character)
			temp_reverseFile += tree.character 
			tree = root
	return temp_reverseFile

def restoreFile():
	fileString = [reverseFile[i:i+8] for i in range(0, len(reverseFile), 8)]

	fileName = sys.argv[1][:-4]
	fileName = fileName[:-4]+"_restored"+fileName[-4:]

	finalByteArray = [int(x, 2) for x in fileString]
	finalByteArray = bytes(finalByteArray)


	with open(fileName, 'wb') as w:
		w.write(finalByteArray)


start_time = time.time()
print ("---------- LOAD FILE ----------")
K, endingZeroes, fileInLine, reqBits = processFile(file)
print("K: %s, zeroes: %s" % (K, endingZeroes))
print("PO LOAD:")
print(fileInLine)
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- BUILD ROOT ----------")
tree, fileInLine = readRoot(fileInLine)
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- BUILD TREE ----------")
print("FILEINLINE BEFORE TREE")
print(fileInLine)
fileInLine = restoreTree(tree, fileInLine)
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- DECODE FILE ----------")

reverseFile = decodeFile(tree, reverseFile)
print(reverseFile)
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))
print ("---------- RESTORE FILE ----------")
print("BEFORE REMOVAL:")
print(reverseFile)
reverseFile = reverseFile[:-reqBits]
print("AFTER:")
print(reverseFile)
restoreFile()
print ("---------- END ----------")
print("-- TIME ELAPSED: %s seconds --" % (time.time() - start_time))