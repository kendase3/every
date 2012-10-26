
from twisted.internet import protocol, reactor
from twisted.protocols import basic
import os, sys, time

LINE_ENDING = "\r\n"

class MasterMgr:
	SERVER_PORT = 50026
	CLIENT_PORT = 50027
	def __init__(self):
		reactor.listenTCP(Master.SERVER_PORT, ServerFactory(self)) 
		reactor.listenTCP(Master.CLIENT_PORT, ClientFactory(self)) 
		reactor.startRunning(False) 
		self.serverList = []
		self.clientList = []

	def iterate(self):
		reactor.iterate() 

class EveryServerProtocol(basic.LineReceiver):
	serverCtr = 0
	def __init__(self): 
		self.number = EveryServerProtocol.serverCtr
		EveryServerProtocol.serverCtr += 1
		
	def connectionMade(self):
		self.factory.master.addServer(self)
	
	def packetize(self, curScreen):
		ret = screen.byte(curScreen)

	def depacketize(self, string):
		ret = stevent.unbyte(string)
		return ret

	def lineReceived(self, line):
		stevent = self.depacketize(line)
		self.factory.master.handleInput(stevent, self.playerNum) 
		self.screen = self.factory.master.getScreen(self.playerNum) 
		self.sendScreen()

	def sendScreen(self):
		screen = self.factory.board.getScreen(self.playerNum)  
		transmission = self.packetize(screen)
		#print "sending this screen update...\n%s" % transmission 
		self.transport.write(str(transmission) + LINE_ENDING) 

class EveryServerFactory(protocol.ServerFactory, master): 
	protocol = EveryServerProtocol
	def __init__(self, master):
		self.master = master
class EveryClientProtocol(basic.LineReceiver):
	clientCtr = 0
	def __init__(self):
		self.number = EveryClientProtocol.clientCtr
		EveryClientProtocol.clientCtr += 1

	def connectionMade(self):
		self.master.addClient(self)

class EveryClientFactory(protocol.ServerFactory, master)
	protocol = EveryClientProtocol
	def __init__(self, master):
		self.master = master
