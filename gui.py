#! /bin/env pythonw

import sys
from Tkinter import *
from boolean import *
from simwumpus import *

class CaveFrame(Frame):

    def __init__(self, root, caveState, numRows, numCols, scale):
		Frame.__init__(self,root,bg="red4")
		self.numRows = numRows
		self.numCols = numCols
		self.scale = scale
		self.layout = Frame(self, bg="gold")
		self.canvas = Canvas(self.layout, background="#000077", 
						width=621, height=480, 
						scrollregion=(0,0,800,600))
		self.items = []
		self.yscroll = Scrollbar(self.layout, bg="yellow", orient=VERTICAL, command=self.canvas.yview) 
		self.xscroll = Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)
		self.canvas.configure(yscrollcommand=self.yscroll.set)
		self.canvas.configure(xscrollcommand=self.xscroll.set)

		agent, wumpus, gold, pits = caveState

		self.DrawGrid()
		self.DrawPits(pits)
		self.DrawWumpus(wumpus)
		self.DrawAgent(agent)
		self.DrawGold(gold)

		self.layout.pack(side=TOP, expand=1, fill=BOTH)
		self.canvas.pack(side=LEFT, expand=1, fill=BOTH)
		self.yscroll.pack(side=RIGHT, expand=1, fill=Y)
		self.xscroll.pack(side=BOTTOM, expand=1, fill=X)

    def Update(self, caveState):
		for id in self.items:
			self.canvas.delete(id)

		agent, wumpus, gold, pits = caveState

		self.DrawGrid()
		self.DrawPits(pits)


    def DrawGrid(self):
		width = self.numCols + 1
		height = self.numRows + 1
		color = "white"
		scale = self.scale
		
		for row in range(1,height+1):
			x1, y1 = (row*scale, scale)
			x2, y2 = (row*scale, width*scale)
			self.canvas.create_line(x1,y1,x2,y2, fill=color, width=2)
			
			if row < height:
				id = self.canvas.create_text(x1+scale/2,y1-scale/2, text=str(row), fill=color)
				self.items.append(id)

			for col in range(1,width+1):
				x3, y3 = (scale, col*scale)
				x4, y4 = (height*scale, col*scale)
				self.canvas.create_line(x3,y3,x4,y4, fill=color, width=2)
				if col < width:
					id = self.canvas.create_text(x3-scale/2,y3+scale/2, text=str(col), fill=color)
					self.items.append(id)

    def DrawPits(self, pits):
		scale = self.scale
		r = scale/2.5
		for pit in pits:
			x,y = pit
			adjacentRooms = self.FindAdjacentRooms(x,y)	
			x = (x*scale) + scale/2.0
			y = (y*scale) + scale/2.0
			id = self.canvas.create_rectangle(x-r,y-r,x+r,y+r,fill="black")
			self.items.append(id)

			for breezyRoom in adjacentRooms:
				if breezyRoom not in pits:
					r = scale/6
					u,v = breezyRoom
					u = (u*scale) + scale/2
					v = (v*scale) + scale/2
					id = self.canvas.create_oval(u-r,v-r,u+r,v+r,outline="green")
					self.items.append(id)
					r = scale/2.5

    def DrawWumpus(self, wumpus):
		scale = self.scale
		r = scale/4.0
		wumpusPos, wumpusAlive = wumpus
		x,y = wumpusPos
		adjacentRooms = self.FindAdjacentRooms(x,y)
		x = (x*scale) + scale/2
		y = (y*scale) + scale/2
		id = self.canvas.create_oval(x-r,y-r,x+r,y+r,fill="red")
		self.items.append(id)

		for smellyRoom in adjacentRooms:
			u,v = smellyRoom
			u = (u*scale) + scale/2
			v = (v*scale) + scale/2
			id = self.canvas.create_oval(u-r,v-r,u+r,v+r, fill="orange")
			self.items.append(id)

    def DrawGold(self, gold):
		scale = self.scale
		r = scale/8
		goldPos = gold
		x,y = goldPos
		x = (x*scale) + scale/2
		y = (y*scale) + scale/2
		id1 = self.canvas.create_oval(x-3*r, y-3*r, x+3*r, y+3*r, fill="yellow")
		id2 = self.canvas.create_oval(x-2*r, y-2*r, x+2*r, y+2*r, fill="yellow4")
		id3 = self.canvas.create_oval(x-r,y-r,x+r,y+r,fill="yellow")
		self.items.append(id1)
		self.items.append(id2)
		self.items.append(id3)

    def DrawAgent(self, agent):
		scale = self.scale
		agentPos, agentDir, agentType = agent
		r = scale/4
		x,y = agentPos
		x = (x*scale) + scale/2
		y = (y*scale) + scale/2
		id = self.canvas.create_oval(x-r,y-r,x+r,y+r,fill="white",outline="purple")
		self.items.append(id)

		if agentDir == Up:
			x1, y1 = x, y+r
			x2, y2 = x, y-r
		elif agentDir == Down:
			x1, y1 = x, y-r
			x2, y2 = x, y+r
		elif agentDir == Left:
			x1, y1 = x+r, y
			x2, y2 = x-r, y
		elif agentDir == Right:
			x1, y1 = x-r, y
			x2, y2 = x+r, y

		id = self.canvas.create_line(x1,y1,x2,y2,fill="black",arrow=LAST,arrowshape=(11,13,7))
		self.items.append(id)
 
    def FindAdjacentRooms(self,i,j):
		possibles = [(i+1,j), (i,j-1), (i,j+1), (i-1,j)]
		return filter(self.InCave, possibles)

    def InCave(self,room):
		u,v = room
		if u < 1 or u > self.numRows or v < 1 or v > self.numCols:
			return false
		else:
			return true

