
# remember that ord('@') trick

class Player: 
	def __init__(self, id, color, isIt, x, y):
		self.id = id	
		self.color = color
		self.isIt = isIt
		self.x = x
		self.y = y
	
	def __repr__(self):
		return "hi!"
		#return "number=%d" % self.number 

	def __str__(self):
		return repr(self)
