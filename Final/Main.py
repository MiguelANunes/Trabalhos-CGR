import Entities
import Logic
import Render
from random import randint
from collections import deque

blu_team = [] # listas de ids de entidades nas equipes
red_team = []

def gameLoop():
    turn = 0

    while(True):
        Logic.takeTurn(blu_team)
        Logic.takeTurn(red_team)
        
        for id, path in Logic.move_buffer: # para cada movimento no buffer de movimentos
            # Render.render(game_map) # renderiza o mapa
            # recupera o movimento e a entidade que fará ele
            while Logic.entity_list[id].action_points > 0 and len(path) > 0:
                Logic.entity_list[id].action_points -= 1
                # se a entidade tiver pontos de ação suficientes
                old_pos = Logic.entity_list[id].position
                new_pos = path.popleft()
                
                Logic.occupied_spaces.remove(old_pos)
                Logic.occupied_spaces.append(new_pos)

                Logic.game_map[old_pos[0]][old_pos[1]] = None
                Logic.game_map[new_pos[0]][new_pos[1]] = id

                # Render.render(game_map) # renderiza o mapa

        for proj, path in Logic.projectile_buffer:
            current_pos = proj.position
            next_pos = path.popleft() # ultima posição do projétil

            if current_pos in Logic.occupied_spaces:
                Logic.projectileCollision(proj, current_pos)
                del proj

            # Render.render_proj(proj, next_pos)

            proj.position = new_pos
            proj.ttl -= randint(1,5)
            if proj.ttl <= 0:
                proj.zeroTTL()

        turn += 1
        # se uma das equipes perdeu todas as entidades, jogo termina
        if len(blu_team) == 0:
            return 0
        if len(red_team) == 0:
            return 1

def gameStart():

    # equipe azul começa na parte de baixo do mapa, vermelha no topo do mapa
    lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y = 0, Logic.map_size-1, 0, 10
    Logic.populateTeams(blu_team, lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)

    lower_limit_y, upper_limit_y = Logic.map_size-10, Logic.map_size-1
    Logic.populateTeams(red_team, lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)

    lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y = 15, Logic.map_size-15, 30, 60
    total_elements = randint(20,30)
    for _ in range(total_elements):
        Entities.generateRandomTerrain(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)
    
    Logic.loadMap()


def main():
    gameStart()

if __name__ == "__main__":
    main()
