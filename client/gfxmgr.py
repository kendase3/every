#! /usr/bin/env python
"""
	should determine screen height/width
		create a certain number of rows/cols	
		allow user to write things
	should provide a gap then separate space
		for current thing being written
"""

import pygame
from pygame.locals import *
import sys, os
from stevent import Stevent
from screen import Screen
from asciipixel import AsciiPixel

#TODO: should have another class called rawgfx that manages ascii cell values
# ^ what?  why?!
class GfxMgr:
	WIGGLE_ROOM_WIDTH = 70 
	WIGGLE_ROOM_HEIGHT = 100 
	FONT_SIZE = 14 # i.e. font height 
	FONT_WIDTH = 10 
	FONT_FILE = "freemonobold.ttf"
	DUMMY_CHAR = "~"
	DUMMY_RED = 255
	DUMMY_GREEN = 0
	DUMMY_BLUE = 0
	
	def __init__(self):
		self.quit = False
		self.outgoing = []
		#init pygame
		pygame.init()
		info = pygame.display.Info()
		winWidth = info.current_w - GfxMgr.WIGGLE_ROOM_WIDTH 
		winHeight = info.current_h - GfxMgr.WIGGLE_ROOM_HEIGHT 
		self.numLines = winHeight / GfxMgr.FONT_SIZE
		self.numChars = winWidth / GfxMgr.FONT_WIDTH
		# screen is what gfxmgr calls the literal graphics context
		self.screen = pygame.display.set_mode((winWidth, winHeight))
		# netScreen is what gfxmgr calls the 'screen' object
		self.netScreen = None
		pygame.display.set_caption('EveryClient') 
		pygame.mouse.set_visible(0) # hide mouse
		self.clearScreen()
		if not pygame.font:
			print "no font module?!  totally freaking out!"
			sys.exit()
		self.font = self.loadFont(GfxMgr.FONT_FILE, GfxMgr.FONT_SIZE) 

		# whether or not shift is pressed 
		self.shift = False

	def updateWindowDimensions(self, numChars, numLines):
		self.numChars = numChars
		self.numLines = numLines
		winWidth = GfxMgr.FONT_WIDTH * numChars 
		winHeight = GfxMgr.FONT_SIZE * numLines  
		self.screen = pygame.display.set_mode((winWidth, winHeight))

	def checkInput(self): 
		for event in pygame.event.get():
			#print "processing event: %s" % str(event)
			if event.type == QUIT:
				self.quit = True
			elif event.type == KEYDOWN: 
				if self.keyIsQuit(event.key): 
					# quit is basically the only thing handled locally
					# 	at least until this novelty fails
					self.quit = True
				if self.keyIsShift(event.key):
					#TODO: modify the keys typed
					self.shift = True
				elif self.keyIsEventable(event.key):
					# then we make a new input stevent and add it to the queue 
					print "found eventable keypress"
					actualKey = self.shiftify(event.key)
					newStevent = Stevent(Stevent.KEYDOWN, actualKey)
					self.outgoing.append(newStevent)
					#print repr(self.outgoing)
			elif event.type == KEYUP:
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
		if key >= 32 and key <= 126:
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
		self.clearScreen()
		self.blitNetScreen()
		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()

	def blitNetScreen(self):
		if self.netScreen == None:
			self.blitDefaultScreen()
			return
		# we check to see if we need to resize the window
		if len(self.netScreen.screen) != self.numLines and (
				len(self.netScreen.screen[0]) != self.numChars):
			# then we require a window resize 
			newNumLines = len(self.netScreen.screen) 
			newNumChars = len(self.netScreen.screen[0])  
			self.updateWindowDimensions(newNumChars, newNumLines)
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
				# FIXME: not sure if FONT_SIZE works for height.  we'll see! 
				textpos = (j * GfxMgr.FONT_WIDTH, i * GfxMgr.FONT_SIZE) 
				self.background.blit(text, textpos)

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
		#print "blitting this screen: \n" + repr(self.netScreen)
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

	def shiftify(self, key): 
		"""
			uses status of shift key to determine actual key sent	
		"""
		if self.shift == False or self.keyIsEnter(key) or self.keyIsBackspace(key):
			return key
		else:
			# then things get pretty real
			if self.keyIsTypeable(key):
				# the upper-case letters are actually higher up in ascii table
				return key - 32
			elif self.keyIsNumbery(key):
				# then (sigh) we handle them all manually
				if key == '`':
					return '~'
				elif key == '1':
					return '!'
				elif key == '2':
					return '@'
				elif key == '3':
					return '#'
				elif key == '4':
					return '$'
				elif key == '5':
					return '%'
				elif key == '6':
					return '^'
				elif key == '7':
					return '&'
				elif key == '8':
					return '*'
				elif key == 9:
					return '('
				elif key == '0':
					return ')'
				elif key == '-':
					return '_'
				elif key == '=':
					return '+' 
			else:
				print "uh, this key is not supported bro.  just returning it."
				return key

	def updateScreen(self, netScreen):
		self.netScreen = netScreen
		# then blit it

	def cleanup(self):
		pygame.quit()

