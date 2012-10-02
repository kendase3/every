#! /usr/bin/env python
"""
	right now i'm sending "123,142|02,133|" to send two asciipixels
	that's at least 8 bytes per asciipixel.  i'd like to make it more
	raw so that i send 2 bytes per asciipixel
"""
# external
import os
import sys
import struct 
sys.path.insert(0, os.path.join("..", "common")) 

# local 
from asciipixel import AsciiPixel 
from screen import Screen 

def writeScreen():
	screen = Screen()
	print str(screen)
	fil = open("out2.bin", "wb") 
	msg = bytearray() 
	msg.extend(struct.pack("BB", screen.height, screen.width))  
	for row in screen.screen:
		for asciipixel in row:
			msg.extend(struct.pack(
					"BB", asciipixel.ascii, asciipixel.color)) 
	fil.write(msg) 
	fil.close() 

def readScreen():
	fil = open("out2.bin", "rb") 
	msg = bytearray()
	msg.extend(fil.read()) 	
	fil.close() 
	print "msg|%s|end" % str(msg)
	print "msg len: %d"  % len(str(msg))
	width = 0
	height = 0
	asciiPixels = [] 	
	curRow = [] 
	#print msg[0]
	#print "len:%d" % len(str(msg[0]))
	height, width = struct.unpack("BB", str(msg[:2])) 
	print "height: %d, width %d" % (height, width)
	for i in range(0, height):
		# height and width are counting in ASCII PIXELS not bytes
		for j in range(0, width):
			curPos = 2 * (i * width + j) + 2 # 2=size of header 
			symbol, color = struct.unpack("BB", 
					str(msg[curPos:(curPos + 2)])) 
			asciiPixel = AsciiPixel(symbol, color) 
			curRow.append(asciiPixel)
		asciiPixels.append(curRow)
		curRow = [] 
	screen = Screen(asciiPixels) 
	return screen

print "read screen:"
read = readScreen()
print str(read) 
print "actual:"
otherScreen = Screen()
print str(otherScreen)

