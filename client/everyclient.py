#! /usr/bin/env python
"""
seems kind of like a misnomer, as the client should work
		independently of server type
"""

import os
import sys

sys.path.insert(0, os.path.join("..", "common")) 
# local imports
from netmgr import NetMgr

def frontendSelect():
	while True:
		choice = raw_input(
				"Please select your frontend:\n1) SDL\n2) Curses\n\n>") 
		choice = int(choice)
		if choice == 1:
			from gfxmgr import GfxMgr
			return GfxMgr
		elif choice == 2:
			from cursesgfxmgr import CursesGfxMgr
			return CursesGfxMgr

class SessionBuddy():
	"""
	session buddy does everything.
	session buddy is the only link between gfxmgr and netmgr. 
	net/gfxmgrs are responsible for providing hasMessages(), popMessages(),
			the other functions explicitly used in run
	"""
	def __init__(self): 
		host = raw_input('Please enter host>')
		#TODO: 2 or 1?
		if len(host) < 2:
			host = None
		gfxMgr = frontendSelect()
		self.gfxMgr = gfxMgr()
		self.netMgr = NetMgr(host) 
		if self.netMgr.failed: 
			print "Failed to connect to server.  Are you sure one is running at %s on port %d?" % (
					NetMgr.HOST, NetMgr.PORT)
		self.quit = False

	def run(self):
		while not self.netMgr.quit:
			#TODO: should this really be 1:1 as it is now?
			self.gfxMgr.iterate()
			self.netMgr.iterate()
			if self.gfxMgr.hasEvents():
				self.netMgr.sendEvents(self.gfxMgr.popEvents())
			if self.netMgr.hasScreen():
				self.gfxMgr.updateScreen(self.netMgr.popScreen())
		#FIXME: when gfxMgr quits, netMgr never hears about the disconnect from the client! 
		# we pump through the remaining events from gfxMgr
		self.cleanup()

	def cleanup(self):
		self.netMgr.cleanup()
		self.gfxMgr.cleanup()

def main():
	buddy = SessionBuddy()
	buddy.run() 

if __name__ == "__main__":
	main()
