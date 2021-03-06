#! /usr/bin/env python
"""
	comment coming soon!
"""

from twisted.internet import protocol, reactor
from twisted.protocols import basic
import pickle
import os
import sys
import time

# add ../common/ to search path
sys.path.insert(0, os.path.join("..", "common"))
# used to find game implementation
sys.path.insert(0, os.path.join("..", "game"))
sys.path.insert(0, os.path.join(".."))

# local
import stevent
from stevent import Stevent
import screen
#from player import Player
from asciipixel import AsciiPixel

#constants
PORT = 50025 
LINE_ENDING = "\r\n"
FPS = 1 

import binder
from game import Game, getGame 

class IngressProtocol(basic.LineReceiver):
	def __init__(self):
		# one day things like this, for now, just spit a default screen to all
		"""
		self.player = Player(self.factory.game) 
		self.factory.game.addPlayer(self.player)
		"""
	def connectionMade(self):
		"""
		Send MOTD, query a new user for their username
		"""
		self.factory.addUser(self)
		self.playerNum = self.factory.numPlayers
		self.factory.numPlayers += 1
		self.factory.board.addPlayer(self.playerNum)
		# we could send a welcome screen with "press x to continue" 
		#	and wait on x
		screen = self.factory.board.getScreen(self.playerNum)  
		transmission = self.packetize(screen)
		#print "sending this screen update...\n%s" % transmission 
		self.transport.write(str(transmission) + LINE_ENDING)

	def packetize(self, curScreen):
		"""
		the only thing we send are screens.
		"""
		# just assume it's a screen
		ret = screen.byte(curScreen) 
		return ret	

	def depacketize(self, string):
		ret = stevent.unbyte(string)
		return ret
		
	def lineReceived(self, line):
		"""
		it's a keypress or event of some kind from the client. 
		        really it's the game's responsibility.
				we should pass on to the game, which returns
				true if we need a new screen dump 
	
		for now i guess we are the game
		"""
		# we assume a single stevent is steve-sent
		stevent = self.depacketize(line) 		

		self.factory.board.handleInput(stevent, self.playerNum)
		print "handling input for player %d" % self.playerNum
		# then it's up to us to also check for quit, game shouldn't have to call us
		if stevent.type == Stevent.QUIT:
			print "Player %d quit!" % self.playerNum 
			self.handleQuit() 
		# to provide a feel of feedback, we respond to every keypress
		self.sendScreen()

	def sendScreen(self):
		screen = self.factory.board.getScreen(self.playerNum)  
		transmission = self.packetize(screen)
		#print "sending this screen update...\n%s" % transmission 
		self.transport.write(str(transmission) + LINE_ENDING) 

	def handleQuit(self):
		self.factory.removeUser(self)
		#self.transport.loseConnection()
		# abort causes immediate disconnect
		self.transport.loseConnection()

class IngressFactory(protocol.ServerFactory):
	protocol = IngressProtocol
	userList = []	
	def __init__(self):
		GameType = getGame()
		self.board = GameType()
		self.numPlayers = 0;

	def getUsers(self):
		return userList 

	def addUser(self, user):
		IngressFactory.userList.append(user)

	def removeUser(self, user):
		# we expect the game will handle its end
		# 	when it receives a quit event
		IngressFactory.userList.remove(user)
	
	def connectionLost(self, reason):
		print "we lost a connection :["

factory = IngressFactory()
reactor.listenTCP(PORT, factory)
reactor.startRunning(False)
lastSentScreen = time.time()
while True:
	reactor.iterate()
	if factory.board != None:
		factory.board.iterate()
		curTime = time.time()
		delta = curTime - lastSentScreen
		if delta > 1.0 / FPS:
			print "delta=%f > %f so sending screen!" % (delta, 1.0 / FPS)
			lastSentScreen = curTime
			for user in factory.userList:
				user.sendScreen()
