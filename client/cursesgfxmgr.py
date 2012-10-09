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
	def __init__(self): 
		IGfxMgr.__init__(self) 	
		self.cursesScreen = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.cursesScreen.keypad(1)
		# set custom tenths of a second to wait before giving up on waiting for input
		curses.start_color() 
		curses.halfdelay(5)
	
	def updateWindowDimensions(self, numChars, numLines):
		IGfxMgr.updateWindowDimensions(self, numChars, numLines)

	def doQuit(self):
		curses.nocbreak()
		screen.keypad(0)
		curses.echo()
		curses.endwin()
		IGfxMgr.doQuit(self)

	def checkInput(self):
		c = screen.getch() 
		if c == curses.ERR:
			# then there has been no input
			return
		# otherwise, the user input something
		if c == ord('q') or c == curses.KEY_ESCAPE:
			self.doQuit()	
		elif self.keyIsEventable(c):
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
		if key >= 32 and key <= 126:
			return True
		else:
			return False 

	def keyIsEnter(self, key):
		if key == curses.KEY_ENTER:
			return True
		else:
			return False

	def keyIsBackspace(self, key):
		if key == curses.KEY_BACKSPACE:
			return True
		else:
			return False
	
	def clearScreen(self):
		screen.clear()
		return

	def blitNetScreen(self):
		if self.netScreen == None:
			self.blitDefaultScreen()
			return
		return

	def blitDefaultScreen(self):
		screen.addstr("Retrieving initial screen...", curses.A_BOLD)
		screen.refresh() 
		return

	def iterate(self):
		self.checkInput() 
		self.blitNetScreen()
		return

	#TODO: both these two move into interface
	def hasEvents(self):
		if len(self.outgoing) > 0:
			return True
		else:
			return False

	def popEvents(self):
		ret = self.outgoing[:]
		self.outgoing = []
		return ret

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
		screen.addstr(3, 0, "awww", curses.color_pair(1))
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
