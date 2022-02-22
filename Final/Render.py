from nis import match
from time import sleep
import numpy
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

import pygame                   #pip install pygame
from pygame.locals import *

import Logic
import Main
import Entities

width, height = 1000, 700


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

def draw_soldado(cx, cy, team, tipo):
    tamx = 0.5
    tamy = 0.5
    if (tipo == "rf"):
        if (team == "red"):
            glColor3f(1,0,0)
            draw_circle(tamx, tamy, cx, cy, GL_POLYGON)
        if (team == "blue"):
            glColor3f(0,0,1)
            draw_circle(tamx, tamy, cx, cy, GL_POLYGON)
        if (team == "none"):
            glColor3f(109/255, 110/255, 109/255)
            draw_circle(tamx, tamy, cx, cy, GL_POLYGON)
    elif (tipo == "mg"):
        if (team == "red"):
            glColor3f(1,0,0)
            draw_circle(tamx, tamy, cx, cy, GL_POLYGON)
            glColor3f(109/255, 110/255, 109/255)
            draw_cano(10, 3, cx+tamx/2-5/2, cy+tamy/2, -90, GL_POLYGON)
        if (team == "blue"):
            glColor3f(0,0,1)
            draw_circle(tamx, tamy, cx, cy, GL_POLYGON)
            glColor3f(109/255, 110/255, 109/255)
            draw_cano(10, 3, cx+tamx/2+5/2, cy+tamy/2, 90, GL_POLYGON)
        if (team == "none"):
            glColor3f(109/255, 110/255, 109/255)
            draw_circle(tamx, tamy, cx, cy, GL_POLYGON)




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

def draw_cano(t1, t2, cx, cy, rotacao, tipoGL):
    x1 = cx
    y1 = cy
    x2 = cx + t1
    y2 = cy
    x3 = cx + t1
    y3 = cy + t2
    x4 = cx
    y4 = cy + t2

    rotaciona(cx, cy, rotacao)    

    glBegin(tipoGL)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glVertex2f(x4, y4)
    glEnd() 

    desrotaciona(cx, cy, rotacao)

def draw_explosion(cx, cy, raio):
    tamanhoExplosao = 10
    raio = raio/10
    for i in range(tamanhoExplosao):        #esse loop deveria redesenhar o raio da eplosão a cada frame, mas n sei fazer isso aa
        draw_circle(raio*i, raio*i, cx, cy, GL_LINE_LOOP)
    glEnd() 

def draw_Text(x, y, text):     
    font = pygame.font.SysFont('arial', 20)                                           
    textSurface = font.render(text, True, (255, 255, 255, 255), (0, 66, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)   

def draw_tank(cx, cy, team):
    tamx = 40
    tamy = 60
    if (team == "red"):
        glColor3f(1,0,0)
        draw_rect(tamx, tamy, cx, cy, 0, GL_POLYGON)
        glColor3f(109/255, 110/255, 109/255)
        draw_cano(60, 10, cx+tamx/2-5, cy+tamy/2, -90, GL_POLYGON)
        draw_circle(1,1,cx+tamx/2-1, cy+tamy/2,GL_POLYGON)
    elif(team == "blue"):
        glColor3f(0,0,1)
        draw_rect(tamx, tamy, cx, cy, 0, GL_POLYGON)
        glColor3f(109/255, 110/255, 109/255)
        draw_cano(60, 10, cx+tamx/2+5, cy+tamy/2, 90, GL_POLYGON)
        draw_circle(1,1,cx+tamx/2-1, cy+tamy/2,GL_POLYGON)
    elif(team == "none"):
        glColor3f(109/255, 110/255, 109/255)
        draw_rect(tamx, tamy, cx, cy, 0, GL_POLYGON)
        glColor3f(109/255, 110/255, 109/255)
        draw_cano(60, 10, cx+tamx/2+5, cy+tamy/2, 90, GL_POLYGON)
        draw_circle(1,1,cx+tamx/2-1, cy+tamy/2,GL_POLYGON)

def draw(red_team, blu_team):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    refresh2d()

    pygame.font.init()
    glColor3f(26/255, 82/255, 33/255)
    draw_rect(700,700,0,0,0,GL_POLYGON)
    glColor3f(0.0, 0.0, 1.0)


    draw_Text(800, 780, "Pontuação: ")
    draw_Text(905, 780, "45")
    
    #ocupado = [(10,10),(20,20),(30,30),(40,40)]
    #Logic.occupied_spaces x,y -> olhar no game_map -> ver o id e testar se ta no time vermelho ou azul

    for i, x in enumerate(Logic.occupied_spaces):
        coordx = Logic.occupied_spaces[i][0]
        coordy = Logic.occupied_spaces[i][1]
        id = Logic.game_map[coordx][coordy]

        if (str(id).startswith("11")):
            if(id in red_team):
                draw_soldado(coordx*7,coordy*7,"red","rf")
            elif(id in blu_team):
                draw_soldado(coordx*7,coordy*7,"blue","rf")
            else:
                draw_soldado(coordx*7,coordy*7,"none","rf")
        elif (str(id).startswith("12")):
            if(id in red_team):
                draw_soldado(coordx*7,coordy*7,"red","mg")
            elif(id in blu_team):
                draw_soldado(coordx*7,coordy*7,"blue","mg")
            else:
                draw_soldado(coordx*7,coordy*7,"none","mg")
        elif (str(id).startswith("13")):
            if(id in red_team):
                draw_tank(coordx*7,coordy*7,"red")
            elif(id in blu_team):
                draw_tank(coordx*7,coordy*7,"blue")
            else:
                draw_tank(coordx*7,coordy*7,"none")
        elif (str(id).startswith("14")):
            if(id in red_team):
                draw_tank(coordx*7,coordy*7,"red")
            elif(id in blu_team):
                draw_tank(coordx*7,coordy*7,"blue")
            else:
                draw_tank(coordx*7,coordy*7,"none")
        elif (str(id).startswith("91")):
            draw_rect(8,8,coordx*7, coordy*7,0,GL_POLYGON)
        elif (str(id).startswith("92")):
            draw_rect(8,8,coordx*7, coordy*7,0,GL_POLYGON)



    glutSwapBuffers()

    '''
        if (id in Main.red_team):
            #glColor3f(1,0,0)
            if (str(id).startswith("13")):
                draw_tank(coordx*8,coordy*8,"red")
            else:
                draw_rect(5,5,coordx*8,coordy*8,0,GL_POLYGON)

        elif (id in Main.blu_team):
            glColor3f(0,0,1)
            if (str(id).startswith("13")):
                draw_tank(coordx*8,coordy*8,"blue")
            else: 
                draw_rect(5,5,coordx*8,coordy*8,0,GL_POLYGON)
        else:
            glColor3f(148/255, 148/255, 148/255)
            draw_rect(5,5,coordx*8,coordy*8,0,GL_POLYGON)
    '''



def main():
    Main.gameStart()
    #Main.gameLoop()
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
