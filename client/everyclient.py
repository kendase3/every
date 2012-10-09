#! /usr/bin/env python
"""
	seems kind of like a misnomer, as the client should work
			independently of server type
"""

import os
import sys

sys.path.insert(0, os.path.join("..", "common")) 
# local imports
from gfxmgr import GfxMgr 
from netmgr import NetMgr
from cursesgfxmgr import CursesGfxMgr

#FIXME: note that this 'solution' has yet to do anything and will probably be removed
LAST_HURRAH_LENGTH = 5 # how many times should we pump the network after quit?

class SessionBuddy():
	"""
		session buddy does everything.
		session buddy is the only link between gfxmgr and netmgr. 
		net/gfxmgrs are responsible for providing hasMessages(), popMessages(),
			the other functions explicitly used in run
	"""
	def __init__(self): 
		self.gfxMgr = CursesGfxMgr() 
		self.netMgr = NetMgr() 
		if self.netMgr.failed: 
			print "Failed to connect to server.  Are you sure one is running at %s on port %d?" % (
					NetMgr.HOST, NetMgr.PORT)
		self.quit = False

	def run(self):
		while not self.gfxMgr.quit and not self.netMgr.quit:
			#TODO: 60 fps code here
			# lawl good one steve
			self.gfxMgr.iterate()
			self.netMgr.iterate()
			if self.gfxMgr.hasEvents():
				self.netMgr.sendEvents(self.gfxMgr.popEvents())
			if self.netMgr.hasScreen():
				self.gfxMgr.updateScreen(self.netMgr.popScreen())
		#FIXME: when gfxMgr quits, netMgr never hears about the disconnect from the client! 
		# we pump through the remaining events from gfxMgr
		self.gfxMgr.iterate() 
		if self.gfxMgr.hasEvents():
			self.netMgr.sendEvents(self.gfxMgr.popEvents())
			for i in range(0, LAST_HURRAH_LENGTH):
				self.netMgr.iterate()
		self.cleanup()
	
	def cleanup(self):
		self.netMgr.cleanup()
		self.gfxMgr.cleanup()

def main():
	buddy = SessionBuddy()
	buddy.run() 

if __name__ == "__main__":
	main()
