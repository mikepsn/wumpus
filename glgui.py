from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from boolean import *
from agent import *
from simwumpus import SimWumpus
import sys

sim = SimWumpus()
step = False

ESCAPE = '\033'

window = 0
winWidth = 800
winHeight = 600

white =  (1.0, 1.0, 1.0)
grey =   (0.5, 0.5, 0.5)
blue =   (0.2, 0.2, 1.0)
red =    (1.0, 0.0, 0.0)
orange = (1.0, 0.5, 0.0)
yellow = (1.0, 1.0, 0.0)
green =  (0.0, 1.0, 0.0)

arrow = [ (0,0), (1,-1), (0,1), (-1,-1) ]

rot = 0
scale = 1

path = [ (1,1), (1,2), (1,3), (1,4), (1,5), (1,6) ]
pos = 0

SimGetNumCols = 10
SimGetNumRows = 10

def ResizeScene(w,h):
    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w)/float(h), 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def Mouse(button, button_state, x, y):
    global step
    if button == GLUT_LEFT_BUTTON:
        step = True
    glutPostRedisplay()
        

def KeyPressed(key,x,y):
    if key == ESCAPE:
        sys.exit()

def InitGL(width,height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(45.0, float(width)/float(height), 0.1, 100)

    glMatrixMode(GL_MODELVIEW)

    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))		
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))		
    glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 2.0, 1.0))	
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)

def DrawScene():
    global step, rot, pos

    numRows, numCols = sim.CaveSize()
    pits = sim.PitLocations()
    wumpus = sim.WumpusState()
    gold = sim.GoldState()
    agent = sim.AgentState()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 800, 0.0, 600)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPushMatrix()
    glScalef(40.0, 40.0, 0.0)
    glTranslatef(0.5,12.5,0)
    glRotatef(-90, 0, 0, 1)
    DrawGrid(numRows, numCols)
    DrawPits(pits)
    DrawWumpus(wumpus)
    DrawGold(gold)
    DrawAgent(agent)
    glPopMatrix()
    DrawTitle()
    DrawAgentInteractions(["GLITTER"],[])

    if step == True:
        sim.Step()
        step = False

    rot = rot + 1 
    if rot == 360:
        rot = 0 

    if rot % 10 == 0:
        pos = pos + 1

    if pos >= len(path):
        pos = 0

    glutPostRedisplay()
    glutSwapBuffers()


def DrawStrokeString(x,y,s,text):
    glPushMatrix()
    glTranslatef(x,y,0)
    glScalef(s,s,s)
    glRasterPos2i(x,y)
    for i in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(i))
    glPopMatrix()

def DrawBitmapString(x,y,text):
    glPushMatrix()
    glRasterPos2f(x,y)
    for i in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(i))
    glPopMatrix()

def DrawTitle():
    numRows, numCols = sim.CaveSize()
    agentPos, agentDir, agentType = sim.AgentState()
    wumpusPos, wumpusAlive = sim.WumpusState()
    goldPos = sim.GoldState()

    wumpusStatus = wumpusAlive and "Alive" or "Dead"

    glColor3fv(white)
    DrawStrokeString(10,570, 0.2, "SimWumpus (%s)" % agentType)
    DrawStrokeString(10,550, 0.1, "SCORE: 10,000")
    DrawStrokeString(10,530, 0.1, "MOVES: 34")
    DrawBitmapString(180,550,"AGENT: @ (%d,%d)" % agentPos)
    DrawBitmapString(180,530,"GOLD: @ (%d,%d)" % goldPos)
    DrawBitmapString(400,550,"ROOMS: %d" % (numRows * numCols))
    DrawBitmapString(400,530,"PERCENT EXPLORED: 4%")
    DrawBitmapString(10,510, "WUMPUS: %s" % wumpusStatus)
    DrawBitmapString(180,510,"MARKED/VISITED: 2%")
    DrawBitmapString(400,510,"MARKED/TOTAL: 1%")

def DrawAgentInteractions(percepts,actions):
    x = 500
    y = 420
    DrawButton(percepts, white, x,y,     "PERCEPTS")
    DrawButton(percepts, grey,  x,y-25,  "BUMP")
    DrawButton(percepts, grey,  x,y-50,  "BREEZE") 
    DrawButton(percepts, grey,  x,y-75,  "STENCH")
    DrawButton(percepts, grey,  x,y-100, "GLITTER")
    DrawButton(percepts, grey,  x,y-125, "SCREAM")

    x = 660
    y = 420
    DrawButton(actions, white, x,y,     "AFFORDANCES")
    DrawButton(actions, grey,  x,y-25,  "FORWARD")
    DrawButton(actions, grey,  x,y-50,  "TURN LEFT") 
    DrawButton(actions, grey,  x,y-75,  "TURN RIGHT")
    DrawButton(actions, grey,  x,y-100, "SHOOT")
    DrawButton(actions, grey,  x,y-125, "CLIMB")

    x = 500
    y = 240
    DrawButton(actions, white, x,y,     "ACTIONS")
    DrawButton(actions, grey,  x,y-25,  "FORWARD")
    DrawButton(actions, grey,  x,y-50,  "TURN LEFT") 
    DrawButton(actions, grey,  x,y-75,  "TURN RIGHT")
    DrawButton(actions, grey,  x,y-100, "SHOOT")
    DrawButton(actions, grey,  x,y-125, "CLIMB")

    

