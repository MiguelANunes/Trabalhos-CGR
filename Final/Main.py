import Entities
import Logic
import Render
from random import randint
from collections import deque

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

width, height = 1050, 700

blu_team = []
red_team = []
blu_points = 0
red_points = 0

def getBluTeam():
    return blu_team
def getRedTeam():
    return red_team

def changeBluTeam(new_blu):
    blu_team = new_blu

def changeRedTeam(new_red):
    red_team = new_red

def gameLoop():
    turn = 0

    while(True):
        Logic.takeTurn(blu_team)
        Logic.takeTurn(red_team)
        for id, path in Logic.move_buffer.items(): # para cada movimento no buffer de movimentos
            # Render.render(game_map) # renderiza o mapa
            # recupera o movimento e a entidade que fará ele
            # input("Passou do loop move_buffer")
            entity = Logic.entity_list[id]
            while entity.action_points > 0 and len(path) > 0:
                # input("Passou do loop action_points")
                entity.action_points -= 1
                # se a entidade tiver pontos de ação suficientes
                old_pos = entity.position
                new_pos = path.popleft()
                entity.updatePosition(new_pos)                

                Logic.occupied_spaces.remove(old_pos)
                Logic.occupied_spaces.append(new_pos)

                Logic.game_map[old_pos[0]][old_pos[1]] = None
                Logic.game_map[new_pos[0]][new_pos[1]] = id

                # Render.render(game_map) # renderiza o mapa
                
                Render.draw(red_team, blu_team, red_points, blu_points)

        for id, path in Logic.projectile_buffer.items():
            proj = Logic.projectile_list[id]
            current_pos = proj.position
            if len(path) == 0:
                continue
            next_pos = path.popleft() # proxima posição do projétil

            # Render.render_proj(proj, next_pos)
            if Logic.entity_list[proj.parent_id].position != current_pos:
                if current_pos in Logic.occupied_spaces and Logic.game_map[current_pos[0]][current_pos[1]] != None:
                    # print(current_pos)
                    # print(Logic.occupied_spaces)
                    # # print(Logic.game_map[current_pos[0]][current_pos[1]])
                    # print(Logic.game_map[current_pos[0]][current_pos[1]])
                    # input()
                    ret = Logic.projectileCollision(proj, current_pos, blu_team, red_team)
                    if ret[0] == "b":
                        changeBluTeam(ret[1])
                    else:
                        changeRedTeam(ret[1])
                    # Render.render(game_map) # renderiza o mapa
                    del proj
                    continue

            proj.position = new_pos
            proj.ttl -= randint(1,5)
            if proj.ttl <= 0:
                proj.zeroTTL()

        turn += 1
        # se uma das equipes perdeu todas as entidades, jogo termina
        if len(blu_team) == 0:
            return (0, blu_points)
        if len(red_team) == 0:
            return (1, red_points)

        for _, entity in Logic.entity_list.items():
            entity.resetActionPoints()
        
    #Render.draw()
    #input()

def gameStart():

    # equipe azul começa na parte de baixo do mapa, vermelha no topo do mapa
    lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y = 5, Logic.map_size-1, 1, 10
    Logic.populateTeams(blu_team, lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)

    lower_limit_y, upper_limit_y = Logic.map_size-10, Logic.map_size-1
    Logic.populateTeams(red_team, lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)

    lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y = 10, Logic.map_size-10, 30, 60
    total_elements = randint(20,30)
    for _ in range(total_elements):
        Entities.generateRandomTerrain(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)
    
    Logic.loadMap()

def main():
    gameStart()
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Trabalho Final de CGR")
    glutDisplayFunc(Render.draw)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40, 1, 1, 40)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, 0, 10,
              0, 0, 0,
              0, 1, 0)
    glPushMatrix()
    glutIdleFunc(Render.draw)
    #glutMainLoop()

    #print(getBluTeam())
    #print(getRedTeam())
    #print("socorro")

    result = gameLoop()
    if result[0] == 0: # Renderizar esse texto na tela
        print("Red Wins !")
    else:
        print("Blu Wins !")

if __name__ == "__main__":
    main()
