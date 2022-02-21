import Entities
from random import randint
from collections import deque

entity_list = {} # mantendo uma lista de todas as entidades atualmente existentes
terrain_list = {}
projectile_list = {}
move_buffer = {} # movimentos a serem tomados serão guardadas nessa lista
projectile_buffer = {} # projéteis que devem se mover num turno
occupied_spaces = [] # lista de tuplas (x,y) de pontos no mapa que já estão ocupados

map_size = 100
game_map = [[None for i in range(map_size)] for i in range(map_size)]

def findOnGameMap(orig, depth, obj_type, team=None, is_own_team=False):
    # BFS para achar algo no mapa
    # obj_type é o caractere primeiro caractere da id do que está sendo procurado
    # depth é a profundidade da busca == o quão longe a entidade consegue ver
    # recebe a lista da própria equipe, para caso está procurando por inimigos, não retornar
    # que uma entidade da mesma equipe é um inimigo
    game_map = game_map

    orig_x, orig_y = orig
    x, y = 0, 0

    visitados = [[False for i in range(map_size)] for i in range(map_size)]
    visitados[orig_x][orig_y] = True
    traverse_queue = deque()
    traverse_queue.append(orig)

    dir_x = [1, -1, 0, 0, 1, 1, -1, -1]
    dir_y = [0, 0, 1, -1, 1, -1, 1, -1]
    visitados[orig_x][orig_y] = True

    while len(traverse_queue) > 0 and depth > 0:
        head = traverse_queue.popleft()

        for i in range(8):
            x = dir_x[i] + head[0] 
            y = dir_y[i] + head[1]

            outside_borders = x <= 0 or y <= 0 or x >= map_size or y >= map_size
            if outside_borders:
                continue
            
            if visitados[x][y]: # pode causar erro de Array out of Bounds se isso ficar no if acima
                continue

            if game_map[x][y] != None and game_map[x][y].startswith(obj_type):
                if team != None and not is_own_team: # se estou procurando algo da outra equipe
                    if not game_map[x][y] in team:
                        return (x,y)
                elif team != None and not is_own_team:
                    if game_map[x][y] in team:
                        return (x,y)
                else:
                    return (x,y)
            
            if not visitados[x][y]:
                visitados[x][y] = True
                traverse_queue.append((x,y))
            
        depth -= 1
    
    return None

def findAllOnGameMap(orig, depth, obj_type, team=None, is_own_team=False):
    # BFS para achar algo no mapa
    # obj_type é o caractere primeiro caractere da id do que está sendo procurado
    # depth é a profundidade da busca == o quão longe a entidade consegue ver
    # recebe a lista da própria equipe, para caso está procurando por inimigos, não retornar
    # que uma entidade da mesma equipe é um inimigo
    game_map = game_map

    orig_x, orig_y = orig
    x, y = 0, 0

    visitados = [[False for i in range(map_size)] for i in range(map_size)]
    visitados[orig_x][orig_y] = True
    traverse_queue = deque()
    traverse_queue.append(orig)

    dir_x = [1, -1, 0, 0, 1, 1, -1, -1]
    dir_y = [0, 0, 1, -1, 1, -1, 1, -1]
    visitados[orig_x][orig_y] = True

    while len(traverse_queue) > 0 and depth > 0:
        head = traverse_queue.popleft()

        for i in range(8):
            x = dir_x[i] + head[0] 
            y = dir_y[i] + head[1]

            outside_borders = x <= 0 or y <= 0 or x >= map_size or y >= map_size
            if outside_borders:
                continue
            
            if visitados[x][y]: # pode causar erro de Array out of Bounds se isso ficar no if acima
                continue

            if game_map[x][y] != None and game_map[x][y].startswith(obj_type):
                if team != None and not is_own_team: # se estou procurando algo da outra equipe
                    if not game_map[x][y] in team:
                        yield (x,y)
                elif team != None and not is_own_team:
                    if game_map[x][y] in team:
                        yield (x,y)
                else:
                    yield (x,y)
            
            if not visitados[x][y]:
                visitados[x][y] = True
                traverse_queue.append((x,y))
            
        depth -= 1

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
        occupied_spaces.append((item.position[0], item.position[1]))
    for chave, item in terrain_list.items():
        game_map[item.position[0]][item.position[1]] = chave
        occupied_spaces.append((item.position[0], item.position[1]))
    for chave, item in projectile_list.items():
        game_map[item.position[0]][item.position[1]] = chave
        occupied_spaces.append((item.position[0], item.position[1]))

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
            stateCalm(entity, team)

        elif entity.current_state == 1:
            stateAlert(entity, team)

        else:
            stateCombat(entity, team)

# calcular as ações a serem feitas - DONE
# colocar a lista de ações numa fila - DONE
# colocar num dict {id_entidade: lista_ações} - DONE
# quando for renderizar, itera por cada elemento do dict - da pop na lista,
#   atualiza o game_map e renderiza o movimento
# quando mudar de estado, apaga a entrada daquele id no dict - DONE

def stateCalm(entity: Entities.Entity, team): 
    # entidades calmas procuram por inimigos, se acharem mudar pro estado de atenção
    # se não encontrar decide entre esperar e se mover
    
    # se retornou algo diferente de None significa que acho um inimigo
    pos = findOnGameMap(entity.position, entity.vision_range, "1", team)
    if pos != None:
        entity.changeState(1)
        actionBroadcast(entity, team, 1)
        del move_buffer[entity.id]
        stateAlert(entity, team, pos)

    action = randint(1, 100)

    if entity.id.startswith("14"):
        actionWait(entity)

    else:
        if action <= 5:
            actionWait(entity)
        
        else: # se não achar nada tenta se mover pro meio do mapa
            actionMove(entity, (50+randint(-5,5), 50+randint(-5,5)))

