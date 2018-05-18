#! /usr/env/python

import sys
import random
from agent import *
from boolean import *

WUMPUS = "Wumpus"
AGENT = "Agent"
ARROW = "Arrow"

randomizer = random.Random(42)

class Cave:
    """ 
    The Cave virtual environment in which the the wumpus lives in.
    The cave contains the gold, as well as numerous pits.
    The agent hunter, searches the cave trying to find the gold.  
    """

    def __init__(self, numRows=10, numColumns=10, pitChance=0.05):
		"""
		Cave constructor. Number of rows and number of columns is 
		specified at initialisation (defaults to a 10x10 grid).
		The pitChance, is the probability that there is a pit 
		in any given room in the cave.
		"""
		self.numRows = 0
		self.numColumns = 0
		self.pits = []
		self.goldPos = ()
		self.wumpusPos = ()
		self.wumpusAlive = false
		self.caveEvents = []
		self.agentPos = ()
		self.agentDir = Right
		self.agent = BumpAndTurnAgent()
		self.CreateRooms(numRows, numColumns)
		self.GeneratePits(pitChance)
		self.GenerateGold()
		self.GenerateWumpus()
		self.GenerateAgent()

    def AgentState(self):
		"""
		Returns the state of the agent, which includes
		his position, his direction, and the type of agent it is.
		"""
		return (self.agentPos, self.agentDir, self.agent.GetType())

    def WumpusState(self):
		"""
		Returns the state of the wumpus := pos + alive/dead
		"""
		return (self.wumpusPos, self.wumpusAlive)

    def GoldState(self):
		"""
		Returns the state of the gold in teh cave.
		"""
		return self.goldPos

    def PitLocations(self):
		"""
		Returns the list of rooms with pits in them in the cave.
		"""
		return self.pits

    def PrintCave(self):
        """
        Dumps a simple representation of the cave to stdout.  
        """ 
        print ""
        print "Gold = ", self.goldPos
        for i in range(1,self.numRows+1):
            for j in range(1,self.numColumns+1):
                if (i,j) in self.pits:
                    print "*",
                elif (i,j) == self.agentPos:
                    print "@",
                elif (i,j) == self.goldPos:
                    print "G",
                elif (i,j) == self.wumpusPos:
                    print "W",
                else:
                    print "O"
            print ""

    def CreateRooms(self, numRows, numColumns):
		""" 
		Creates the specified number of rows/columns 
		and hence rooms in the cave.
		"""
		self.numRows = numRows
		self.numColumns = numColumns

    def NumRows(self):
		""" Returns number of rows in the cave grid. """
		return self.numRows

    def NumColumns(self):
		""" Returns number of columns in the cave grid. """
		return self.numColumns
			
    def GeneratePits(self, pitChance):
		"""
		Generates pits in the cave. Goes through each room,
		and generates a random number between 0 and 1.
		If the number is less than the pitChance, then
		a pit is generated for that particular room.
		"""
		for row in range(1,self.numRows+1):
			for column in range(1,self.numColumns+1):
				if random.uniform(0,1) <= pitChance:
					self.pits.append( (row,column) )

    def GenerateGold(self):
		"""
		Selects a random room in the cave grid to place the gold.
		"""
		gRow = random.randrange(1,self.numRows + 1)
		gColumn = random.randrange(1,self.numColumns + 1)
		self.goldPos = (gRow,gColumn)

    def GenerateWumpus(self):
		"""
		Selects a random room in the cave grid to place the wumpus.
		"""
		wRow = random.randrange(1, self.numRows + 1, 1)
		wColumn = random.randrange(1, self.numColumns + 1, 1)
		self.wumpusPos = (wRow,wColumn)
		self.wumpusAlive = true

    def GenerateAgent(self):
		"""
		Sets the initial position of the agent to be (1,1), that is
		the start room (or entrance) facing in the right direction.
		"""
		self.agentPos = (1,1)
		self.agentDir = Right

    def Execute(self):
		"""
		Executes the cave environment for a single time step.
		Generates all the percepts for the agent, and passes
		them to the agent's perceive method. The agent
		then reasons about what actions to perform. The actions
		are obtained using the agent's act method and are then
		processed by the Cave environment using the 
		ProcessActions method.
		"""
		self.ProcessEnvironment()
		if self.agent.Alive() == true:
			percepts = self.GeneratePercepts()
			self.agent.Perceive(percepts)
			self.agent.Reason()
			actions = self.agent.Act()
			print "Actions = ", actions
			self.ProcessActions(actions)

    def ProcessEnvironment(self):
		"""
		Determines the state of the environment and kills
		the agent if the correct conditions have been met.
		If the aegnt is in the same room as the wumpus, 
		the wumpus kills the agent. If the agent is in the
		same room as a pit, the agent falls in the pit
		and dies.
		"""
		if self.agentPos == self.wumpusPos:
			self.KillAgent()

		if self.agentPos in self.pits:
			self.KillAgent()

    def GeneratePercepts(self):
		""" 
		Generates percepts for the agent given its current position
		in the cave. First all the adjacent rooms are found. Then going
		through all the adjacent rooms the percepts are generated.
		If the gold is in the same room that the agent is in,
		then the agent can perceive a Glitter.
		If there is a pit, then the agent can perceive a breeze.
		If there is a wumpus then the agent can perceive a stench.
		Finally, if there are any events which have been generated
		in the cave (such as the agent bumping into walls, or the 
		wumpus screaming) then these events are processed and turned
		into percepts for the agent.
		"""
		agentRow, agentColumn = self.agentPos
		adjacentRooms = self.FindAdjacentRooms(agentRow,agentColumn)	

		percepts = []

		currentRoom = (agentRow, agentColumn)
		if currentRoom == self.goldPos:
			percepts.append(Glitter)

		for room in adjacentRooms:
			if room in self.pits:
				percepts.append(Breeze)
			if room == self.wumpusPos:
				percepts.append(Stench)

		for event in self.caveEvents:
			percepts.append(event)

		self.caveEvents = []

		return percepts

    def ProcessActions(self, actions):
		"""
		Goes through the list of actions the agent has decided
		to perform this timestep and passes the to handler methods.
		"""
		for action in actions:
			if action == Forward:
				self.HandleForwardAction()
			elif action == TurnRight:
				self.HandleTurnRightAction()
			elif action == TurnLeft:
				self.HandleTurnLeftAction()
			elif action == Shoot:
				self.HandleShootAction()
			elif action == Climb:
				self.HandleClimbAction()

    def HandleForwardAction(self):
		"""
		Moves the agent forward one room according to the direction
		he is facing. If the agent hits a wall, a bump event is 
		generated and he remains in the same spot.
		"""
		row, col = self.agentPos
		direction = self.agentDir

		if direction == Right:
			col = col + 1
		elif direction == Left:
			col = col - 1
		elif direction == Up:
			row = row + 1
		elif direction == Down:
			row = row - 1
		else:
			print "Unknown Direction"
			sys.exit(-1)

		print "UPDATE DIR,ROW,COL = ", (direction,row,col)

		invalidColumn = col < 1 or col > self.numColumns
		invalidRow = row < 1 or row > self.numRows

		if invalidColumn or invalidRow:
			self.caveEvents.append(Bump)
		else:
			self.agentPos = (row,col)
			print "NEW AGENT POS = ", self.agentPos, (row,col)

    def HandleTurnRightAction(self):
		"""
		Changes the direction the agent is facing by 
		ninety degrees in the clockwise direction.
		"""
		dir = self.agentDir
		newDir = self.agentDir

		if dir == Up: 
			newDir = Right
		elif dir == Right:
			newDir = Down
		elif dir == Down:
			newDir = Left
		elif dir == Left:
			newDir = Up

		self.agentDir = newDir

    def HandleTurnLeftAction(self):
		"""
		Changes the direction the agent is facing by
		ninety degrees in the anti-clockwise direction.
		"""
		dir = self.agentDir
		newDir = self.agentDir

		if dir == Up:
			newDir = Left
		elif dir == Right:
			newDir = Up
		elif dir == Down:
			newDir = Right
		elif dir == Left:
			newDir = Down

		self.agentDir = newDir

    def HandleShootAction(self):
		"""
		First look at the direction the agent is facing. 
		Obtain a list of all the rooms in that row or column,
		and filter out the rooms behind the agent, and the room
		that the agent is in. Now that we have the rooms in 
		front of the agent, we check to see if the wumpus is
		in one of these remaining rooms. If this is the case,
		and the agent had just launched the arrow this time step,
		that means that we have killed the wumpus.
		"""
		dir = self.agentDir
		row, col = self.agentPos
		wumpusPos = self.wumpusPos

		startRow = endRow = 0
		startCol = endCol = 0	

		if dir == Up:
			startRow = row + 1
			endRow = self.NumRows()
			startCol = col
			endCol = col
		elif dir == Down:
			startRow = row - 1
			endRow = 1
			startCol = col
			endCol = col
		elif dir == Left:
			startRow = row
			endRow = row
			startCol = col - 1
			endCol = 1
		elif dir == Right:
			startRow = row
			endRow = row
			startCol = col + 1
			endCol = self.NumColumns()

		arrowPath = [(i,j) for i in range(startRow,endRow+1)
				for j in range(startCol,endCol+1)]

		if wumpusPos in arrowPath:
			self.KillWumpus()

    def KillWumpus(self):
		"""
		Kills the wumpus - the wumpus' alive flag is set to false, 
		and the wumpus lets out a scream. The scream is represented
		as an event that occurs in the cave environment.
		"""
		self.wumpusAlive = false
		self.caveEvents.append(Scream)

    def KillAgent(self):
		"""
		Kills the agent.
		"""
		self.agent.Die()

    def HandleClimbAction(self):
		"""
		If the agent is in the starting grid, it sets the 
		agent position to negative to indicate that it has
		left the cave by climbing out.
		"""
		if self.agentPos == (1,1):
			self.agentPos = (-1,-1)

    def FindAdjacentRooms(self,i,j):
		"""
		For a given room (i,j) in the cave, generates all the 
		possible adjacent rooms. Then filters them to make
		sure they are actually in the cave.
		"""
		possibleAdjacents = [(i+1,j), (i,j-1), (i,j+1), (i-1,j)]
		return filter(self.InCave, possibleAdjacents)

    def InCave(self,room):
		"""
		For a given room (i,j), determines if it is in the cave,
		and returns a boolean value to indicate the case.
		"""
		i,j = room
		if i < 1 or i > self.numRows or j < 1 or j > self.numColumns:
			return false
		else:
			return true

    def EndCondition(self):
		"""
		Returns true if the end conditions have been satisfied and
		true otherwise. The end conditions are if the agent is not
		alive (i.e. it is dead) or if it has left the cave.
		"""
		print "Agent Alive = ", self.agent.Alive()
		agentAlive = self.agent.Alive()
		agentPos = self.agentPos
		if agentPos == (-1,-1) or agentAlive == false:
			return true
		else:
			return false

