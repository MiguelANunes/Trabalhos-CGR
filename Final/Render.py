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


'''
  4____t3_____3
  |           |
t4|           |t2
  |___________|  
  1    t1     2
'''


#If you want to rotate around P, translate by -P (so that P moves to the origin), then perform your rotation, then translate by P (so that the origin moves back to P).
def rotaciona(meiox, meioy, rotacao):
    glTranslatef(meiox, meioy, 0)
    glRotatef(rotacao, 0, 0, 1)
    glTranslatef(-meiox, -meioy, 0)

def desrotaciona(meiox, meioy, rotacao):
    glTranslatef(meiox, meioy, 0)
    glRotatef(-rotacao, 0, 0, 1)
    glTranslatef(-meiox, -meioy, 0)

def draw_rect(t1, t2, cx, cy, rotacao, tipoGL):
    x1 = cx
    y1 = cy
    x2 = cx + t1
    y2 = cy
    x3 = cx + t1
    y3 = cy + t2
    x4 = cx
    y4 = cy + t2
    meiox = cx + t1/2
    meioy = cy + t2/2

    rotaciona(meiox, meioy, rotacao)    

    glBegin(tipoGL)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glVertex2f(x4, y4)
    glEnd() 

    desrotaciona(meiox, meioy, rotacao)

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    refresh2d()
    glColor3f(0.0, 0.0, 1.0)
    draw_circle( 5, 5, 100, 100, GL_POLYGON) # (tamanho x, tamanho y, coordenada x, coordenada y, tipo do objeto a ser desenhado)
    draw_rect( 80, 100, 300, 300, 0, GL_QUADS)
    draw_rect( 80, 100, 300, 300, 30, GL_QUADS) # (tamanho x, tamanho y, rotação, coordenada x, coordenada y, tipo do objeto)
    draw_rect( 80, 100, 500, 300, 0, GL_QUADS)

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