def stateAlert(entity: Entities.Entity, team, position = None):
    # se há um inimigo dentro do alcançe de ataque da unidade, entra em combate
    if findOnGameMap(entity.position, entity.attack_range, "1", team) != None:
        entity.changeState(2)
        actionBroadcast(entity, team, 2)
        del move_buffer[entity.id]
        stateCombat(entity, team)

    # se não há mais inimigos vistos, volta pro calmo
    if findOnGameMap(entity.position, entity.vision_range, "1", team) == None:
        entity.changeState(0)
        # actionBroadcast(entity, team, 1)
        del move_buffer[entity.id]
        stateCalm(entity, team)

    # se for uma MG, pode começar a atirar onde viu o inimigo
    if entity.id.startswith("12") and randint(1, 100) >= 50: # 50% de chance de atirar
        actionAttack(entity, position)
    
    elif entity.id.startswith("14"):
        actionWait(entity)

    else:
        # escolhe entre continuar avançando, mover para tras de cenário ou ficar parado
        action = randint(1, 100)

        if action <= 5 and not entity.id.startswith("13"): # 5% de chance de ficar parado
            actionWait(entity)

        elif action > 5 and action <= 65 and not entity.id.startswith("13"): # 60% de chance de se mover pra trás de algum cover
            position = findOnGameMap(entity.position, entity.vision_range, "9") # procura por um objeto do cenário
            if position[1] >= 50: # muda o valor de y da posição pra não tentar calcular um path pra cima do objeto
                position[1] += 1 # se está acima da metade (equipe vermelha, sobe)
            else:
                position[1] -= 1 # se não (equipe azul) desce
            
            actionMove(entity, position)

        else: # continua movendo pro meio
            actionMove(entity, (50+randint(-5,5), 50+randint(-5,5)))
    
def stateCombat(entity: Entities.Entity, team):
    # se não há mais inimigos no alcançe de ataque, volta pro alerta
    if findOnGameMap(entity.position, entity.attack_range, "1", team) == None:
        entity.changeState(1)
        # actionBroadcast(entity, team, 2)
        del move_buffer[entity.id]
        stateAlert(entity, team)

    # se não for um tanque, escolhe entre mover pra cover ou atacar

    if not entity.id.startswith("13"):

        if randint(1, 100) <= 30 : # 30% de chance de se mover pra trás de algum cover
            position = findOnGameMap(entity.position, entity.vision_range, "9") # procura por um objeto do cenário
            if position[1] >= 50: # muda o valor de y da posição pra não tentar calcular um path pra cima do objeto
                position[1] += 1 # se está acima da metade (equipe vermelha, sobe)
            else:
                position[1] -= 1 # se não (equipe azul) desce
        actionMove(entity, position)
        return

    # se for artilharia, tem apenas uma chance de atacar
    if entity.id.startswith("14") and randint(1, 100) >= 10:
        return
    # para cada inimigo que vê e pode atirar, vai atirar neles
    enemies = findAllOnGameMap(entity.position, entity.attack_range, "1", team)

    for e in enemies:
        if entity.action_points > 0:
            actionAttack(entity, e)

def actionMove(entity: Entities.Entity, target):
    if entity.action_points > 0:
        # entity.action_points -= 1 # gasta os pontos de ação na Main
        move = entity.calculateMove(target)
        move_buffer[move[0]] = deque(move[1])

def actionWait(entity: Entities.Entity):
    entity.action_points -= 1
    return

def actionAttack(entity: Entities.Entity, target):
    if entity.action_points > 0: # cada tipo de entidade tem um caso
        entity.action_points -= 1 # pois cada entidade atira de uma forma diferente
        if entity.id.startswith("13"):
            target_id = game_map[target[0]][target[1]]
            if target_id.startswith("13") or target_id.startswith("14"):
                if entity.current_ammo == 1 and entity.checkAmmo() != -1:
                    entity.fire(target, "31")
                else:
                    actionReload(entity, 1)
            else:
                if entity.current_ammo == 2 and entity.checkAmmo() != -1:
                    entity.fire(target, "32")
                else:
                    actionReload(entity, 2)
        elif entity.id.startswith("14"):
            if entity.checkAmmo() != -1:
                entity.fire(target, "4")
            else:
                actionReload(entity)
        elif entity.id.startswith("12"):
            if entity.checkAmmo() != -1:
                for _ in range(10):
                    entity.fire(target, "2")
            else:
                actionReload(entity)
        else:
            if entity.checkAmmo() != -1:
                entity.fire(target, "2")
            else:
                actionReload(entity)
    else:
        return

def actionReload(entity: Entities.Entity, new_ammo = None):
    entity.action_points -= 1
    if entity.id.startswith("11"):
        entity.current_ammo = 8
    elif entity.id.startswith("12"):
        entity.current_ammo = 200
    else:
        entity.current_ammo = 1
        if new_ammo != None:
            entity.ammo_type = new_ammo

def actionBroadcast(entity: Entities.Entity, team, new_state):
    friendly_positions = findAllOnGameMap(entity.position, 10, "1", team, True)
    for pos_x, pos_y in friendly_positions:
        id = game_map[pos_x][pos_y]
        if entity_list[id] < new_state: # < new_state significa que só pode aumentar o estado
            entity_list[id].changeState(new_state) # i.e, calmo -> alerta, alerta -> combate