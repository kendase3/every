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
	DUMMY_CHAR = '~'
	DUMMY_COLOR = AsciiPixel.RED[0] 

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
		curses.start_color() 
		self.cursesScreen.nodelay(1)
		fil = open('debug', 'w')
		for bgColor in AsciiPixel.COLORS:
			for fgColor in AsciiPixel.COLORS:
				code = CursesGfxMgr.getColorCode(fgColor[0], bgColor[0])
				fgCursesColor = self.getCursesColor(fgColor[0])
				bgCursesColor = self.getCursesColor(bgColor[0])
				fil.write("code=%d,fg=%d,bg=%d" % (
						code, fgColor[0], bgColor[0]))
				curses.init_pair(code, fgCursesColor, bgCursesColor) 
		fil.close()

	def getCursesColor(self, colorIndex):
		if colorIndex == AsciiPixel.WHITE[0]:
			return curses.COLOR_WHITE
		elif colorIndex == AsciiPixel.BLACK[0]:
			return curses.COLOR_BLACK
		elif colorIndex == AsciiPixel.RED[0]:
			return curses.COLOR_RED
		elif colorIndex == AsciiPixel.BLUE[0]:
			return curses.COLOR_BLUE
		elif colorIndex == AsciiPixel.YELLOW[0]:
			return curses.COLOR_YELLOW
		elif colorIndex == AsciiPixel.GREEN[0]:
			return curses.COLOR_GREEN
		elif colorIndex == AsciiPixel.MAGENTA[0]:
			return curses.COLOR_MAGENTA
		elif colorIndex == AsciiPixel.CYAN[0]:
			return curses.COLOR_CYAN
		else: # explode
			print "ERROR: UNKNOWN COLOR!  HAVE A NICE DAY"
			return None

	@staticmethod
	def getColorCode(fg, bg=None):
		return AsciiPixel.getColorCode(fg, bg) + 1 

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
					#FIXME -SEK 
					colorPair = CursesGfxMgr.getColorCode(asciiPixel.color[0], asciiPixel.bgColor[0])
					#end
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
