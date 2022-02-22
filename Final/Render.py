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

width, height = 1050, 700

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
            glColor3f(0,0,0)
            draw_circle(tamx, tamy, cx, cy, GL_LINE_LOOP)
            draw_circle(tamx-0.09, tamy-0.09, cx, cy, GL_LINE_LOOP)
        if (team == "blue"):
            glColor3f(0,0,1)
            draw_circle(tamx, tamy, cx, cy, GL_POLYGON)
            glColor3f(0,0,0)
            draw_circle(tamx, tamy, cx, cy, GL_LINE_LOOP)
            draw_circle(tamx-0.09, tamy-0.09, cx, cy, GL_LINE_LOOP)
        if (team == "none"):
            glColor3f(109/255, 110/255, 109/255)
            draw_circle(tamx, tamy, cx, cy, GL_POLYGON)
            glColor3f(0,0,0)
    elif (tipo == "mg"):
        if (team == "red"):
            glColor3f(1,0,0)
            draw_circle(tamx, tamy, cx, cy, GL_POLYGON)
            glColor3f(0,0,0)
            draw_circle(tamx, tamy, cx, cy, GL_LINE_LOOP)
            draw_circle(tamx-0.09, tamy-0.09, cx, cy, GL_LINE_LOOP)
            glColor3f(109/255, 110/255, 109/255)
            draw_cano(10, 3, cx+tamx/2-3/2, cy+tamy/2, -90, GL_POLYGON)
        if (team == "blue"):
            glColor3f(0,0,1)
            draw_circle(tamx, tamy, cx, cy, GL_POLYGON)
            glColor3f(0,0,0)
            draw_circle(tamx, tamy, cx, cy, GL_LINE_LOOP)
            draw_circle(tamx-0.09, tamy-0.09, cx, cy, GL_LINE_LOOP)
            glColor3f(109/255, 110/255, 109/255)
            draw_cano(10, 3, cx+tamx/2+3/2, cy+tamy/2, 90, GL_POLYGON)
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

def draw_tank(cx, cy, team, tipo):
    tamx = 20
    tamy = 30
    if (team == "red"):
        glColor3f(1,0,0)
        draw_rect(tamx, tamy, cx, cy, 0, GL_POLYGON)
        glColor3f(0,0,0)
        draw_rect(tamx, tamy, cx, cy, 0, GL_LINE_LOOP)
        draw_rect(tamx-0.09, tamy-0.09, cx, cy, 0, GL_LINE_LOOP)
        glColor3f(109/255, 110/255, 109/255)
        draw_cano(30, 5, cx+tamx/2-5/2, cy+tamy/2, -90, GL_POLYGON)
        if(tipo == "mt"):
            draw_circle(0.75,0.75,cx+tamx/2-1, cy+tamy/2,GL_POLYGON)
        elif(tipo == "at"):  
            draw_rect(15,15,cx+tamx/2-15/2, cy+tamy/2-15/2,0,GL_POLYGON)
    elif(team == "blue"):
        glColor3f(0,0,1)
        draw_rect(tamx, tamy, cx, cy, 0, GL_POLYGON)
        glColor3f(0,0,0)
        draw_rect(tamx, tamy, cx, cy, 0, GL_LINE_LOOP)
        draw_rect(tamx-0.09, tamy-0.09, cx, cy, 0, GL_LINE_LOOP)
        glColor3f(109/255, 110/255, 109/255)
        draw_cano(30, 5, cx+tamx/2+5/2, cy+tamy/2, 90, GL_POLYGON)
        if(tipo == "mt"):
            draw_circle(0.75,0.75,cx+tamx/2-1, cy+tamy/2,GL_POLYGON)
        elif(tipo == "at"):
            glColor3f(109/255, 110/255, 109/255)
            draw_rect(15,15,cx+tamx/2-15/2, cy+tamy/2-15/2,0,GL_POLYGON)
    elif(team == "none"):
        glColor3f(109/255, 110/255, 109/255)
        draw_rect(tamx, tamy, cx, cy, 0, GL_POLYGON)
        glColor3f(109/255, 110/255, 109/255)
        draw_cano(60, 10, cx+tamx/2+5, cy+tamy/2, 90, GL_POLYGON)
        if(tipo == "mt"):
            draw_circle(1,1,cx+tamx/2-1, cy+tamy/2,GL_POLYGON)
        elif(tipo == "at"):
            glColor3f(109/255, 110/255, 109/255)
            draw_rect(10,10,cx+tamx/2, cy+tamy/2,0,GL_POLYGON)

