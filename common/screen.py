#! /usr/bin/env python

import struct 
from itertools import izip

from asciipixel import AsciiPixel 

class Screen:
	"""
	stores a screen full of ascii characters
			and their respective RGB values

	i think the client should tell the server what size
			screen they want (number of tiles) 
	"""
	# units are in ascii pixels, not pixels
	DEFAULT_WIDTH = 5 
	DEFAULT_HEIGHT = 5 
	def __init__(self, screen=None): 
		# note that this makes the list row-major
		# 	i.e. y,x
		if screen == None:
			self.width = Screen.DEFAULT_WIDTH
			self.height = Screen.DEFAULT_HEIGHT
			# then initially populate with dummy cells
			# cool!  i almost never use list comprehensions!
			#FIXME: seems like too much processing work for something
			#	that is just going to be replaced anyway
			self.screen = [[AsciiPixel() for j in range(self.width)]
						for i in range(self.height)]
		else:
			self.screen = screen
			self.height = len(screen)
			self.width = len(screen[0]) 

	def setCell(self, cell, x, y):
		self.screen[y][x] = cell

	def getCell(self, x, y):
		return self.screen[y][x] 

	def setScreen(self, screen):
		self.screen = screen

	def getScreen(self):
		return self.screen

	def __repr__(self):
		ret = ""
		for row in self.screen:
			rowStr = ""
			for cell in row:
				rowStr += repr(cell) 
			ret += rowStr + '\n' 
		return ret

	def __str__(self):
		"""
		at least a little confusing that string does 
				something completely unlike repr in
				this case.  maybe use a different
				naming convention?  i mean, this
				is really just a custom pickle job
		"""
		ret = ""
		for row in self.screen:
			rowStr = ""
			for cell in row:
				rowStr += str(cell) 
				rowStr += "|" # ascii-pixel separator 
			ret += rowStr + '\n' 
		return ret

# note: not part of class
def destr(screenString):
	"""
	should return a valid screen object
			as defined by input string
			(think depickling)
	"""
	#print "making screen from this received string: %s" % screenString
	rowList = []
	curRow = []
	curAsciiStr = ""
	curStr = ""

	for ch in screenString:
		if ch == '\n':
			# then we are done with the row and append it
			# 	and start a new row
			rowList.append(curRow)
			curRow = []
		elif ch == '|':
			# then we're ready to make our current asciipixel 
			curAsciiPixel = AsciiPixel(int(curAsciiStr), int(curStr))
			curAsciiStr = curColorStr = ""
			curRow.append(curAsciiPixel)
			curStr = ""
		elif ch == ',':
			# then we're now building the color string
			curAsciiStr = curStr[:]
			curStr = ""
		else:
			curStr += ch

	ret = Screen(rowList) 
	return ret

def byte(screen):
	msg = bytearray() 
	msg.extend(struct.pack("BB", screen.height, screen.width))  
	for row in screen.screen:
		for asciiPixel in row:
			msg.extend(struct.pack(
					"BB", asciiPixel.ascii, AsciiPixel.getColorCode(
							asciiPixel.color[0], asciiPixel.bgColor[0]))) 
	return msg

def unbyte(screenBytes): 
	msg = bytearray()
	msg.extend(screenBytes) 
	width = 0
	height = 0
	asciiPixels = []
	curRow = [] 
	height, width = struct.unpack("BB", str(msg[:2])) 
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

if __name__=="__main__":
	#unit test
	screen = Screen()
	newCell = AsciiPixel(ord('a'), 255, 0, 0)	
	screen.setCell(newCell, 2, 0)
	print "repr of screen:"
	print repr(screen)	
	print "str of screen:"
	print str(screen)	