class PerceptsFrame(Frame):
    def __init__(self,root=None):
		Frame.__init__(self,root)
		font=("Helvetica","14")
		self.breeze = Label(self, text="Breeze", relief=RAISED, font=font,width=5)
		self.scream = Label(self, text="Scream", relief=RAISED, font=font,width=5)
		self.bump = Label(self, text="Bump", relief=RAISED, font=font,width=5)
		self.smell = Label(self, text="Smell", relief=RAISED, font=font,width=5)
		self.glitter = Label(self, text="Glitter", relief=RAISED, font=font,width=5)

		self.breeze.pack(side=LEFT, expand=1, fill=X)
		self.scream.pack(side=LEFT, expand=1, fill=X)
		self.bump.pack(side=LEFT, expand=1, fill=X)
		self.smell.pack(side=LEFT, expand=1, fill=X)
		self.glitter.pack(side=LEFT, expand=1, fill=X)

class ActionsFrame(Frame):
    def __init__(self,root=None):
		Frame.__init__(self,root)
		font=("Helvetica","14")
		self.forward = Label(self, text="Forward", relief=RAISED, font=font, width=5)
		self.left = Label(self, text="Turn Left", relief=RAISED, font=font, width=5)
		self.right = Label(self, text="Turn Right", relief=RAISED, font=font, width=5)
		self.shoot = Label(self, text="Shoot", relief=RAISED, font=font, width=5)
		self.climb = Label(self, text="Climb", relief=RAISED, font=font, width=5)

		self.forward.pack(side=LEFT, expand=1, fill=X)
		self.left.pack(side=LEFT, expand=1, fill=X)
		self.right.pack(side=LEFT, expand=1, fill=X)
		self.shoot.pack(side=LEFT, expand=1, fill=X)
		self.climb.pack(side=LEFT, expand=1, fill=X)