def draw(red_team, blu_team, red_points, blu_points):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    refresh2d()

    pygame.font.init()
    glColor3f(26/255, 82/255, 33/255)
    draw_rect(height,height,0,0,0,GL_POLYGON)
    glColor3f(0.0, 0.0, 1.0)

    #draw_tank(100,100,"blue")
    #draw_tank(800,600,"red")

    #draw_Text(800, 780, "Pontuação: ")
    #draw_Text(905, 780, "45")
    draw_Text(height, height-20, "Quantidade de tropas time vermelho:")
    draw_Text(height, 80, "Quantidade de tropas time azul:")
    #rifleman, machinegunner, mediumtank, artillerytank
    qtdred = [0,0,0,0]
    qtdblu = [0,0,0,0]    
    
    #ocupado = [(10,10),(20,20),(30,30),(40,40)]
    #Logic.occupied_spaces x,y -> olhar no game_map -> ver o id e testar se ta no time vermelho ou azul

    for i, x in enumerate(Logic.occupied_spaces):
        #print(x)
        coordx = Logic.occupied_spaces[i][0]
        coordy = Logic.occupied_spaces[i][1]
        id = Logic.game_map[coordx][coordy]
        #print ("vermelho: ", red_points)
        #print ("azul: ", blu_points)
        #print(Main.getBluTeam())
        #print(Main.getRedTeam())
        #print (id, id in Main.red_team)
        #print (id, id in Main.blu_team)
        if (str(id).startswith("11")):
            #print(id in Main.red_team)
            if(id in red_team):
                draw_soldado(coordx*(height/100),coordy*(height/100),"red","rf")
                qtdred[0] += 1
            elif(id in blu_team):
                draw_soldado(coordx*(height/100),coordy*(height/100),"blue","rf")
                qtdblu[0] += 1
            else:
                draw_soldado(coordx*(height/100),coordy*(height/100),"none","rf")
        elif (str(id).startswith("12")):
            if(id in red_team):
                draw_soldado(coordx*(height/100),coordy*(height/100),"red","mg")
                qtdred[1] += 1
            elif(id in blu_team):
                draw_soldado(coordx*(height/100),coordy*(height/100),"blue","mg")
                qtdblu[1] += 1
            else:
                draw_soldado(coordx*(height/100),coordy*(height/100),"none","mg")
        elif (str(id).startswith("13")):
            if(id in red_team):
                draw_tank(coordx*(height/100),coordy*(height/100),"red", "mt")
                qtdred[2] += 1
            elif(id in blu_team):
                draw_tank(coordx*(height/100),coordy*(height/100),"blue", "mt")
                qtdblu[2] += 1
            else:
                draw_tank(coordx*(height/100),coordy*(height/100),"none", "mt")
        elif (str(id).startswith("14")):
            if(id in red_team):
                draw_tank(coordx*(height/100),coordy*(height/100),"red", "at")
                qtdred[3] += 1
            elif(id in blu_team):
                draw_tank(coordx*(height/100),coordy*(height/100),"blue", "at")
                qtdblu[3] += 1
            else:
                draw_tank(coordx*(height/100),coordy*(height/100),"none", "at")
        elif (str(id).startswith("91")):
            draw_rect(8,8,coordx*(height/100), coordy*(height/100),0,GL_POLYGON)
        elif (str(id).startswith("92")):
            draw_rect(8,8,coordx*(height/100), coordy*(height/100),0,GL_POLYGON)

    #print("red: ", qtdred)
    #print("blu: ", qtdblu)

    draw_Text(height,height-(20*2), "Rifleman: ")
    draw_Text(height+200,height-(20*2), str(qtdred[0]))
    draw_Text(height,height-(20*3), "Machinegunner: ")
    draw_Text(height+200,height-(20*3), str(qtdred[1]))
    draw_Text(height,height-(20*4), "MediumTank: ")
    draw_Text(height+200,height-(20*4), str(qtdred[2]))
    draw_Text(height,height-(20*5), "ArtilleryTank: ")
    draw_Text(height+200,height-(20*5), str(qtdred[3]))

    draw_Text(height,60, "Rifleman: ")
    draw_Text(height+200,60, str(qtdblu[0]))
    draw_Text(height,40, "Machinegunner: ")
    draw_Text(height+200,40, str(qtdblu[1]))
    draw_Text(height,20, "MediumTank: ")
    draw_Text(height+200,20, str(qtdblu[2]))
    draw_Text(height,0, "ArtilleryTank: ")
    draw_Text(height+200,0, str(qtdblu[3]))

    glutSwapBuffers()



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
