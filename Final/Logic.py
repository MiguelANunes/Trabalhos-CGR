import Entities
from random import randint

entity_list = {} # mantendo uma lista de todas as entidades atualmente existentes
projectile_list = {}
terrain_list = {}

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

def generateRandomTerrain(pos_x, pos_y): # gera um objeto de terreno que é colocado no cenário
    x = randint(1,3)
    obj = Entities.Terrain(pos_x, pos_y, (x, x))
    terrain_list[obj.id] = obj