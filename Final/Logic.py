import Entities
import Main
from random import randint
from collections import deque

entity_list = {} # mantendo uma lista de todas as entidades atualmente existentes
terrain_list = {}
projectile_list = {}
move_buffer = {} # movimentos a serem tomados serão guardadas nessa lista
projectile_buffer = {} # projéteis que devem se mover num turno
explosion_buffer = {} # projéteis de explosão que devem se mover num turno
occupied_spaces = [] # lista de tuplas (x,y) de pontos no mapa que já estão ocupados

map_size = 100
game_map = [[None for i in range(map_size)] for i in range(map_size)]

def findOnGameMap(orig, depth, obj_type, team=None, is_own_team=False):
    # BFS para achar algo no mapa
    # obj_type é o caractere primeiro caractere da id do que está sendo procurado
    # depth é a profundidade da busca == o quão longe a entidade consegue ver
    # recebe a lista da própria equipe, para caso está procurando por inimigos, não retornar
    # que uma entidade da mesma equipe é um inimigo
    # game_map = game_map

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
    # game_map = game_map

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
    # gera 50 projéteis especiais para explosão
    
    projectiles = []
    for _ in range(50):
        p = Entities.Projectile(position, None, None)
        p.explosionProjectile(damage, radius+randint(-1,2))
        projectiles.append(p)
        explosion_buffer[p.id] = p

def projectileCollision(proj, position, blu_team, red_team):
    # se um projétil explosivo atinge algo, explode
    if proj.id.startswith("32") or proj.id.startswith("4"):
        del projectile_list[proj.id]
        createExplosion(proj.position, proj.radius, proj.damage)
        del proj

    elif game_map[position[0]][position[1]].startswith("9"):
        if randint(1, 100) <= 35 and not proj.id in explosion_buffer: # 35% de chance do projetil não colidir c/ terreno
            return
        if proj.id in explosion_buffer:
            del explosion_buffer[proj.id]
            del proj
        del projectile_list[proj.id]
        del proj # se uma bala normal atinge algo do terreno, nada acontece
    
    else: # se o alvo não é um terreno então é uma entidade - não vamos lidar com colisão entre projéteis
        del projectile_list[proj.id]
        target_id = game_map[position[0]][position[1]]
        target = entity_list[target_id]
        if target.takeDamage(proj.damage) == 0: # se perdeu toda a vida
            if target_id in blu_team:
                blu_team.remove(target_id)
                Main.red_points += target.id[:2]
                print("BLU Morreu: "+target.id)
                target.isKilled()
                return ("b", blu_team)
            elif target_id in red_team:
                red_team.remove(target_id)
                Main.blu_points += target.id[:2]
                print("RED Morreu: "+target.id)
                target.isKilled()
                return ("r", red_team)
            else:
                print("Morreu: ", target.id)
                print("Não estava em nenhuma equipe!")

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
        new_rifleman = Entities.createRifleman(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)
        # print("Rifleman="+new_rifleman)
        team.append(new_rifleman)
    for _ in range(10):
        new_mg = Entities.createMachineGunner(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)
        # print("MG="+new_mg)
        team.append(new_mg)
    for _ in range(4):
        new_tank = Entities.createTank(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)
        # print("Tank="+new_tank)
        team.append(new_tank)
    new_arty_tank = Entities.createArtilleryTank(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y)
    # print("Arty Tank="+new_arty_tank)
    team.append(new_arty_tank)

def takeTurn(team):

    for entity_id in team: # iterando pelas ids de entidades na lista da equipe
        # print(entity_id)
        entity = entity_list[entity_id]
        if entity.getState() == 0:
            stateCalm(entity, team)

        elif entity.getState() == 1:
            print("Ta na RED ?:", entity.id in Main.getRedTeam())
            print("Alerta: ", entity.id, " ", entity.position)
            stateAlert(entity, team)

        else:
            print("Ta na RED ?:", entity.id in Main.getRedTeam())
            print("Combate: ", entity.id, " ", entity.position)
            stateCombat(entity, team)

def stateCalm(entity, team): 
    # entidades calmas procuram por inimigos, se acharem mudar pro estado de atenção
    # se não encontrar decide entre esperar e se mover
    
    # se retornou algo diferente de None significa que acho um inimigo
    pos = findOnGameMap(entity.position, entity.vision_range, "1", team)
    if pos != None:
        entity.changeState(1)
        actionBroadcast(entity, team, 1)
        if entity.id in move_buffer:
            del move_buffer[entity.id]
        stateAlert(entity, team, pos)

    action = randint(1, 100)

    if entity.id.startswith("14") and action <= 95:
        actionWait(entity)

    else:
        if action <= 5:
            actionWait(entity)
        
        else: # se não achar nada tenta se mover pro meio do mapa
            if entity.id in move_buffer:
                return
            pos = (50+randint(-25,25), 50+randint(-25,25))
            i = 0
            while pos in occupied_spaces:
                pos = (50+randint(-25-i,25+i), 50+randint(-25-i,25+i))
                i += 1
            actionMove(entity, pos)

