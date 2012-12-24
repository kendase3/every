#! /usr/bin/env python

import struct

class Stevent:
	"""
		like an event but more handsome
	"""
	# event type constants
	KEYDOWN = 0
	KEYUP = 1
	QUIT = 2
	
	# handy ascii constants
	BACKSPACE = 8
	ENTER = ord('\n')
	QUESTION_MARK = 63 
	EXCLAIMATION_POINT = 33 

	def __init__(self, eventType, key=0): 
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

def byte(stevent):
	"""
		turn a stevent into a two-byte representation
	"""
	msg = bytearray()
	msg.extend(struct.pack("BB", stevent.type, stevent.key)) 
	return msg

def unbyte(steventBytes):		
	msg = bytearray()
	type, key = struct.unpack("BB", steventBytes) 	
	print "type=%d, key=%d" % (type, key) 
	stevent = Stevent(type, key)
	return stevent

if __name__=="__main__":
	# unit test
	stevent1 = Stevent(Stevent.KEYDOWN, ord('a'))
	print repr(stevent1)
	stevent2 = Stevent(Stevent.KEYUP, ord('?'))
	print repr(stevent2)
	stevent3 = Stevent(Stevent.QUIT)
	print repr(stevent3)
