
# external
import abc, os, sys 

sys.path.insert(0, os.path.join("..", "common")) 

# local
from stevent import Stevent
from screen import Screen
from asciipixel import AsciiPixel

class IGfxMgr: 
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def __init__(self):
		self.quit = False
		self.outgoing = [] 
		self.netScreen = None

	@abc.abstractmethod
	def updateWindowDimensions(self, numChars, numLines):
		self.numChars = numChars
		self.numLines = numLines
		# then custom logic to actually test/apply settings 
		return 

	@abc.abstractmethod
	def updateScreen(self, netScreen):
		self.netScreen = netScreen

	@abc.abstractmethod
	def doQuit(self): 
		newStevent = Stevent(Stevent.QUIT)
		self.outgoing.append(newStevent) 
		self.quit = True
	
	@abc.abstractmethod
	def checkInput(self):
		return

	@abc.abstractmethod
	def clearScreen(self):
		return

	@abc.abstractmethod
	def blitNetScreen(self):
		return 

	@abc.abstractmethod
	def blitDefaultScreen(self):
		return

	@abc.abstractmethod
	def iterate(self):
		return

	@abc.abstractmethod
	def hasEvents(self):
		if len(self.outgoing) > 0:
			return True
		else:
			return False
	
	@abc.abstractmethod
	def popEvents(self):
		ret = self.outgoing[:]
		self.outgoing = []
		return ret

	@abc.abstractmethod
	def cleanup(self):
		return
