import sys
from boolean import *
from cave import *

"""
The simwumpus module contains classes related 
to simulating the wumpus world.
"""

class SimWumpus:
    """A simulation of the wumpus world."""

    def __init__(self):
	"""Creates an instance of a single cave."""
	self.cave = Cave()
        self.tick = 0

    def Execute(self):
		""" Executes the cave world a single time."""
		self.cave.PrintCave()
		self.cave.Execute()
		self.tick = self.tick + 1

    def Run(self):
		""" Keeps on executing the cave simulation while an end 
			condition hasn't been reached.
		"""
		while self.cave.EndCondition() == false:
			print "Tick = ", self.tick
			self.Step()
			#raw_input()

    def Start(self):
		""" Starts the simulation. """
		self.Run()

    def Pause(self):
		pass

    def Step(self):
		if self.cave.EndCondition() == false:
			self.Execute()
		else:
			self.Reset()

    def Reset(self):
		del self.cave
		self.cave = Cave()
		self.tick = 0

    def End(self):
		pass

    def Quit(self):
		sys.exit(0)

    def TimeStep(self):
		return self.tick

    def CaveSize(self):
		numRows = self.cave.NumRows()
		numCols = self.cave.NumColumns()
		return (numRows, numCols)

    def Score(self):
		pass

    def Moves(self):
		pass

    def AgentState(self):
		return self.cave.AgentState()

    def WumpusState(self):
		return self.cave.WumpusState()

    def GoldState(self):
		return self.cave.GoldState()

    def PitLocations(self):
		return self.cave.PitLocations()


def Main():
    simulation = SimWumpus()
    simulation.Run()

if __name__ == "__main__":
    Main()


