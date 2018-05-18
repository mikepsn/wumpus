from boolean import *
from agent import *

def IncrementDictValue(dict, key):
	if key in dict.keys():
		dict[key] = dict[key] + 1
	else:
		dict[key] = 1

class AgentState:
    """
    Base class representing an agent state, 
    containing the name of the class and a reference 
    to the agent this state belongs to.
    """
    def __init__(self, agent, name):
    	self.agent = agent
		self.name = name

    def DetermineState(self):
		"""
		Determines if the agent should remain in the 
		current state or change to another state.
		"""
		pass

    def ExecuteState(self):
		"""
		Executes the behaviour required for the current state.
		"""
		pass

class GoForward(AgentState):
    """
    In this state the agent just keeps on going forward in
    whatever direction he is currently facing.
    """
    def __init__(self, agent):
		AgentState.__init__(self, agent, "GO_FORWARD")

    def DetermineState(self):
		"""
		If the agent has bumped into a wall, then it should change
		state to the ChangeRow state.
		"""
		if self.agent.bumpedIntoWall == true:
			self.agent.ChangeState(ChangeRow())

    def ExecuteState(self):
		"""
		In this state, the agent just does one thing
		each time step. Goes forward.
		"""
		self.agent.AddAction(Forward)

class ChangeRow(AgentState):
    """
    While in this state the agent starts in one row,
    and figures out how to change rows pointing in the
    opposite direction. This state has four sub-states.
    beginTurn = the agent does the first turn
    goForward = the agent moves to the next row
    endTurn = the agent does the final turn
    finished = finished change rows.
    """
    def __init__(self, agent):
		AgentState.__init__(self, agent, "CHANGE_ROW")
		self.initialDir = agent.direction
		self.beginTurn = 1
		self.goForward = 2
		self.endTurn = 3
		self.finished = 4
		self.state = self.beginTurn

    def DetermineState(self):
		"""
		If the agent has finished changing rows, then he may
		go back to going in the forward direction.
		"""
		if self.state == self.finished:
			self.agent.ChangeState(GoForward())

    def ExecuteState(self):
		"""
		If the agent is begining the turn, he turns, then
		goes forward, then followed by a completion turn.
		e.g. if facing right: Right, Forward, Right
		e.g. if facing left: Left, Forward, Left
		"""
		turn = Right
		if self.initialDir == Right or self.initialDir == Up: 
			turn = Right
		elif self.initialDir == Left or self.initialDir == Down:
			turn = Left

		if self.state == self.beginTurn:
			self.agent.AddAction(turn)
			self.state = self.goForward
		elif self.state == self.goForward:
			self.agent.AddAction(Forward)
			self.state = self.endTurn
		elif self.state == self.endTurn:
			self.agent.AddAction(turn)
			self.state = self.finished

class AvoidObstacle(AgentState):
    """
    In this state the agent tries to avoid an obstacle (pit or wumpus), 
    by trying to find a path around it. In all circumstances, if the
    obstacle is wumpus, the agent shoots in its current direction hoping
    to shoot it (this is a shoot first ask questions later policy).
    If the wumpus screams and it is destroyed, then the agent knows it
    is dead and this information can be used in the obstacle avoidance
    code.
    Once this is done, the agent can then focus on obstacle avoidance.
    Three possible paths are generated. 1) Straight, 2) Over 3) Under.
    Straight is considered because the agent may be feeling a breeze or
    stench from an cave room.
    Each generated path is assessed for feasability. Can the path be
    traversed without leaving the cave? Only the feasible paths are
    kept, the rest are ignored.
    Each feasible path is then assessed as to the level of risk it would
    take for the agent. The agent then selects the lowest risk path.
    If more than one path have the same risk, one is randomly chosen.
    If there is no feasable path...
    """
    def __init__(self, agent):
		AgentState.__init__(self, agent, "AVOID_OBSTACLE")

    def DetermineState(self):
		pass

    def ExecuteState(self):
		pass

    def GenerateStraightPath(self):
		dir = self.agent.direction
		i,j = self.agent.position
		paths = { Right : [ (i,j+1), (i,j+2) ], 
			Left  : [ (i,j-1), (i,j-2) ],
				Up    : [ (i-1,j), (i-2,j) ],
			Down  : [ (i+1,j), (i+2,j) ] }
		return paths[dir]

    def GenerateOverPath(self):
		dir = self.agent.direction
		i,j = self.agent.position
		paths = { Right : [ (i+1,j), (i+1,j+1), (i+1,j+2), (i,j+2) ],
			Left  : [ (i+1,j), (i+1,j-1), (i+1,j-2), (i,j-2) ],
			Up	: [ (i,j-1), (i-1,j+1), (), () ],
			Down	: [ ] }
		return paths[dir]

    def GenerateUnderPath(self):
		dir = self.agent.direction
		i,j = self.agent.position
		paths = { Right : [],
			Left  : [],
			Up	: [],
			Down	: [] }

