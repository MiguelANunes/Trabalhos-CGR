import Entities
import Logic
import Render
from random import randint

blu_team = [] # listas de ids de entidades nas equipes
red_team = []

def gameLoop():
    turn = 0

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
