
from twisted.internet import reactor
from twisted.protocols import basic
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
import pickle

import screen

class NetMgr:
	"""
		new abstraction:
		1) this module receives the latest screen from the server.
		2) this module sends all user input in the form of an event list to the server.
	"""
	HOST = "localhost"
	PORT = 50025
	LINE_ENDING = "\r\n"

	def __init__(self):
		reactor.connectTCP(NetMgr.HOST, NetMgr.PORT, IngressClientFactory(self))
		reactor.startRunning(False) 
		self.screen = None
		self.client = None
		self.quit = False
		self.failed = False

	def iterate(self):
		reactor.iterate()

	def sendEvents(self, outgoing):
		if self.client == None:
			print "No client!  =0 "
			return
		# otherwise, we'll need to pack up the messages and send them
		#FIXME: so are we sending strings?  or actual objects these days?
		# interesting complexity: am i always sending a list?  or sometimes just one event?
		outgoingEvents = pickle.dumps(outgoing)		
		print "sending..." + repr(outgoing)
		self.client.sendMessage(outgoingEvents) 

	def receiveScreen(self, screenString):
		"""
			the server has sent us an updated screen object
		"""
		print "RECEIVESCREEN HAPPENED!"
		self.screen = screen.destr(screenString)

	def popScreen(self):
		"""
			gets the screen and clears the 
				screen object so we know
				when we get a new one
		"""
		ret = self.screen 
		#TODO: uncomment
		#self.screen = None	
		return ret
	
	def hasScreen(self):
		"""
			returns whether or not there is a screen update
		"""
		if self.screen == None:
			return False
		else:
			return True

	def cleanup(self):
		reactor.stop()
		# allow the stop to actually be processed
		reactor.iterate()

class IngressClient(basic.LineReceiver):
	def __init__(self, netMgr):
		self.netMgr = netMgr 

	def lineReceived(self, line):
		# we assume it is a screen update 
		#	and pass it up to netMgr 
		print "WE CAUGHT A SCREEN!"
		self.netMgr.receiveScreen(line)

	def sendMessage(self, line):
		# send out the message
		self.transport.write(line + NetMgr.LINE_ENDING)

class IngressClientFactory(ReconnectingClientFactory):
	def __init__(self, netMgr):
		self.netMgr = netMgr

	def startedConnecting(self, connector):
		print 'Started to connect.'

	def buildProtocol(self, addr):
		print 'Connected.'
		print 'Resetting connection delay.'
		self.resetDelay()
		ic = IngressClient(self.netMgr)
		# the latest client is always the correct one
		self.netMgr.client = ic
		return ic

	def clientConnectionLost(self, connector, reason):
		print 'Lost connection!\n'
		print 'Reason: %s' % reason 
		#TODO: attempt reconnect instead of failing out
		#i.e. connector.connect()
		ReconnectingClientFactory.clientConnectionFailed(
				self, connector, reason) 
		self.netMgr.quit = True
	
	def clientConnectionFailed(self, connector, reason):
		self.netMgr.connectionFailed = True 
		self.netMgr.failed = True
		print 'Failed to connect to server.  Are you sure one is running at %s on port %d?' % (NetMgr.HOST, NetMgr.PORT)
		self.netMgr.quit = True

