from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

ESCAPE = '\033'

window = 0
winWidth = 800
winHeight = 600

zrot = 0

def ResizeScene(w,h):
    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(w)/float(h), 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

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
    
    gluPerspective(60.0, float(width)/float(height), 0.1, 100)

    glMatrixMode(GL_MODELVIEW)

    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))		
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))		
    glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 2.0, 1.0))	
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)

def DrawScene():
    global zrot
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)

    glRotatef(zrot, 0.0, 1.0, 0.0)
    glColor3f(float(zrot)/float(360), 0.5, float(360)/float(zrot+1))
    glutWireCube(3)
    glEnable(GL_LIGHTING)
    glutSolidTeapot(1)
    zrot = zrot + 0.01
    if zrot > 360.0:
        zrot = 0.0

    glutSwapBuffers()

def Main():
    global window, width, height
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(0,0)
    window = glutCreateWindow("PyOpenGL Template")
    glutDisplayFunc(DrawScene)
    glutIdleFunc(DrawScene)
    glutReshapeFunc(ResizeScene)
    glutKeyboardFunc(KeyPressed)
    InitGL(winWidth, winHeight)
    glutMainLoop()
    

if __name__ == '__main__':
    Main()
