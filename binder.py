"""
	This class is to be filled out by the game creator
		for proper linkage. 
"""
import os
import sys

# ~~~~~
### SET THE PATH TO YOUR GAME FOLDER HERE
# sys.path.insert(0, os.path.join("path", "to", "your", "folder")
#sys.path.insert(0, os.path.join("..", "tag")) 
#sys.path.insert(0, os.path.join("..", "..", "battletyme")) 
sys.path.insert(0, os.path.join("..", "..", "pop")) 
sys.path.insert(0, os.path.join("..", "..", "hess")) 
# ~~~~~

# ~~~~~
### IMPORT YOUR GAME CLASS HERE 
# (must subclass Game class as found in server/game.py) 
#from tag import Board  
#from battletyme import Arena
#from pop import GameMgr 
from hess import GameMgr
# ~~~~~