def DrawButton(inputs, color, x, y, text):
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    if text in inputs:
        glColor3fv(red)
    else:
        glColor3fv(color)
    DrawBitmapString(x+10,y+6,text)

    glPushMatrix()
    glBegin(GL_QUADS)
    glVertex2f(x,y)
    glVertex2f(x+120,y)
    glVertex2f(x+120,y+20)
    glVertex2f(x,y+20)
    glVertex2f(x,y)
    glEnd()
    glPopMatrix()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def DrawGrid(rows, cols):
    glColor3fv(grey)
    gWidth = cols + 1
    gHeight = rows + 1

    for row in range(1, gHeight+1):
        x1, y1 = (row*scale, scale)
        x2, y2 = (row*scale, gWidth*scale)
        glBegin(GL_LINES)
        glVertex2f(x1,y1)
        glVertex2f(x2,y2)
        glEnd()

        if row < gHeight:
            DrawBitmapString(x1+scale/2.0, y1-scale/2.0, "%d" % (row))

    for col in range(1,gWidth+1):
        x3, y3 = (scale, col*scale)
        x4, y4 = (gHeight*scale, col*scale)
        glBegin(GL_LINES)
        glVertex2f(x3,y3)
        glVertex2f(x4,y4)
        glEnd()

        if col < gWidth:
            DrawBitmapString(x3-scale/2.0, y3+scale/2.0, "%d" % (col))

def DrawRectangle(x,y,r,color):
    glPushMatrix()
    glColor3fv(color)
    glBegin(GL_QUADS)
    glVertex2f(x-r, y+r)
    glVertex2f(x+r, y+r)
    glVertex2f(x+r, y-r)
    glVertex2f(x-r, y-r)
    glEnd()
    glPopMatrix()

def DrawPits(pits):
    r = scale/2.0

	# Draw darkened pits
    for pit in pits:
        x,y = pit
        adjacentRooms = FindAdjacentRooms(x,y)
        x = (x*scale) + scale/2.0
        y = (y*scale) + scale/2.0
        DrawRectangle(x,y,r,grey)

        # Draw breezy rooms
    for breezyRoom in adjacentRooms:
        if breezyRoom not in pits:
            r = scale/6.0
            u,v = breezyRoom
            u = (u*scale) + scale/2.0
            v = (v*scale) + scale/2.0
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            DrawRectangle(u,v,r,blue)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
    r = scale/5.0

def DrawWumpus(wumpus):
    r = scale/4.0
    wumpusPos, wumpusAlive = wumpus
    x,y = wumpusPos
    adjacentRooms = FindAdjacentRooms(x,y)
    x = (x*scale) + scale/2.0
    y = (y*scale) + scale/2.0
    DrawRectangle(x,y,r,red)

    # Draw smelly rooms
    for smellyRoom in adjacentRooms:
        u,v = smellyRoom
        u = (u*scale) + scale/2.0
        v = (v*scale) + scale/2.0
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        DrawRectangle(u,v,r,orange)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def DrawGold(gold):
    r = scale/5.0
    x,y = gold
    x = (x*scale) + scale/2.0
    y = (y*scale) + scale/2.0
    #DrawRectangle(x,y,r,yellow)
    glPushMatrix()
    glTranslatef(x,y,0)
    glScalef(0.3,0.3,0.3)
    glRotatef(rot,1,0,0)
    glColor3fv(yellow)
    #glutWireIcosahedron()
    glPushMatrix()
    glRotatef(90,0,0,1)
    glutSolidTeapot(1)
    glPopMatrix()
    glPopMatrix()

def DrawAgent(agent):
    agentPos, agentDir, agentType = agent
    r = scale/5.0
    x,y = agentPos 
    x = (x*scale) + scale/2.0
    y = (y*scale) + scale/2.0

    angle = 0
    if agentDir == Up:
        angle = -90
    elif agentDir == Left:
        angle = -180
    elif agentDir == Down:
        angle = 90
    elif agentDir == Right:
        angle = 0

    DrawArrow(x,y,r*2,angle,green)

def DrawArrow(x,y,s,angle,color):
    glPushMatrix()
    glTranslatef(x,y,0)
    glScalef(s,s,s)
    glRotatef(angle,0.0, 0.0, 1.0)
    glColor3fv(color)
    glBegin(GL_POLYGON)
    for point in arrow:
        x, y = point
	glVertex2f(x,y)
    glEnd()
    glPopMatrix()
    
def FindAdjacentRooms(i,j):
    possibles = [(i+1,j), (i,j-1), (i,j+1), (i-1,j)]
    return filter(InCave, possibles)

def InCave(room):
    numRows = SimGetNumRows
    numCols = SimGetNumCols
    u,v = room
    if u < 1 or u > numRows or v < 1 or v > numCols:
        return false
    else:
        return true

def Main():
    global window, width, height, step
    step = False
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowPosition(0,0)
    glutInitWindowSize(winWidth, winHeight)
    window = glutCreateWindow(b"SimWumpus")
    glutDisplayFunc(DrawScene)
    glutIdleFunc(DrawScene)
    glutReshapeFunc(ResizeScene)
    glutKeyboardFunc(KeyPressed)
    glutMouseFunc(Mouse)
    InitGL(winWidth, winHeight)
    glutMainLoop()
    

if __name__ == '__main__':
    Main()