class ReturnHome(AgentState):
    """
    The agent returns home by considering the path taken to
    get to the current room. The agent then follows the path 
    in reverse, until it reaches home at which time it climbs
    out of the cave.
    """
    def __init__(self, agent):
		import copy
		AgentState.__init__(self, agent, "RETURN_HOME")
		self.rooms = copy.copy(self.agent.visitedRooms)
		self.rooms.reverse()
		self.roomId = 0
		self.actionQ = []

    def DetermineState(self):
		pass

    def ExecuteState(self):
		if self.roomId == len(self.rooms):
			self.agent.AddAction(Climb)
		else:
			if len(self.actionQ) == 0:
			self.GenerateActions()

			self.agent.AddAction(self.actionQ.pop())

    def GenerateActions(self):
		thisRoom = self.rooms[self.roomId]
		nextRoom = self.rooms[self.roomId + 1]

		if thisRoom != self.agent.position:
			print "ReturnHome::Execute - Invalid Room: ", thisRoom, self.agent.position
		else:
			if self.Adjacent(thisRoom, nextRoom) == true:
			thisDir = self.agent.direction
			nextDir = self.NextRoomDirection(thisRoom, nextRoom)
			turnCmds = self.GenerateTurnCmds(thisDir, nextDir)
			self.actionQ = turnCmds + [Forward]
			self.actionQ.reverse()

    def Adjacent(self, thisRoom, nextRoom):
		i, j = thisRoom
		return nextRoom in [(i+1,j), (i,j-1), (i,j+1), (i-1,j)]

    def NextRoomDirection(self, thisRoom, nextRoom):
		i, j = thisRoom
		directions = { (i+1, j)   : Down,
					(i  , j-1) : Left, 
				(i  , j+1) : Right,
				(i-1, j)   : Up }

		return directions[nextRoom]
	    
    def GenerateTurnCommands(self, thisDir, nextDir):
		commands = { (Right, Right) : [],
				(Right, Left ) : [TurnRight, TurnRight],
				(Right, Up   ) : [TurnLeft],
				(Right, Down ) : [TurnRight],
				(Left,  Right) : [TurnLeft, TurnLeft],
				(Left,  Left ) : [],
				(Left,  Up   ) : [TurnLeft],
				(Left,  Down ) : [TurnRight],
				(Up,    Right) : [TurnLeft],
				(Up,    Left ) : [TurnRight],
				(Up,    Up   ) : [],
				(Up,    Down ) : [TurnRight, TurnRight],
				(Down,  Right) : [TurnRight],
				(Down,  Left ) : [TurnLeft],
				(Down,  Up   ) : [TurnLeft, TurnLeft],
				(Down,  Down ) : [] }

		return commands[(thisDir, nextDir)]