def stateAlert(entity, team, position = None):
    # se há um inimigo dentro do alcançe de ataque da unidade, entra em combate
    if findOnGameMap(entity.position, entity.attack_range, "1", team) != None:
        entity.changeState(2)
        actionBroadcast(entity, team, 2)
        if entity.id in move_buffer:
            del move_buffer[entity.id]
        # del move_buffer[entity.id]
        stateCombat(entity, team)

    # se não há mais inimigos vistos, volta pro calmo
    if findOnGameMap(entity.position, entity.vision_range, "1", team) == None:
        entity.changeState(0)
        # actionBroadcast(entity, team, 1)
        if entity.id in move_buffer:
            del move_buffer[entity.id]
        # del move_buffer[entity.id]
        stateCalm(entity, team)

    action = randint(1, 100)
    # se for uma MG, pode começar a atirar onde viu o inimigo
    if entity.id.startswith("12") and randint(1, 100) >= 50: # 50% de chance de atirar
        actionAttack(entity, position)
    
    elif entity.id.startswith("14")  and action <= 95:
        actionWait(entity)

    else:
        # escolhe entre continuar avançando, mover para tras de cenário ou ficar parado
        action = randint(1, 100)

        if action <= 5 and not entity.id.startswith("13"): # 5% de chance de ficar parado
            actionWait(entity)

        # elif action > 5 and action <= 65 and not entity.id.startswith("13"): # 60% de chance de se mover pra trás de algum cover
        #     position = findOnGameMap(entity.position, entity.vision_range, "9") # procura por um objeto do cenário
        #     if position != None:
        #         if position[1] >= 50: # muda o valor de y da posição pra não tentar calcular um path pra cima do objeto
        #             x = position[0]
        #             new_y = position[1] + 1
        #             position = (x, new_y) # # se está acima da metade (equipe vermelha, sobe)
        #         else:
        #             x = position[0]
        #             new_y = position[1] - 1
        #             position = (x, new_y) # # se não (equipe azul) desce
                
        #         actionMove(entity, position)

        else: # continua movendo pro meio
            if entity.id in move_buffer:
                return
            pos = (50+randint(-25,25), 50+randint(-25,25))
            i = 0
            while pos in occupied_spaces:
                pos = (50+randint(-25-i,25+i), 50+randint(-25-i,25+i))
                i += 1
            actionMove(entity, pos)
    
def stateCombat(entity, team):
    # se não há mais inimigos no alcançe de ataque, volta pro alerta
    if findOnGameMap(entity.position, entity.attack_range, "1", team) == None:
        entity.changeState(1)
        # actionBroadcast(entity, team, 2)
        if entity.id in move_buffer:
            del move_buffer[entity.id]
        # del move_buffer[entity.id]
        stateAlert(entity, team)

    # se não for um tanque, escolhe entre mover pra cover ou atacar

    # if not entity.id.startswith("13"):

    #     if randint(1, 100) <= 30 : # 30% de chance de se mover pra trás de algum cover
    #         position = findOnGameMap(entity.position, entity.vision_range, "9") # procura por um objeto do cenário
    #         if position != None:
    #             if position[1] >= 50: # muda o valor de y da posição pra não tentar calcular um path pra cima do objeto
    #                 x = position[0]
    #                 new_y = position[1] + 1
    #                 position = (x, new_y) # se está acima da metade (equipe vermelha, sobe)
    #             else:
    #                 x = position[0]
    #                 new_y = position[1] - 1
    #                 position = (x, new_y) # se não (equipe azul) desce
    #             actionMove(entity, position)
    #     return

    # se for artilharia, tem apenas uma chance de atacar
    if entity.id.startswith("14") and randint(1, 100) >= 10:
        return
    # para cada inimigo que vê e pode atirar, vai atirar neles
    enemies = findAllOnGameMap(entity.position, entity.attack_range, "1", team)

    for e in enemies:
        if entity.action_points > 0:
            actionAttack(entity, e)

def actionMove(entity, target):
    if entity.action_points > 0:
        # entity.action_points -= 1 # gasta os pontos de ação na Main
        move = entity.calculateMove(target)
        if move[1] != None:
            move_buffer[move[0]] = deque(move[1])

def actionWait(entity):
    entity.action_points -= 1
    return

def actionAttack(entity, target):
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

def actionReload(entity, new_ammo = None):
    entity.action_points -= 1
    if entity.id.startswith("11"):
        entity.current_ammo = 8
    elif entity.id.startswith("12"):
        entity.current_ammo = 200
    else:
        entity.current_ammo = 1
        if new_ammo != None:
            entity.ammo_type = new_ammo

def actionBroadcast(entity, team, new_state):
    friendly_positions = findAllOnGameMap(entity.position, 10, "1", team, True)
    for pos_x, pos_y in friendly_positions:
        id = game_map[pos_x][pos_y]
        if entity_list[id].getState() < new_state: # < new_state significa que só pode aumentar o estado
            entity_list[id].changeState(new_state) # i.e, calmo -> alerta, alerta -> combate