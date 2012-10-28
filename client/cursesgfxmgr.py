#! /usr/bin/env python
import os, sys
import curses
from curses import wrapper # handles the wonk automatically and enables colors 
from curses import ascii # maybe? 

sys.path.insert(0, os.path.join("..", "common")) 
sys.path.insert(0, os.path.join("..")) 
from igfx import IGfxMgr
from stevent import Stevent
from screen import Screen
from asciipixel import AsciiPixel

class CursesGfxMgr(IGfxMgr):
	COLORS = (
		['WHITE', 'BLACK', 'RED', 'BLUE', 'YELLOW', 'GREEN', 'MAGENTA', 'CYAN'])
	DUMMY_CHAR = '~'
	DUMMY_COLOR = RED

	def __init__(self): 
		IGfxMgr.__init__(self) 	
		self.screenChanged = True
		self.numLines = 25
		self.numChars = 80 	# assume a standard nethack screen to begin 
							# (does not matter to curses)
		self.cursesScreen = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.cursesScreen.keypad(1)
		# set custom tenths of a second to wait before giving up on waiting for input
		curses.start_color() 
		#curses.use_default_colors()
		#curses.halfdelay(5)
		self.cursesScreen.nodelay(1)
		for i, bgColor in enumerate(CursesGfxMgr.COLORS):
			for j, fgColor in enumerate(CursesGfxMgr.COLORS):
				code = self.getColorCode(j, i)
				curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK) 
	
	def getCursesColor(colorStr):
		if colorStr == 'white':
			return curses.COLOR_WHITE
		elif colorStr == 'black':
			return curses.COLOR_BLACK
		elif colorStr == 'red':
			return curses.COLOR_RED
		elif colorStr == 'blue':
			return curses.COLOR_BLUE
		elif colorStr == 'yellow':
			return curses.COLOR_YELLOW
		elif colorStr == 'green':
			return curses.COLOR_GREEN
		elif colorStr == 'magenta':
			return curses.COLOR_MAGENTA
		elif colorStr == 'cyan':
			return curses.COLOR_CYAN
		else: # explode
			print "ERROR: UNKNOWN COLOR!  HAVE A NICE DAY"
			return None

	"""
	def getColorIndex(colorStr):
		if colorStr not in CursesGfxMgr.COLORS:
			"ERROR: COLOR %s NOT IN COLORS.  HAVE A NICE DAY." % colorStr 
			return None
		else:
			return CursesGfxMgr.COLORS.index(colorStr)
	"""

	def getColorCode(fg, bg=None):
		if bg == None:
			bg = self.getColorIndex('BLACK') 
		if isinstance(fg, str):
			fg = self.getColorIndex(fg)
		if isinstance(bg, str):
			bg = self.getColorIndex(bg) 
		return fg * 2**3 + bg

	def getColors(colorCode):
		fg = colorCode / 8
		bg = colorCode % 8
		return fg, bg
			
	def updateWindowDimensions(self, numChars, numLines):
		IGfxMgr.updateWindowDimensions(self, numChars, numLines)

	def updateScreen(self, netScreen):
		self.screenChanged = True
		IGfxMgr.updateScreen(self, netScreen)

	def doQuit(self):
		curses.nocbreak()
		self.cursesScreen.keypad(0)
		curses.echo()
		curses.endwin()
		IGfxMgr.doQuit(self)

	def checkInput(self):
		c = self.cursesScreen.getch() 
		if c == curses.ERR:
			# then there has been no input
			return
		# otherwise, the user input something
		if c == curses.ascii.ESC:
			self.doQuit()	
		elif self.keyIsEnter(c):
			newStevent = Stevent(Stevent.KEYDOWN, Stevent.ENTER)
			self.outgoing.append(newStevent)
		elif self.keyIsBackspace(c):
			newStevent = Stevent(Stevent.KEYDOWN, Stevent.BACKSPACE)
			self.outgoing.append(newStevent)
		elif self.keyIsTypeable(c):
			newStevent = Stevent(Stevent.KEYDOWN, c)
			self.outgoing.append(newStevent) 
		return

	def keyIsEventable(self, key):
		#TODO: move into ABC
		if self.keyIsEnter(key) or self.keyIsBackspace(key) or self.keyIsTypeable(key):
			return True
		else:
			return False

	def keyIsTypeable(self, key):
		if key >= 32 and key <= 126 or key == 15 or key == 17:
			return True
		else:
			return False 

	def keyIsEnter(self, key):
		if key == curses.ascii.LF:
			return True
		else:
			return False

	def keyIsBackspace(self, key):
		if key == curses.KEY_BACKSPACE:
			return True
		else:
			return False
	
	def clearScreen(self):
		self.cursesScreen.clear()
		return

	def blitNetScreen(self):
		if self.screenChanged == False:
			return
		if self.netScreen == None:
			self.blitDefaultScreen()
			return
		self.clearScreen() 
		if len(self.netScreen.screen) != self.numLines and (
				len(self.netScreen.screen[0]) != self.numChars):
			# then we require a window resize	
			newNumLines = len(self.netScreen.screen)
			newNumChars = len(self.netScreen.screen[0]) 
			self.updateWindowDimensions(newNumChars, newNumLines) 
		for i in range(0, self.netScreen.height):
			for j in range(0, self.netScreen.width):
				asciiPixel = self.netScreen.screen[i][j]
				# default is white on black
				colorPair = 0 
				if asciiPixel.ascii == AsciiPixel.DUMMY:
					asciiChar = CursesGfxMgr.DUMMY_CHAR
					colorPair = CursesGfxMgr.DUMMY_COLOR
				else:
					asciiChar = chr(asciiPixel.ascii)
					#FIXME: tsk tsk tsk.  manual iteration?
					if asciiPixel.color == AsciiPixel.BLUE:
						# then we set the color to blue
						colorPair = CursesGfxMgr.BLUE_PAIR
					elif asciiPixel.color == AsciiPixel.RED:
						# you get the idea
						colorPair = CursesGfxMgr.RED_PAIR
					elif asciiPixel.color == AsciiPixel.YELLOW:
						colorPair = CursesGfxMgr.YELLOW_PAIR
					elif asciiPixel.color == AsciiPixel.GREEN:
						colorPair = CursesGfxMgr.GREEN_PAIR
					elif asciiPixel.color == AsciiPixel.MAGENTA:
						colorPair = CursesGfxMgr.MAGENTA_PAIR
					elif asciiPixel.color == AsciiPixel.CYAN:
						colorPair = CursesGfxMgr.CYAN_PAIR 
					else:
						# if it's unknown, we just assume white
						colorNum = 0
				self.cursesScreen.addstr(i, j, asciiChar, curses.color_pair(colorPair))
		self.screenChanged = False
		return

	def blitDefaultScreen(self):
		self.clearScreen() 
		self.cursesScreen.addstr("Retrieving initial screen...", curses.A_BOLD)
		self.cursesScreen.refresh() 
		return

	def iterate(self):
		self.checkInput() 
		self.blitNetScreen()
		return

	#TODO: both these two move into interface
	def hasEvents(self):
		return IGfxMgr.hasEvents(self)

	def popEvents(self):
		return IGfxMgr.popEvents(self)

	def cleanup(self):
		#TODO: redundant with doQuit?  refactor!
		self.doQuit() 
		return