class AgentScan(Agent):
    """
    This agent searches the room in a scanning pattern.
    It keeps on going forward following the current row of rooms,
    until it bumps into a wall. It then changes rows, continuing 
    to go forward. If it can't change rows, it has realised it
    has reached the end of the cave.
    """
    def __init__(self):
		Agent.__init__(self)
		self.state = GoForward()
		self.bumpedIntoWall = false
		self.shotArrow = false
		self.direction = Right
		self.home = (1,1)
		self.position = (1,1)
		self.visitedRooms = [(1,1)]
		self.actionHistory = []
		self.foundGold = false
		self.wumpusDead = false
		self.breezyRooms = []
		self.suspectPits = {}
		self.stinkyRooms = []
		self.suspectWumpus = {}
		self.numRows = 10
		self.numCols = 10

    def ChangeState(self, newState):
		self.state = newState

    def Reason(self):
		self.ClearActions()
		self.BeliefRevision()
		self.state.DetermineState()
		self.state.ExecuteState()
		self.ClearPercepts()
		self.RememberActions()

    def RememberActions(self):
		self.actionHistory.append(self.actions)

    def ClearTransientBeliefs(self):
		self.bumpedIntoWall = false

    def BeliefRevision(self):	
		"""
		Processes the agent's percepts to determine 
		the current situation the agent is in.
		The information perceived by the agent forces
		him to revise his beliefs about the world.
		"""
		self.ClearTransientBeliefs()
		self.ConsiderPreviousActions()

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
			print "AgentScan::BeliefRevision - Unknown Percept"

    def ProcessStench(self):
		"""
		If a stench is perceived in the room, the agent's beliefs
		are updated to determine what this means. That is the agent
		does some reasoning based on the current percepts
		and past travels to try and determine the location of the
		wumpus.
		Adds the current room to the list of stinky rooms, if it
		isn't already there.
		Rooms adjacent to the current room are found. Only the 
		adjacent rooms which haven't been visited are
		considered. These rooms are added to the list of suspect pits.
		If the room is already in the list, then it's suspect level
		is incremented by one.
		"""
		if self.position not in self.stinkyRooms:
			self.stinkyRooms.append(self.position)
		adjacentRooms = self.FindAdjacentRooms()
		rooms = [i for in adjacentRooms if i not in self.visitedRooms]
		for room in rooms:
			IncrementDictValue(self.suspectWumpus, room)

    def ProcessBreeze(self):
		"""
		Adds the current room to the list of breezy rooms, if it
		isn't already there.
		Rooms adjacent to the current room are found. Only the 
		adjacent rooms which haven't been visited are
		considered. These rooms are added to the list of suspect pits.
		If the room is already in the list, then it's suspect level
		is incremented by one.
		"""
		if self.position not in self.breezyRooms:
			self.breezyRooms.append(self.position)
		adjacentRooms = self.FindAdjacentRooms()
		rooms = [i for i in adjacentRooms if i not in self.visitedRooms]
		for room in rooms:
			IncrementDictValue(self.suspectPits, room)

    def ProcessGlitter(self):
		"""
		If I can perceive glitter, then I know I have found
		the gold. Yahoo! I'm now rich.
		"""
		self.foundGold = true

    def ProcessBump(self):
		"""
		If I perceive a bump, it means I just bumped into a wall.
		This is a transient belief. It is only true for the moment.
		"""
		self.bumpedIntoWall = true

    def ProcessScream(self):
		"""
		If I  perceive a scream, it means the wumpus is dead.
		"""
		self.wumpusDead = true

    def ConsiderPreviousActions(self):
		"""
		Consider the consequences of my previous actions on my beliefs.
		This just considers the actions taken in the last time step, 
		and adjusts the agent's beliefs accordingly.
		"""
		previousActions = self.actionHistory[-1]
	
		for action in previousAtions:
			if action == Forward:
			self.ConsiderForwardAction()
			elif action == TurnRight:
			self.ConsiderTurnRightAction()
			elif action == TurnLeft:
			self.ConsiderTurnLeftAction()
			elif action == Shoot:
			self.ConsiderShootAction()
			elif action == Climb:
			self.ConsiderClimbAction()

    def ConsiderForwardAction(self):
		"""
		If my last action was a forward action, and I didn't
		bump into a wall, then I change what I believe about
		my current position, and what I believe about
		what rooms I have visited.
		"""
		if Bump not in self.percepts:
			row, col = self.position
			dir = self.direction

			if dir == Up:
			row = row + 1
			elif dir == Down:
			row = row - 1
			elif dir == Left:
			col = col - 1
			elif dir == Right:
			col = col + 1

			self.position = (row,col)
			self.visitedRooms.append(self.position)

    def ProcessTurnRight(self):
		"""
		If my previous action was to turn right, I now determine
		what I should believe about the new direction I am facing.
		"""
		dir = self.direction

		if dir == Up:
			self.direction = Right
		elif dir == Down:
			self.direction = Left
		elif dir == Left:
			self.direction = Up
		elif dir == Right:
			self.direction = Down

    def ProcessTurnLeft(self):
		"""
		If my previous action was to turn left, I now determine
		what I should believe about the new direction I am facing.
		"""
		dir = self.direction

		if dir == Up:
			self.direction = Left:
		elif dir == Down:
			self.direction = Right
		elif dir == Left:
			self.direction = Down
		elif dir == Right:
			self.direction = Up

    def ProcessShootAction(self):
		"""
		If one of my previous actions was to shoot the arrow, 
		I now believe I have shot it.
		"""
		self.shotArrow = true

    def ProcessClimbAction(self):
		"""
		I only believe that I have left the cave (-ve pos), if my
		previous action was a Climb action and my current position
		is in the start room.
		"""
		if self.position == (1,1):
			self.position = (-1,-1)

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



