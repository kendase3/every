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

screen = Screen()
#print str(screen)
print str(screen.screen[0][0]) 
fil = open("out2.bin", "wb") 
msg = bytearray() 
msg.extend(struct.pack("BB", screen.height, screen.width))  
for row in screen.screen:
	for asciipixel in row:
		msg.extend(struct.pack("BB", asciipixel.ascii, asciipixel.color)) 
fil.write(msg) 
fil.close() 
