#! /usr/bin/env python

#TODO: does it matter how big these are?  
# i think they're way smaller than a screen dump 
class Stevent:
	"""
		like an event but more handsome
	"""
	# event type constants
	KEYDOWN = 0
	KEYUP = 1
	QUIT = 2

	def __init__(self, eventType, key=None): 
		"""
			key is the number i.e. ord('a') not 'a'
		"""
		self.type = eventType
		self.key = key

	def __repr__(self):
		ret = "Event: "
		if self.type == Stevent.QUIT:
			ret += "Quit"
		else:
			if self.type == Stevent.KEYDOWN:
				ret += "keydown->"
			elif self.type == Stevent.KEYUP:
				ret += "keyup->"
			ret += "%d:%c" % (self.key, self.key)
		return ret

	def __str__(self):
		return repr(self)	

if __name__=="__main__":
	# unit test
	stevent1 = Stevent(Stevent.KEYDOWN, ord('a'))
	print repr(stevent1)
	stevent2 = Stevent(Stevent.KEYUP, ord('?'))
	print repr(stevent2)
	stevent3 = Stevent(Stevent.QUIT)
	print repr(stevent3)
