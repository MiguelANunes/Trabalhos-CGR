import numpy
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
width, height = 1000, 768


def refresh2d():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw_circle(tx, ty, cx, cy, tipoGL):
    glBegin(tipoGL)

    raio = 10
    segmentos = 30

    for i in range(segmentos):
        angulo = (2*numpy.pi*i)/segmentos
        x = tx*raio*math.cos(angulo)
        y = ty*raio*math.sin(angulo)

        glVertex2f(cx+x+tx, cy+y+ty)
        

    glEnd() 

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    refresh2d()
    glColor3f(0.0, 0.0, 1.0)
    draw_circle( 5, 5, 100, 100, GL_POLYGON) #( tamanho x, tamanho y, coordenada x, coordenada y, tipo do objeto a ser desenhado)

    

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Trabalho Final de CGR")
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutMainLoop()

if __name__ == "__main__":
    main()
    
# https://stackoverflow.com/questions/22444450/drawing-circle-with-opengl
# https://noobtuts.com/python/opengl-introduction
# https://cyrille.rossant.net/2d-graphics-rendering-tutorial-with-pyopengl/
# http://pyopengl.sourceforge.net/documentation/index.html
# http://pyopengl.sourceforge.net/context/tutorials/index.html
