from boolean import *
import random

# ACTIONS
Forward = 0
TurnRight = 1
TurnLeft = 2
Shoot = 3
Climb = 4

#PERCEPTS
Stench = 0
Breeze = 1
Glitter = 2
Bump = 3
Scream = 4

# DIRECTIONS
Up = 0
Down = 1
Left = 2
Right = 3

AgentActions = [Forward, TurnRight, TurnLeft, Shoot, Climb]
AgentPercepts = [Stench, Breeze, Glitter, Bump, Scream]
AgentDirections = [Up, Down, Left, Right]

class Agent:
    """
    A base class to represent a basic hunter agent. 
    Can receive percepts from the environment, and send
    actions to the environment. Apart from it's percepts
    and actions to perform it has two basic beliefs.
    It knows if it is alive (or dead), and knows 
    if it has shot it's arrow.
    This agent does no reasoning. It's reasoning
    method should be over-ridden by child classes.
    """
    def __init__(self):
        self.agentType = "Agent"
        self.percepts = []
        self.actions = []
        self.alive = true
        self.shotArrow = false

    def SetType(self,agentType):
        self.agentType = agentType

    def GetType(self):
        return self.agentType

    def Alive(self):
        return self.alive

    def Die(self):
        self.alive = false

    def Perceive(self, percepts):
        "Perceiving the world = ", percepts
        self.percepts = percepts

    def Reason(self):
        pass

    def Act(self):
        return self.actions

    def AddAction(self, newAction):
        self.actions.append(newAction)

    def ClearActions(self):
        self.actions = []

    def ClearPercepts(self):
        self.percepts = []

class RandomAgent(Agent):
    """
    This agent chooses a random action to perform each time step.
    If the action is to shoot an arrow, it changes its belief that
    the arrow has been shot.
    """

    def __init__(self):
        Agent.__init__(self)
        self.SetType("RandomAgent")

    def Reason(self):
        self.ClearActions()
        randomAction = random.randrange(0, len(AgentActions))
        self.actions.append(AgentActions[randomAction]) 
        self.ClearPercepts()

	if Shoot in self.actions:
            self.shotArrow = true

class BumpAndTurnAgent(Agent):
    """
    This is a bump and turn agent. Each time step, the agent goes
    forward one time step. If the agent bumps into a wall, instead
    of going forward it just changes direction (we turn left in this
    case). This is like those simple remote control cars.
    """

    def __init__(self):
        Agent.__init__(self)
        self.SetType("BumpAndTurn")

    def Reason(self):
        self.ClearActions()
        print "PERCEPTS = ", self.percepts
        if Bump in self.percepts:
            self.actions.append(TurnLeft)
        else:
            self.actions.append(Forward)
        self.ClearPercepts()








