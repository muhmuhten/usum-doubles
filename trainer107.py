#!/usr/bin/env python3
import struct
import sys

data = bytearray(sys.stdin.buffer.read())
assert(struct.unpack_from("<I", data, 20)[0] == len(data))

btafoff = 0xa64
BTAF, btafsize, btaflen = struct.unpack_from("<4sII", data, btafoff)
assert(BTAF == b'BTAF')
assert(btafsize == btaflen*16+12)
btafdata = memoryview(data)[btafoff:][:btafsize][12:]

bmifoff = 0xa64 + btafsize
BMIF, bmifhead, bmifsize = struct.unpack_from("<4sII", data, bmifoff)
assert(BMIF == b'BMIF')
bmifdata = memoryview(data)[bmifoff+bmifhead:][:bmifsize]

nextoff = 0
runningoff = 0
bmifaccum = bytearray()
for j in range(btaflen):
    ONE, base, succ, size = struct.unpack_from("<IIII", btafdata, 16*j)
    assert(ONE == 1)
    assert(base == nextoff)
    assert(base - (-size >> 3 << 3) == succ)
    nextoff = succ

    if size < 32:
        struct.pack_into("<IIII", btafdata, 16*j, 1, runningoff, runningoff, 0)
    else:
        assert(size == len(bmifdata[base:succ]))
        if size == 32:
            size *= 2
            bmifaccum += bmifdata[base:succ]
        bmifaccum += bmifdata[base:succ]
        struct.pack_into("<IIII", btafdata, 16*j, 1, runningoff, runningoff + size, size)
        runningoff += size

newdata = data[:bmifoff+bmifhead] + bmifaccum
struct.pack_into("<I", newdata, 20, len(newdata))
struct.pack_into("<I", newdata, bmifoff+8, len(bmifaccum))
sys.stdout.buffer.write(newdata)
