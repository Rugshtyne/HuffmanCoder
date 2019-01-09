#!/usr/bin/env python3
import binascii

my_bytes = []

with open("tekstas.txt", "rb") as f:
	b = f.read(1)
	while b != b"":
		my_bytes.append(format(ord(b), 'b').zfill(8))
		b = f.read(1)

my_bytes = [int(x, 2) for x in my_bytes]

print("MY_BYTES:\n",my_bytes)

byteArray = bytearray(my_bytes)

print("BYTEARRAY:\n",byteArray)

newFile = open("test.bin", "wb")

newFile.write(byteArray)