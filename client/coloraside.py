#! /usr/bin/env python

WHITE = 0
BLACK = 1
RED = 2
YELLOW = 3
GREEN = 4
MAGENTA = 5
CYAN = 6

def getColorCode(fg, bg):
	return fg * 2**3 + bg

def getColors(colorCode):
	fg = colorCode / 8
	bg = colorCode % 8
	return fg, bg

code = getColorCode(RED, MAGENTA)
print code
fg, bg = getColors(code) 
print "fg=%d, bg=%d" % (fg, bg)
