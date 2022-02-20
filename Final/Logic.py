import Entities
from random import randint
from collections import deque

entity_list = {} # mantendo uma lista de todas as entidades atualmente existentes
terrain_list = {}
projectile_list = {}
action_buffer = {} # ações a serem tomadas serão guardadas nessa lista
occupied_spaces = [] # lista de tuplas (x,y) de pontos no mapa que já estão ocupados
used_ids = [] # lista de todos os ids que já estão associados a alguma coisa

map_size = 100
game_map = [[None for i in range(map_size)] for i in range(map_size)]

def createExplosion(position, radius, damage):
    # marca as celulas ao redor de position[0],position[1] com uma explosão
    # explosões dão damage pontos de dano em todas as unidades nas celulas marcadas com explosão
    # repete isso radius vezes, sendo que após cada iteração, celulas marcadas com explosão anteriormente são desmarcadas
    # e novas celulas são marcadas

    # Explosões são bloqueadas por objetos do terreno

    """
    Primeiro momento:
    X X X X X
    X X X X X
    X X E X X
    X X X X X
    X X X X X

    Depois de uma iterção:
    X X X X X
    X E E E X
    X E X E X
    X E E E X
    X X X X X

    Depois de duas:
    E E E E E
    E X X X E
    E X X X E
    E X X X E
    E E E E E

    Assim por diante
    
    Com um objeto do terreno:

        Primeiro momento:
        X X X X X
        X T T T X
        X X E X X
        X X X X X
        X X X X X

        Depois de uma iterção:
        X X X X X
        X T T T X
        X E X E X
        X E E E X
        X X X X X

        Depois de duas:
        X X X X X
        E T T T E
        E X X X E
        E X X X E
        E E E E E
    """
    pass

def loadMap(): # carrega todos os componentes do jogo no mapa
    for chave, item in entity_list.items():
        game_map[item.position[0]][item.position[1]] = chave
    for chave, item in terrain_list.items():
        game_map[item.position[0]][item.position[1]] = chave
    for chave, item in projectile_list.items():
        game_map[item.position[0]][item.position[1]] = chave

def populateTeams(team, lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y):
    for _ in range(30):
        team.append(Entities.createRifleman(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y))
    for _ in range(10):
        team.append(Entities.createMachineGunner(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y))
    for _ in range(4):
        team.append(Entities.createTank(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y))

    team.append(Entities.createArtilleryTank(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y))

def gameStart():
    blu_team = [] # listas de ids de entidades nas equipes
    red_team = []

    # equipe azul começa na parte de baixo do mapa, vermelha no topo do mapa
    lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y = 0, map_size, 0, 10
    populateTeams(blu_team, lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)

    lower_limit_y, upper_limit_y = map_size-10, map_size
    populateTeams(red_team, lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)

    lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y = 15, map_size-15, 30, 60
    total_elements = randint(20,30)
    for _ in range(total_elements):
        Entities.generateRandomTerrain(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)
    
    loadMap()


    