class ControlPanel(Frame):
    def __init__(self,root,mainwin):
		Frame.__init__(self,root,bg="pink",relief=RIDGE)
		font = ("Helvetica","12")

			# Start, end and quit buttons
		self.start = Button(self, text="Start", font=font, command=mainwin.Start())
		self.pause = Button(self, text="Pause", font=font, command=mainwin.Pause()) 
		self.step = Button(self, text="Step", font=font, command=mainwin.Step())
		self.end = Button(self, text="End", font=font, command=mainwin.End())
		self.reset = Button(self, text="Reset", font=font, command=mainwin.Reset())
		self.quit = Button(self, text="Quit", font=font, command=mainwin.Quit)

		self.timeStep = Label(self, anchor=W, relief=GROOVE, padx=10, pady=10, font=font, text="TIME STEP: 0")
		self.numRows = Label(self,  anchor=W, relief=GROOVE, padx=10, pady=10, font=font, text="ROWS: 10")
		self.numCols = Label(self,  anchor=W, relief=GROOVE, padx=10, pady=10, font=font, text="COLS: 10")
		self.score = Label(self, anchor=W, relief=GROOVE, padx=10, pady=10, font=font, text="SCORE: 10,000")
		self.moves = Label(self, anchor=W, relief=GROOVE, padx=10, pady=10, font=font, text="MOVES: 0")

			# Empty label
		self.empty = Label(self,height=14, relief=GROOVE)

			# Pack, start end and quit
		self.start.pack(side=TOP, expand=1, fill=X)
		self.pause.pack(side=TOP, expand=1, fill=X)
		self.step.pack(side=TOP, expand=1, fill=X)
		self.reset.pack(side=TOP, expand=1, fill=X)
		self.end.pack(side=TOP, expand=1, fill=X)
		self.quit.pack(side=TOP, expand=1, fill=X)

		self.timeStep.pack(side=TOP, expand=1, fill=X)
		self.numRows.pack(side=TOP, expand=1, fill=X)
		self.numCols.pack(side=TOP, expand=1, fill=X)
		self.score.pack(side=TOP, expand=1, fill=X)
		self.moves.pack(side=TOP, expand=1, fill=X)

			# Pack extra area
		#self.empty.pack(side=BOTTOM, expand=1, fill=BOTH)

class SimWumpusWindow(Frame):

	def __init__(self, root=None):
		Frame.__init__(self, root, bg="slate gray")
		self.sim = SimWumpus()
		self.root = root
		self.root.tk_setPalette(background="dim gray", foreground="white smoke")
		self.master.title("SimWumpus")
		self.CreateWidgets()

	def CreateWidgets(self):
		agent = self.sim.AgentState()
		wumpus = self.sim.WumpusState()
		gold = self.sim.GoldState()
		pits = self.sim.PitLocations()

		caveState = (agent, wumpus, gold, pits)

		self.layout = Frame(self, bg="green")
		self.cave = CaveFrame(self.layout, caveState, 10,10,30)
		self.percepts = PerceptsFrame(self.layout)
		self.actions = ActionsFrame(self.layout)

		self.controls = ControlPanel(self, self)
		self.controls.pack(side=LEFT, expand=1, fill=X, padx=10, pady=10)

		self.cave.pack(side=TOP, expand=1, fill=BOTH)
		self.percepts.pack(side=BOTTOM, expand=1, fill=X)
		self.actions.pack(side=BOTTOM, expand=1, fill=X)
		self.layout.pack(side=RIGHT, expand=1, fill=BOTH)

	def UpdateDisplay(self):
		agent = self.sim.AgentState()
		wumpus = self.sim.WumpusState()
		gold = self.sim.GoldState()
		pits = self.sim.PitLocations()

		caveState = (agent,wumpus,gold,pits)

		self.cave.Update(caveState)
		#self.percepts.Update()
		#self.actions.Update()
		#self.controls.Update()

	def Start(self):
		pass

	def Pause(self):
		pass

	def Step(self):
		pass

	def Reset(self):
		self.sim.Reset()
		self.UpdateDisplay()

	def End(self):
		pass

	def Quit(self):
		self.sim.Quit()


def Main():
    root = Tk()
    simWumpusWin = SimWumpusWindow(root)
    simWumpusWin.pack(side=TOP, expand=1, fill=BOTH)
    root.mainloop()
    
if __name__ == '__main__':
    Main()
