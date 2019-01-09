#!/usr/bin/env python3

my_bytes = [194, 255, 255, 255, 255, 252]

newFile = open("test.bin", "wb")
byteArray = bytes(my_bytes)
print(byteArray)
newFile.write(byteArray)