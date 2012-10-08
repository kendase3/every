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
	
	def updateWindowDimensions(self, numChars, numLines):
		IGfxMgr.updateWindowDimensions(self, numChars, numLines)

	def doQuit(self):
		IGfxMgr.doQuit(self)

	def checkInput(self):
		#TODO
		return
	
	def clearScreen(self):
		#TODO
		return

	def blitNetScreen(self):
		#TODO
		return

	def blitDefaultScreen(self):
		#TODO
		return

	def iterate(self):
		#TODO
		return

	def hasEvents(self):
		#TODO
		return

	def popEvents(self):
		#TODO
		return

	def cleanup(self):
		#TODO
		return

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

#wrapper(hello)
cur = CursesGfxMgr()
print "%d" % cur.quit
