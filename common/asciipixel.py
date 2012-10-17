#! /usr/bin/env python
class AsciiPixel:
	DUMMY = 255
	DEFAULT_ASCII = DUMMY 
	DEFAULT_RED = 255
	DEFAULT_GREEN = 255
	DEFAULT_BLUE = 255
	MAX_COLOR_INDEX = 4
	COLORS = []
	WHITE = 0, 'white', 255, 255, 255 
	COLORS.append(WHITE)
	BLACK = 1, 'black', 0, 0, 0 
	COLORS.append(BLACK)
	RED = 2, 'red', 255, 0, 0 
	COLORS.append(RED)
	GREEN = 3, 'green', 0, 255, 0 
	COLORS.append(GREEN)
	BLUE = 4, 'blue', 0, 0, 255 
	COLORS.append(BLUE)
	YELLOW = 5, 'yellow', 255, 255, 0
	COLORS.append(YELLOW)
	MAGENTA = 6, 'magenta', 255, 0, 255 #TODO: ? 
	COLORS.append(MAGENTA)
	CYAN = 7, 'cyan', 0, 255, 255 
	COLORS.append(CYAN)
	def __init__(self, ascii=DEFAULT_ASCII, 
				color=WHITE):
		if isinstance(ascii, int): 
			self.ascii = ascii
		else:
			self.ascii = ord(ascii) 
		# this lookup does add in some overhead every asciiPixel render
		if isinstance(color, int):
			for curColor in AsciiPixel.COLORS:
				if curColor[0] == color:
					self.color = curColor
		else:
			# we assume it's a full color list
			self.color = color
	
	def __repr__(self):
		if self.ascii == AsciiPixel.DUMMY:
			return "Dummy "
		ret = "(ASCII=%s," % chr(self.ascii)
		ret += " Color=%s) " % self.color[1] 
		return ret
	
	def __str__(self):
		return "%d,%d" % (self.ascii, self.color[0])

	def __eq__(self, other):
		if self.ascii == other.ascii and (
				self.color == other.color):
			return True
		else:
			return False	

	def getRed(self):
		return self.color[2]

	def getGreen(self):
		return self.color[3]
	
	def getBlue(self):
		return self.color[4]

if __name__=="__main__":
	"""
		asciipixel unit test
	"""
	defaultAP = AsciiPixel()
	print str(defaultAP)
