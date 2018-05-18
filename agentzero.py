from boolean import *
from agent import *

class AgentZero(Agent):
    """
    This is a first attempt at a hunter agent with at least
    some sort of semblance of intelligent behaviour.
    The agent is designed around the concept of a finite
    state machine. The different states represent the different
    things (or intentions/goals) the agent can do/have.
    """

    def __init__(self):
		Agent.__init__(self)
		self.myPos = (1,1)
		self.myDir = Right
		self.numRows = 1
		self.numCols = 1
		self.visitedRooms = []
		self.foundGold = false
		self.wumpusDead = false
		self.breezyRooms = []
		self.suspectedPits = []
		self.stinkyRooms = []
		self.suspectedWumpus = []
		self.actionHistory = []

		def Reason(self):
			self.actions = []
			self.BeliefRevision()
			if Bump in self.percepts:
				self.actions.append(TurnLeft)
			else:
				self.actions.append(Forward)
			self.percepts = []

    def BeliefRevision(self):
		"""
		Processes the agent's percepts to determine 
		the current situation the agent is in.
		The information perceived by the agent forces
		him to revise his beliefs about the world.
		"""
		for p in self.percepts:
			if p == Stench:
			self.ProcessStench()
			elif p == Breeze:
			self.ProcessBreeze()
			elif p == Glitter:
			self.ProcessGlitter()
			elif p == Bump:
			self.ProcessBump()
			elif p == Scream:
			self.ProcessScream()
			else:
			print "AgentZero::SA - Unknown Percept"

    def ProcessStench(self):
		"""
		Process stench
		"""
		self.stinkyRooms.append(self.myPos)
		rooms = self.FindAdjacentRooms()

    def ProcessBreeze(self):
		"""
		Process breeze
		"""
		self.breezyRooms.append(myPos)

    def ProcessGlitter(self):
		"""
		If I can perceive glitter, then I know I have found
		the gold. Yahoo! I'm now rich.
		"""
		self.foundGold = true

    def ProcessBump(self):
		"""
		"""
		pass

    def ProcessScream(self):
		"""
		"""
		self.wumpusDead = true






