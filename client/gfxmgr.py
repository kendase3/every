#! /usr/bin/env python
"""
	should determine screen height/width
		create a certain number of rows/cols	
		allow user to write things
	should provide a gap then separate space
		for current thing being written
"""

#TODO: rename pygamegfx.py

import pygame
from pygame.locals import *
import sys, os 
from stevent import Stevent
from screen import Screen
from asciipixel import AsciiPixel

class GfxMgr:
	WIGGLE_ROOM_WIDTH = 70 
	WIGGLE_ROOM_HEIGHT = 100 
	FONT_RATIO = 7.0 / 5.0 # ratio of font height / width 
	#FONT_SIZE = 14 # i.e. font height 
	FONT_FILE = "freemonobold.ttf"
	DUMMY_CHAR = "~"
	DUMMY_RED = 255
	DUMMY_GREEN = 0
	DUMMY_BLUE = 0
	DEFAULT_NUM_CHARS = 80
	DEFAULT_NUM_LINES = 20
	
	def __init__(self):
		self.quit = False
		self.outgoing = []
		#init pygame
		pygame.init()
		info = pygame.display.Info()
		#print "width=%d, height=%d" % (info.current_w, info.current_h)
		self.winWidth = info.current_w - GfxMgr.WIGGLE_ROOM_WIDTH 
		self.winHeight = info.current_h - GfxMgr.WIGGLE_ROOM_HEIGHT 
		self.initialWinWidth = self.winWidth
		self.initialWinHeight = self.winHeight
		self.numChars = GfxMgr.DEFAULT_NUM_CHARS
		self.numLines = GfxMgr.DEFAULT_NUM_LINES
		self.fontWidth = self.winWidth / self.numChars
		fontSize1 = int(self.fontWidth * GfxMgr.FONT_RATIO)
		fontSize2 = self.winHeight / self.numLines
		self.fontSize = min(fontSize1, fontSize2)
		self.numLines = self.winHeight / self.fontSize 
		self.numChars = self.winWidth / self.fontWidth
 
		#TODO: numLines and numChars will be fixed

		# screen is what gfxmgr calls the literal graphics context
		self.screen = pygame.display.set_mode(
				(self.winWidth, self.winHeight))
		# netScreen is what gfxmgr calls the 'screen' object
		self.netScreen = None
		pygame.display.set_caption('EveryClient') 
		pygame.mouse.set_visible(0) # hide mouse
		self.clearScreen()
		if not pygame.font:
			print "no font module?!  totally freaking out!"
			sys.exit()
		self.font = self.loadFont(GfxMgr.FONT_FILE, self.fontSize) 

		# whether or not shift is pressed 
		self.shift = False

		# whether or not the screen has new something worth showing
		self.needBlit = True

	def updateWindowDimensions(self, numChars, numLines):
		self.numChars = numChars
		self.numLines = numLines
		self.fontWidth = self.initialWinWidth / numChars 
		self.fontSize = self.initialWinHeight / numLines  
		# we use the smaller of the two
		print "initial size=%d, width=%d" % (self.fontSize, self.fontWidth)
		self.fontWidth = int(min(self.fontWidth, self.fontSize / GfxMgr.FONT_RATIO))
		self.fontSize = int(min(self.fontSize, self.fontWidth * GfxMgr.FONT_RATIO)) 
		print "adjusted size=%d, width=%d" % (self.fontSize, self.fontWidth)
		self.winWidth = self.fontWidth * numChars 
		self.winHeight = self.fontSize * numLines  
		self.screen = pygame.display.set_mode((self.winWidth, self.winHeight))

	def doQuit(self): 
		print "gfxmgr noticed it was quitting time!"
		newStevent = Stevent(Stevent.QUIT)
		self.outgoing.append(newStevent)
		self.quit = True

	def checkInput(self): 
		for event in pygame.event.get():
			#print "processing event: %s" % str(event)
			# FIXME: AHA, it's not Stevent.Quit
			if event.type == QUIT:
				# we need to tell the server that this user quit
				self.doQuit()
			elif event.type == KEYDOWN: 
				print "noticed keydown event"
				if self.keyIsQuit(event.key): 
					# quit is basically the only thing handled locally
					# 	at least until this novelty fails
					self.doQuit()
				elif self.keyIsEnter(event.key):
					newStevent = Stevent(Stevent.KEYDOWN, ord('\n'))
					self.outgoing.append(newStevent)
				elif self.keyIsShift(event.key):
					#TODO: modify the keys typed
					self.shift = True
				elif self.keyIsEventable(event.key):
					# then we make a new input stevent and add it to the queue 
					#print "found eventable keypress"
					actualKey = self.shiftify(event.key)
					newStevent = Stevent(Stevent.KEYDOWN, actualKey)
					self.outgoing.append(newStevent)
					#print repr(self.outgoing)
			elif event.type == KEYUP:
				print "noticed keyup event"
				if self.keyIsShift(event.key):
					self.shift = False

	def keyIsEventable(self, key):
		if self.keyIsEnter(key) or self.keyIsBackspace(key) or self.keyIsTypeable(key):
			return True
		else:
			return False

	def keyIsQuit(self, key):
		if key == K_ESCAPE: # or key == ord('q') 
			return True
		else:
			return False

	def keyIsEnter(self, key):
		if key == K_RETURN: #i.e. carriage return 
			return True
		else:
			return False

	def keyIsTypeable(self, key):
		if key >= 32 and key <= 126 or key == 15 or key == 17:
			return True
		else:
			return False 
	
	def keyIsBackspace(self, key):
		if key == K_BACKSPACE: #i.e. backspace
			return True
		else:
			return False

	def keyIsShift(self, key):
		if key == K_LSHIFT or key == K_RSHIFT:
			return True
		else:
			return False

	def shiftIsPressed(self):
		if self.shiftPressed:
			return True
		else:
			return False

	def clearScreen(self): 
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0, 0, 0)) 

	def blit(self):
		self.blitNetScreen()

		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()

	def blitNetScreen(self):
		if self.needBlit == False:
			return
		# but if we do need a blit, get rid of that crap!
		self.clearScreen()
		if self.netScreen == None:
			self.blitDefaultScreen()
			self.needBlit = False
			return
		# we check to see if we need to resize the window
		if len(self.netScreen.screen) != self.numLines or (
				len(self.netScreen.screen[0]) != self.numChars):
			# then we require a window resize 
			newNumLines = len(self.netScreen.screen) 
			newNumChars = len(self.netScreen.screen[0])  
			self.updateWindowDimensions(newNumChars, newNumLines)
		#TODO: make a list of dirty lines and only update them  
		for i in range(0, self.netScreen.height):
			for j in range(0, self.netScreen.width): 
				asciiPixel = self.netScreen.screen[i][j] 
				# it's GfxMgr's job to decide how dummy pixels are rendered
				if asciiPixel.ascii == AsciiPixel.DUMMY:
					asciiChar = GfxMgr.DUMMY_CHAR
					redVal = GfxMgr.DUMMY_RED
					greenVal = GfxMgr.DUMMY_GREEN
					blueVal = GfxMgr.DUMMY_BLUE
				else:
					asciiChar = chr(asciiPixel.ascii)
					redVal = asciiPixel.getRed() 
					greenVal = asciiPixel.getGreen() 
					blueVal = asciiPixel.getBlue() 
				text = self.font.render(asciiChar, 1, (
						redVal, greenVal, blueVal)) 
				# textpos is x,y in pixels i think
				# NOTE: the font width is a lil flexible because of AA 
				textpos = (j * self.fontWidth, i * self.fontSize) 
				self.background.blit(text, textpos)
		self.needBlit = False

	def blitDefaultScreen(self):
		words = "Retrieving initial screen..."
		text = self.font.render(words, 1, (255, 255, 255))
		textpos = (0, 0) 
		self.background.blit(text, textpos)
			
	def loadFont(self, filename, size):
		"""
			navigates to the fonts directory and 
				loads the font i so thoughtfully put there	
		"""
		try:
			# assume font is in a directory called 'fonts' BESIDE our directory
			font = pygame.font.Font(os.path.join('..', 'fonts', filename), size)
		except IOError:
			print "Exploded attempting to retrieve font file"
			sys.exit()
		return font

	def iterate(self):
		self.checkInput()
		self.blit()

	def hasEvents(self):
		if len(self.outgoing) > 0:
			return True
		else:
			return False 

	def popEvents(self):
		ret = self.outgoing[:]
		self.outgoing = []
		return ret 

	def keyIsNumbery(self, key):
		if (key >= ord('0') and key <= ord('9')) or key == ord('/'):
			return True
		else:
			return False 

	def keyIsSpace(self, key):
		if key == ord(' '):
			return True
		else:
			return False

	def shiftify(self, key): 
		"""
			uses status of shift key to determine actual key sent	
		"""
		if self.shift == False or self.keyIsEnter(key) or (
				self.keyIsBackspace(key) or self.keyIsSpace(key)):
			return key
		else:
			# then things get pretty real
			if self.keyIsNumbery(key):
				# then (sigh) we handle them all manually
				if key == ord('`'):
					return ord('~')
				elif key == ord('1'):
					return ord('!')
				elif key == ord('2'):
					return ord('@')
				elif key == ord('3'):
					return ord('#')
				elif key == ord('4'):
					return ord('$')
				elif key == ord('5'):
					return ord('%')
				elif key == ord('6'):
					return ord('^')
				elif key == ord('7'):
					return ord('&')
				elif key == ord('8'):
					return ord('*')
				elif key == ord('9'):
					return ord('(')
				elif key == ord('0'):
					return ord(')')
				elif key == ord('-'):
					return ord('_')
				elif key == ord('='):
					return ord('+') 
				elif key == ord('/'):
					return ord('?')
			elif self.keyIsTypeable(key):
				# the lower-case letters are actually higher up in ascii table
				return key - 32
			else:
				print "uh, this key is not supported bro.  just returning it."
				return key

	def updateScreen(self, netScreen):
		self.netScreen = netScreen
		# then say we need a fresh blit 
		self.needBlit = True

	def cleanup(self):
		pygame.quit()

