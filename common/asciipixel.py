#! /usr/bin/env python
class AsciiPixel:
	DUMMY = 255
	DEFAULT_ASCII = DUMMY 
	DEFAULT_RED = 255
	DEFAULT_GREEN = 255
	DEFAULT_BLUE = 255
	MAX_COLOR_INDEX = 4
	WHITE = 0
	BLACK = 1
	RED = 2
	GREEN = 3
	BLUE = 4
	"""
	YELLOW = 5
	ORANGE = 6
	PURPLE = 7
	PINK = 8
	"""
	def __init__(self, ascii=DEFAULT_ASCII, 
				color=WHITE):
		if type(ascii) is int: 
			self.ascii = ascii
		else:
			self.ascii = ord(ascii) 
		self.color = color
	
	def __repr__(self):
		if self.ascii == AsciiPixel.DUMMY:
			return "Dummy "
		ret = "(ASCII=%s," % chr(self.ascii)
		ret += " Color=%d) " % self.color 
		return ret
	
	def __str__(self):
		return "%d,%d" % (self.ascii, self.color)

	def __eq__(self, other):
		if self.ascii == other.ascii and (
				self.color == other.color):
			return True
		else:
			return False	

	def getRed(self):
		# only consider white, black, red, green, blue
		if self.color == AsciiPixel.WHITE or self.color == AsciiPixel.RED:
			return 255
		else:
			return 0

	def getGreen(self):
		if self.color == AsciiPixel.WHITE or self.color == AsciiPixel.GREEN:
			return 255
		else:
			return 0 
	
	def getBlue(self):
		if self.color == AsciiPixel.WHITE or self.color == AsciiPixel.BLUE:
			return 255
		else:
			return 0

if __name__=="__main__":
	"""
		asciipixel unit test
	"""
	defaultAP = AsciiPixel()
	print str(defaultAP)
