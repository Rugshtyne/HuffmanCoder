#!/usr/bin/env python3

import sys

isRemaining = 0
K = int(sys.argv[2])
currentWord = ""
byteStringLeftover = ""



# my_bytes = [int(x, 2) for x in my_bytes]

# newFile = open("test.bin", "w+b")
# byteArray = bytearray(my_bytes)
# newFile.write(byteArray)

def processByteStringLeftover(file=None):
	global byteStringLeftover
	global currentWord
	global isRemaining

	while byteStringLeftover:
		if len(byteStringLeftover) >= K:
			currentWord = byteStringLeftover[0:K]
			byteStringLeftover = byteStringLeftover[K:] # arba len(byteStringLeftover) ?
			if file is not None:
				pass
				# for(LookupTable record : this.lookupTable) {
    #                 if(record.getCharacter().equals(this.currentWord)) {
    #                     //System.out.println(record.getTreePath());
    #                     this.appendFile(file, record.getTreePath());
    #                     break;
    #                 }
    #             }   
			else:
				print(currentWord)
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

	processByteStringLeftover()
	binary_str = format(ord(byte), 'b').zfill(8)
	compareTo = K if isRemaining == 0 else isRemaining
	if compareTo <= 8:
		currentWord += binary_str[:compareTo]
		byteStringLeftover = binary_str[compareTo:8]
		if file is not None:
			pass
			# for(LookupTable record : this.lookupTable) {
	#              if(record.getCharacter().equals(this.currentWord)) {
	#                  this.appendFile(file, record.getTreePath());
	#                  break;
	#              }
	#          }
		else:
   			print(currentWord)
   			# !!! createFreqTable(currentWord)
		currentWord = ""
		if isRemaining != 0:
			isRemaining = 0
	else:
		currentWord += binary_str
		isRemaining = compareTo - 8

with open(sys.argv[1], "rb") as f:
	b = f.read(1)
	while b != b"":
		#my_bytes.append(format(ord(b), 'b').zfill(8))
		processByte(b)
		b = f.read(1)