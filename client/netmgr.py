
from twisted.internet import defer, reactor
from twisted.protocols import basic
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from time import sleep

# local
import screen
import stevent

class NetMgr:
	"""
		new abstraction:
		1) this module receives the latest screen from the server.
		2) this module sends all user input in the form of an event list to the server.
	"""
	HOST = "localhost"
	PORT = 50025
	LINE_ENDING = "\r\n"
	#TODO: should eventually prompt for host and port 
	# and remember a list of previously used hosts and ports
	# (or at least the last one) 

	def __init__(self, host=None):
		if host == None:
			host = NetMgr.HOST
		reactor.connectTCP(host, NetMgr.PORT, IngressClientFactory(self))
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
		#TODO: what if an event happens to match '\r\n'?  it could happen.
		for event in outgoing:	
			outBytes = stevent.byte(event)  
			self.client.sendMessage(str(outBytes)) 

	def receiveScreen(self, screenBytes):
		"""
			the server has sent us an updated screen object
		"""
		self.screen = screen.unbyte(screenBytes) 

	def popScreen(self):
		"""
			gets the screen and clears the 
				screen object so we know
				when we get a new one
		"""
		ret = self.screen 
		self.screen = None	
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
		if self.client != None:
			self.client.transport.loseConnection() 		
			#FIXME: should use deferreds and wait exact amount
			sleep(1) 
		reactor.stop()
		# allow the stop to actually be processed
		reactor.iterate()

class IngressClient(basic.LineReceiver):
	def __init__(self, netMgr):
		self.netMgr = netMgr 

	def lineReceived(self, line):
		# we assume it is a screen update 
		#	and pass it up to netMgr 
		#print "USING LINE MODE!"
		self.netMgr.receiveScreen(line)
	
	def sendMessage(self, line):
		# send out the message
		#print "sending|%s|" % (line + NetMgr.LINE_ENDING)
		#print "\nlen=%d" % len(line + NetMgr.LINE_ENDING)
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
		#print 'Reason: %s' % reason 
		ReconnectingClientFactory.clientConnectionFailed(
				self, connector, reason) 
		self.netMgr.quit = True
	
	def clientConnectionFailed(self, connector, reason):
		self.netMgr.failed = True
		print 'Failed to connect to server.  Are you sure one is running at %s on port %d?' % (NetMgr.HOST, NetMgr.PORT)
		self.netMgr.quit = True

