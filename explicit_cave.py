#! /usr/env/python

import random
from boolean import *

WUMPUS = "Wumpus"
AGENT = "Agent"
ARROW = "Arrow"

randomizer = Random(42)

class Room:
    	
    def __init__(self, hasGold=false, hasPit=false):
		self.gold = hasGold	
		self.pit = hasPit
		self.entities = []
    
	def PlacePit(self):
		self.pit = true
    
	def PlaceGold(self):
		self.gold = true
    
	def AddEntity(self, entity):
		self.entities.append(entity)
    
	def RemoveEntity(self, entity)
		if entity in self.entities:
			self.entities.remove(entity)


class Cave:
    	
    def __init__(self, numRows=10, numColumns=10, pitChance=0.2):
		self.rooms = []
		self.CreateRooms(numRows, numColumns)
		self.GeneratePits(pitChance)
		self.GenerateGold()
		self.GenerateWumpus()
		self.GenerateAgent()

    def CreateRooms(self, numRows, numColumns):
		for i in range(numRows):
			self.rooms.append([])
			for j in range(numColumns):
				self.rooms[i].append(Room())

    def NumRows(self):
		return len(self.rooms)

    def NumColumns(self):
		if len(self.rooms) > 1:
			return len(self.roooms[0])
		else:
			return 0
			
    def GeneratePits(self, pitChance):
		for row in rooms:
			columns = rooms[i]
			for room in columns:
				if uniform(0,1) <= pitChance: 
					room.PlacePit()

    def GenerateGold(self):
	gRow = random.randrange(1, numRows + 1, 1)
	gColumn = random.randrange(1, numColumns + 1, 1)
	rooms[gRow][gColumn].PlaceGold()

    def GenerateWumpus(self):
		wRow = random.randrange(1, numRows + 1, 1)
		wColumn = random.randrange(1, numColumns + 1, 1)
		rooms[wRow][wColumn].AddEntity(WUMPUS)

    def GenerateAgent(self):
		try:
			rooms[0][0].AddEntity(AGENT)
		except IndexError:
			print "Cave::GenerateAgent : IndexError"	



