#! /usr/bin/env python
import curses
from curses import wrapper # handles the wonk automatically and enables colors 
from curses import ascii # maybe? 

def hello(screen):
	screen.addstr("hello")
	#print str(screen) 
	screen.refresh()

wrapper(hello)
