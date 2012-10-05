
# external
import abc

# local
from stevent import Stevent
from screen import Screen
from asciipixel import AsciiPixel

class GfxMgr: 
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

	def doQuit(self): 
		newStevent = Stevent(Stevent.QUIT)
		self.outgoing.append(newStevent) 
		self.quit = True
	
	def checkInput(self):
		return

	def clearScreen(self):
		return

	def blitNetScreen(self):
		return 

	def blitDefaultScreen(self):
		return

	def iterate(self):
		return

	def hasEvents(self):
		if len(self.outgoing) > 0:
			return True
		else:
			return False
	
	def popEvents(self):
		ret = self.outgoing[:]
		self.outgoing = []
		return ret

	def cleanup(self):
		return
