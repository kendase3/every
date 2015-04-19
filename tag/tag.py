#! /usr/bin/env python
"""
	a game of tag
"""

# external
import time
import random
import os
import sys

sys.path.insert(0, os.path.join("..", "common"))

# locals
from game import Game
from screen import Screen 
from cell import Cell
from asciipixel import AsciiPixel
from player import Player
from stevent import Stevent

class Board(Game):
	"""
	a lil' world
	"""
	WIDTH = 80 
	HEIGHT = 25 
	def __init__(self):
		self.players = [] 	
		self.haveIt = False
		self.board = [[Cell() for j in range(Board.WIDTH)]
				for i in range(Board.HEIGHT)] 

	def iterate(self):
		return

	def addPlayer(self, playerId): 
		targetX = random.randint(0, 9)
		targetY = random.randint(0, 9)
		targetCell = self.board[targetY][targetX]  
		while targetCell.player != None:
			targetX = random.randint(0, 9)
			targetY = random.randint(0, 9)
			targetCell = self.board[targetY][targetX]  
		playerColor = AsciiPixel.BLUE
		if self.haveIt:
			it = False
		else:
			it = True
			playerColor = AsciiPixel.RED
			self.haveIt = True
		newPlayer = Player(playerId, 
				playerColor, it, targetX, targetY) 	
		targetCell.player = newPlayer
		self.players.append(newPlayer) 
		print "appended %s" % str(newPlayer)
	
	def removePlayer(self, playerId):
		print "removePlayer fired! playerId=%d" % playerId 
		print "ok, here is the playerlist before anything happens:\n" % (
				#repr(self.players))
				self.players)
		targetPlayer = None
		found = False
		for i in range(0, len(self.players)):
			if self.players[i].id == playerId:
				found = True
				targetPlayer = self.players.pop(i) 
				break	
		if found == False:
			print "oh no!"
		if targetPlayer == None:
			print "That's weird!"
			return
		targetCell = self.board[targetPlayer.y][targetPlayer.x]
		targetCell.player = None
		if targetPlayer.isIt:
			self.haveIt = False
		return 

	def getPlayer(self, playerId):
		for player in self.players:
			if player.id == playerId:
				return player
		return None

	def handleInput(self, stevent, playerId):
		if stevent.type == Stevent.QUIT:
			self.removePlayer(playerId) 
		if stevent.type != Stevent.KEYDOWN:
			return
		#print "stevent=%s" % str(stevent) 
		xOffset = yOffset = 0
		if stevent.key == ord('a') or stevent.key == ord('h'):
			# then we move left 
			xOffset = -1
			yOffset = 0
		elif stevent.key == ord('d') or stevent.key == ord('l'):
			# then we move right
			xOffset = 1
			yOffset = 0
		elif stevent.key == ord('s') or stevent.key == ord('j'):
			# then we move down
			xOffset = 0
			yOffset = 1
		elif stevent.key == ord('w') or stevent.key == ord('k'):
			# then we move up
			xOffset = 0
			yOffset = -1
		else:
			# any other input is invalid
			return
		player = self.getPlayer(playerId)
		newX = (player.x + xOffset) % Board.WIDTH 
		newY = (player.y + yOffset) % Board.HEIGHT 
		if self.board[newY][newX].player != None:
			# then we dismiss the move
			targetPlayer = self.board[newY][newX].player
			print "player %d collided with player %d" % (
					player.id, targetPlayer.id)  
			if player.isIt:
				targetPlayer.isIt = True
				targetPlayer.color = AsciiPixel.RED
				player.isIt = False
				player.color = AsciiPixel.BLUE
		else:
			# then we allow the move
			self.board[player.y][player.x].player = None 
			self.board[newY][newX].player = player 
			player.x = newX
			player.y = newY

	def getScreen(self, playerId): 
		"""
		so let me get this straight, steve
			
		we first convert these cells into asciipixels
		and then these asciipixels into a string

		which begs the question, why not just direct conversion?
		"""
		#TODO: use player number to create custom screen
		rowList = []
		curRow = []
		for row in self.board:
			for cell in row:
				if cell.player == None:
					curRow.append(AsciiPixel(ord('_'), AsciiPixel.WHITE)) 
				else:
					curRow.append(AsciiPixel(ord('@'), cell.player.color))
			rowList.append(curRow)
			curRow = [] 
		screen = Screen(rowList)
		return screen
		