#TODO: get rid of this temporary crap below

def respondToInput(screen):
	problem = False
	c = screen.getch() 
	if c == curses.ERR: 
		problem = True
	screen.clear()
	if problem:
		screen.addstr(4, 0, "exception!", curses.A_BOLD)
	else:
		screen.addstr(4, 0, "no exception!", curses.A_BOLD)
	if c == ord('y'):
		screen.addstr(3, 0, "yussss", curses.color_pair(3))
		return True
	elif c == ord('n'):
		# mabe i need to turn somethign on or off like bold etc.
		screen.addstr(3, 0, "awww", curses.color_pair(4))
		return True
	elif c == ord('q'):
		return False
	else:
		screen.addstr(3, 0, "?!?", curses.color_pair(2))
		return True

def notWrapperInit(): 
	screen = curses.initscr()
	curses.noecho()
	curses.cbreak()
	screen.keypad(1)
	# set custom tenths of a second to wait before giving up on waiting for input
	curses.start_color() 
	curses.halfdelay(5)
	return screen
	
def hello(screen):
	#screen.attron(curses.A_BOLD)
	curses.halfdelay(5)
	screen.addstr("h", curses.A_BOLD)
	screen.addstr("e", curses.A_BOLD)
	screen.addstr("l", curses.A_BOLD)
	screen.addstr("l", curses.A_BOLD)
	screen.addstr("o", curses.A_BOLD)
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK) 
	curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK) 
	curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) 
	curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE) 
	screen.addstr(1, 0, '@', curses.color_pair(2)) 
	screen.addstr(2, 0, '@', curses.color_pair(3)) 
	#if curses.has_colors():
	#	screen.addstr("y")
	screen.refresh()
	while respondToInput(screen):
		screen.refresh()

def notWrapperCleanup(screen):
	curses.nocbreak()
	screen.keypad(0)
	curses.echo()
	curses.endwin()

if __name__ == "__main__":
	screen = notWrapperInit()
	hello(screen)
	notWrapperCleanup(screen)
