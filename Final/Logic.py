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

def takeTurn(team):

    for entity_id in team: # iterando pelas ids de entidades na lista da equipe
        entity = entity_list[entity_id]
        if entity.current_state == 0:
            stateCalm(entity)

        elif entity.current_state == 1:
            stateAlert(entity)

        else:
            stateCombat(entity)

def stateCalm(entity):
    pass
    # calcular as ações a serem feitas
    # colocar a lista de ações numa fila
    # colocar num dict {id_entidade: lista_ações}
    # quando mudar de estado, apaga a entrada daquele id no dict

def stateAlert(entity):
    pass

def stateCombat(entity):
    pass

def changeState(entity, new_state):
    pass

def actionMove():
    pass

def actionWait():
    pass

def actionAttack():
    pass

def actionReload():
    pass

def actionBroadcast():
    pass