
import abc

class Game:
	"""
		an abstract base class 
	"""
	__metaclass__ = abc.ABCMeta
	@abc.abstractmethod
	def __init__(self):
		return
	@abc.abstractmethod
	def addPlayer(self, playerNumber):
		return 
	@abc.abstractmethod
	def removePlayer(self, playerNumber):
		return
	@abc.abstractmethod
	def handleInput(self, stevent, playerIndex):
		return
	@abc.abstractmethod
	def getScreen(self, playerNumber):
		return

def getGame():
	subgames = []
	for subclass in Game.__subclasses__():
		subgames.append(subclass)	
	if len(subgames) == 0:
		print "ERROR: no implementation of game found"
	elif len(subgames) > 1:
		print "ERROR: more than one implementation of game found" 
	else:
		return subgames[0] 
