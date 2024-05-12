#!/usr/bin/env python3
import sys

data = bytearray(sys.stdin.buffer.read())

for j in range(653):
    off = 0x334c + 20*j
    if data[off+3] == 1 and not 491 <= j <= 493:
        data[off+3] = 2
    if data[off+2] == 0 and data[off+3] >= 2:
        data[off+2] = 1
    #data[off+17] = 0

sys.stdout.buffer.write(data)
