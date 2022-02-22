from random import randint
from collections import deque
import Logic

used_ids = [] # lista de todos os ids que já estão associados a alguma coisa

"""
TODO:   
    Calcular explosões
    Comandos do player

IDs:
    IDs de entidades começam com 1 seguido por mais um digito que define o tipo de entidade e então 
    mais três digitos que diferenciam as entidades de um dado tipo, temos as seguinte classes de entidades:

    11xxx: Rifleman, fuzileiro, soldado mais comum, tem algumas ações num turno
    12xxx: MachineGunner, , soldado especial, tem mais munição e atira várias balas num turno, mas tem menos ações
    13xxx: MediumTank, tanque médio, tem bastante armadura e pode fazer várias ações, mas só pode atirar 1 vez antes de recarregar 
                        e demora vários turnos para recarregar
    14xxx: ArtilleryTank, tanque de artilharia, tem pouca armadura, pode fazer poucas ações e demora pra recarregar, 
                        mas tem o maior alcance de ataque e pode atacar qualquer parte do mapa manualmente

    IDs de projéteis começam com 2 ou 3 seguido por mais um digito ou 4, então mais 4 digitos que diferenciam projéteis 
    de um dado tipo, temos as seguintes classe de projéteis:

    2xxxx:  RifleRound, projétil disparado pelos soldados, da o menor dano, tem pouca penetração de armadura,
                     tem alta dispersão e menor tempo de vida
    31xxxx: TankAPRound, projétil penetrante de tanque, tem maior penetração de armadura, alto dano, baixa dispersão 
                     e alto tempo de vida
    32xxxx: TankHERound, projétil explosivo de tanque, tem baixa penetração de armadura, dano alto alta dispersão, alto tempo
                     de vida e é explosivo, isto é, quando ttl = 0 ou quando colide com algo, gera uma explosão
    4xxxx:  ArtilleryRound, projétil do tanque de artilharia, tem baixa penetração de armadura, extrema dispersão,
                     alto tempo de vida e o maior dano de todos os projéteis

    IDs de terreno começam com 9, seguido por um digito então por mais 3 dígitos que diferenciam objetos únicos no terreno, 
    temos as seguintes classes de terrenos:

    91xxx: Objetos que bloqueiam caminho de entidades e projéteis, quando tanques são destruidos, no lugar onde estavam é inserido
            um objeto deste tipo
    92xxx: Objetos que não bloqueiam caminha de entidades e projéteis, quando projéteis de artilharia explodem, há uma
            pequena chance de um objeto deste tipo ser inserido na posição onde estava esse projétil

Estados:
    Cada entidade pode estar em 1 de 3 estados, que definem quais ações as entidades vão tomar, assim como as chances delas
    tomarem essas ações, os estados são os seguinte:

    0: Estado calmo, a entidade não sabe da posição de nenhum inimigo e portanto vai apenas se mover pelo mapa ou ficar onde está
    1: Estado alerta, a entidade encontrou um inimigo (está dentro do alcançe de visão dela, mas não dentro do alcançe de ataque) 
        e notificou as outras entidades da equipe, vai procurar e se mover para trás de objetos do cenário, ou continuar avançando, 
        apenas MGs podem começar a atirar e apenas na posição onde o inimigo foi detectado
    2: Estado combate, há entidades inimigas dentro do alcançe de ataque da entidade, ela livremente ataca o inimigo e notifica
        outras entidades da equipe sobre a posição do inimigo
"""

def rebuildPath(path, orig, dest):
    end = path[dest[0]][dest[1]]
    i, j = end
    final_path = [end]

    if orig == end:
        return final_path

    while path[i][j] != orig:
        # print(i,j)
        # print(path[i][j])
        final_path.append(path[i][j])
        # if path[i][j] == None:
            # print(orig)
            # print(i, j)
            # input()
        if path[i][j] != None:
            i, j = path[i][j]
    final_path.reverse()
    return final_path

def findPathOnGameMap(orig, dest, map_size): # BFS para achar um caminho entre dois pontos
    game_map = Logic.game_map

    orig_x, orig_y = orig
    dest_x, dest_y = dest
    x, y = 0, 0

    visitados = [[False for i in range(map_size)] for i in range(map_size)]
    visitados[orig_x][orig_y] = True
    traverse_queue = deque()
    traverse_queue.append(orig)
    path = [[None for i in range(map_size)] for i in range(map_size)]

    dir_x = [1, 0, -1, 0]
    dir_y = [0, 1, 0, -1]
    visitados[orig_x][orig_y] = True

    while len(traverse_queue) > 0:
        head = traverse_queue.popleft()

        for i in range(4):
            x = dir_x[i] + head[0] 
            y = dir_y[i] + head[1]

            outside_borders = x <= 0 or y <= 0 or x >= map_size or y >= map_size
            if outside_borders:
                continue
            
            if visitados[x][y]: # pode causar erro de Array out of Bounds se isso ficar no if acima
                continue

            if x == dest_x and y == dest_y:
                path[x][y] = (x - dir_x[i], y - dir_y[i])
                return rebuildPath(path, orig, dest)

            if game_map[x][y] == None and not visitados[x][y]:
                path[x][y] = (x - dir_x[i], y - dir_y[i])
                visitados[x][y] = True
                traverse_queue.append((x,y))
    
    return None

def findDiagonalPathOnGameMap(orig, dest, map_size): # BFS para achar um caminho entre dois pontos com movimentos diagonais
    game_map = Logic.game_map

    orig_x, orig_y = orig
    dest_x, dest_y = dest
    x, y = 0, 0

    visitados = [[False for i in range(map_size)] for i in range(map_size)]
    visitados[orig_x][orig_y] = True
    traverse_queue = deque()
    traverse_queue.append(orig)
    path = [[None for i in range(map_size)] for i in range(map_size)]

    dir_x = [1, -1, 0, 0, 1, 1, -1, -1]
    dir_y = [0, 0, 1, -1, 1, -1, 1, -1]
    visitados[orig_x][orig_y] = True

    while len(traverse_queue) > 0:
        head = traverse_queue.popleft()

        for i in range(8):
            x = dir_x[i] + head[0] 
            y = dir_y[i] + head[1]

            outside_borders = x <= 0 or y <= 0 or x >= map_size or y >= map_size
            if outside_borders:
                continue
            
            if visitados[x][y]: # pode causar erro de Array out of Bounds se isso ficar no if acima
                continue

            if x == dest_x and y == dest_y:
                path[x][y] = (x - dir_x[i], y - dir_y[i])
                return rebuildPath(path, orig, dest)

            if game_map[x][y] == None and not visitados[x][y]:
                path[x][y] = (x - dir_x[i], y - dir_y[i])
                visitados[x][y] = True
                traverse_queue.append((x,y))
    
    return None

def createRifleman(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y):
    pos_x = randint(lower_limit_x, upper_limit_x)
    pos_y = randint(lower_limit_y, upper_limit_y)
    while (pos_x, pos_y) in Logic.occupied_spaces:
        pos_x = randint(lower_limit_x, upper_limit_x)
        pos_y = randint(lower_limit_y, upper_limit_y)

    while (pos_x, pos_y) in Logic.occupied_spaces:
        pos_x = randint(lower_limit_x, upper_limit_x)
        pos_y = randint(lower_limit_y, upper_limit_y)
        dir_x = [1, -1, 0, 0, 1, 1, -1, -1]
        dir_y = [0, 0, 1, -1, 1, -1, 1, -1]
        for dirx, diry in zip(dir_x, dir_y):
            while (pos_x+dirx, pos_y+diry) in Logic.occupied_spaces:
                pos_x = randint(lower_limit_x, upper_limit_x)
                pos_y = randint(lower_limit_y, upper_limit_y)

    R = Rifleman(pos_x, pos_y)
    used_ids.append(R.id)
    return R.id

def createMachineGunner(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y):
    pos_x = randint(lower_limit_x, upper_limit_x)
    pos_y = randint(lower_limit_y, upper_limit_y)
    while (pos_x, pos_y) in Logic.occupied_spaces:
        pos_x = randint(lower_limit_x, upper_limit_x)
        pos_y = randint(lower_limit_y, upper_limit_y)
    
    while (pos_x, pos_y) in Logic.occupied_spaces:
        pos_x = randint(lower_limit_x, upper_limit_x)
        pos_y = randint(lower_limit_y, upper_limit_y)
        dir_x = [1, -1, 0, 0, 1, 1, -1, -1]
        dir_y = [0, 0, 1, -1, 1, -1, 1, -1]
        for dirx, diry in zip(dir_x, dir_y):
            while (pos_x+dirx, pos_y+diry) in Logic.occupied_spaces:
                pos_x = randint(lower_limit_x, upper_limit_x)
                pos_y = randint(lower_limit_y, upper_limit_y)

    M = MachineGunner(pos_x, pos_y)
    used_ids.append(M.id)
    return M.id

def createTank(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y):
    pos_x = randint(lower_limit_x, upper_limit_x)
    pos_y = randint(lower_limit_y, upper_limit_y)
    while (pos_x, pos_y) in Logic.occupied_spaces:
        pos_x = randint(lower_limit_x, upper_limit_x)
        pos_y = randint(lower_limit_y, upper_limit_y)
    
    while (pos_x, pos_y) in Logic.occupied_spaces:
        pos_x = randint(lower_limit_x, upper_limit_x)
        pos_y = randint(lower_limit_y, upper_limit_y)
        dir_x = [1, -1, 0, 0, 1, 1, -1, -1]
        dir_y = [0, 0, 1, -1, 1, -1, 1, -1]
        for dirx, diry in zip(dir_x, dir_y):
            while (pos_x+dirx, pos_y+diry) in Logic.occupied_spaces:
                pos_x = randint(lower_limit_x, upper_limit_x)
                pos_y = randint(lower_limit_y, upper_limit_y)

    T = MediumTank(pos_x, pos_y)
    used_ids.append(T.id)
    return T.id

def createArtilleryTank(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y):
    pos_x = randint(lower_limit_x, upper_limit_x)
    pos_y = randint(lower_limit_y, upper_limit_y)
    while (pos_x, pos_y) in Logic.occupied_spaces:
        pos_x = randint(lower_limit_x, upper_limit_x)
        pos_y = randint(lower_limit_y, upper_limit_y)
    
    while (pos_x, pos_y) in Logic.occupied_spaces:
        pos_x = randint(lower_limit_x, upper_limit_x)
        pos_y = randint(lower_limit_y, upper_limit_y)
        dir_x = [1, -1, 0, 0, 1, 1, -1, -1]
        dir_y = [0, 0, 1, -1, 1, -1, 1, -1]
        for dirx, diry in zip(dir_x, dir_y):
            while (pos_x+dirx, pos_y+diry) in Logic.occupied_spaces:
                pos_x = randint(lower_limit_x, upper_limit_x)
                pos_y = randint(lower_limit_y, upper_limit_y)

    A = ArtilleryTank(pos_x, pos_y)
    used_ids.append(A.id)
    return A.id

def generateRandomTerrain(lower_limit_x, upper_limit_x, lower_limit_y, upper_limit_y): 
    # gera um objeto de terreno que é colocado no cenário
    pos_x = randint(lower_limit_x, upper_limit_x)
    pos_y = randint(lower_limit_y, upper_limit_y)
    while (pos_x, pos_y) in Logic.occupied_spaces:
        pos_x = randint(lower_limit_x, upper_limit_x)
        pos_y = randint(lower_limit_y, upper_limit_y)
    x = randint(1,3)
    T = Terrain(pos_x, pos_y, (x, x))
    used_ids.append(T.id)
    return T.id

class Entity(object):
    id = ""            # id da entidade
    life = 0           # quanto dano a entidade pode receber antes de morrer
    armor = 0          # quanto dano a entidade pode ignorar
    ammo_amount = 0    # quantos tiros pode dar antes de recarregar
    ammo_type = 0      # que tipo de projetil é gerando quando a entidade ataca
    position = (-1,-1) # onde a entidade está no mapa
    action_points = 0  # quantas ações a entidade pode fazer num turno
    vision_range = 0   # quão longe uma entidade consegue detectar entidades inimigas
    attack_range = 0   # quão longe uma entidade consegue atacar uma entidade inimiga
    curret_state = 0   # estado atual da entidade, controlado pela lógica do jogo
    current_ammo = 0   # atributo exclusivo ao tanque, que indica que tipo de munição está carregada
    size = (-1,-1)     # tamanho da entidade, usado para desenhar ela na tela

    def __init__(self, pos_x, pos_y):
        self.id = str(randint(100, 999))
        self.position = (pos_x, pos_y)
        self.curret_state = 0

    def getState(self):
        return self.curret_state

    def changeState(self, new_state):
        self.curret_state = new_state

    def takeDamage(self, damage):
        if damage >= self.armor: # trivialmente verdadeiro no caso do soldado
            if damage >= self.life:
                return 0
            else:
                self.life -= damage
                return 1
        else:
            if damage * 2 < self.armor:
                return 1 # se dano for menor que metade do valor da armadura é ignorado
            self.life -= damage//100
            return 1

    def resetActionPoints(self):
        if self.id.startswith("11"):
            self.action_points = 3
        elif self.id.startswith("12"):
            self.action_points = 2
        elif self.id.startswith("13"):
            self.action_points = 2
        else:
            self.action_points = 1

    def isKilled(self):
        del Logic.entity_list[self.id] # remove a id da entidade da lista de entidades existentes

        if(isinstance(self, Tank)): # se um tanque morre ele vira um objeto do terreno
            T = Terrain(self.position[0], self.position[1], self.size)
            Logic.terrain_list[T.id] = T

        del self # objeto só é removido inteiramente da memória se não há mais referencias a ele

    def checkAmmo(self):
        if self.ammo_amount >= 1:
            if not self.id.startswith("12"):
                return 1
            if self.ammo_amount >= 10:
                return 1
        return -1

    def fire(self, target, ammo_type): # metodo para uma entidade disparar um ataque
        self.ammo_amount -= 1
        if ammo_type == "31":
            TankAPRound(self.position, target, self.id).createProjectile()
        elif ammo_type == "32":
            TankHERound(self.position, target, self.id).createProjectile()
        elif ammo_type == "4":
            ArtilleryRound(self.position, target, self.id).createProjectile()
        else:
            RifleRound(self.position, target, self.id).createProjectile()

    def calculateMove(self, target): # target sera uma tupla
        path = findPathOnGameMap(self.position, target, Logic.map_size)
        return (self.id, path)
        # Logic.action_buffer[self.id] = path

    def updatePosition(self, new_position):
        self.position = new_position

class Soldier(Entity):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x,pos_y)
        self.life = 10
        self.armor = 0 
        self.ammo_type = 2
        self.vision_range = 60 + randint(-5,15)
        self.size = (1,1)

class Rifleman(Soldier):

    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x,pos_y)
        self.id = "11"+self.id
        while self.id in used_ids:
            self.id = "11"+str(randint(100, 999))
        self.ammo_amount = 8
        self.action_points = 3
        self.attack_range = 50
        self.curret_state = 0
        Logic.entity_list[self.id] = self # inserindo a entidade criada na lista de entidades existentes

class MachineGunner(Soldier):

    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x,pos_y)
        self.id = "12"+self.id
        while self.id in used_ids:
            self.id = "12"+str(randint(100, 999))
        self.ammo_amount = 200
        self.action_points = 2
        self.attack_range = 40
        Logic.entity_list[self.id] = self # inserindo a entidade criada na lista de entidades existentes

class Tank(Entity):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x,pos_y)
        self.life = 100
        self.vision_range = 80 + randint(-5,5)

class MediumTank(Tank):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x,pos_y)
        self.id = "13"+self.id
        while self.id in used_ids:
            self.id = "13"+str(randint(100, 999))
        self.armor = 50
        self.ammo_amount = 1
        self.ammo_type = 3
        self.current_ammo = 2
        self.action_points = 2
        self.attack_range = 70
        self.size = (3,7)
        Logic.entity_list[self.id] = self # inserindo a entidade criada na lista de entidades existentes

class ArtilleryTank(Tank):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x,pos_y)
        self.id = "14"+self.id
        while self.id in used_ids:
            self.id = "14"+str(randint(100, 999))
        self.armor = 25
        self.ammo_amount = 1
        self.ammo_type = 4
        self.action_points = 1
        self.attack_range = 100
        self.size = (2,5)
        Logic.entity_list[self.id] = self # inserindo a entidade criada na lista de entidades existentes

class Projectile(object):
    id = ""
    position = (0,0)
    target = (0,0)
    parent_id = "" # id da entidade que criou este projetil
    damage = 0
    radius = 0
    ttl = 0
    dispersion = (0,0) # (% de chance do projétil desviar, direcao p/ onde vai desviar (-1 esq, 1 dir))

    def __init__(self, position, target, parent_id):
        self.id = str(randint(1000, 9999))
        self.position = position
        self.target = target
        self.parent_id = parent_id

    def explosionProjectile(self, damage, radius):
        self.damage = damage
        self.ttl = radius
        self.parent_id = None
        self.target = None

    def createProjectile(self):
        path = findDiagonalPathOnGameMap(self.position, self.target, Logic.map_size)
        for pos,pair in enumerate(path): # aplicando a dispersão nos projéteis disparados
            if randint(1, 100) <= self.dispersion[0]:
                for i in range(pos, len(path)):
                    pair = path[i]
                    pair = (pair[0]+self.dispersion[1], pair[1])
                    path[i] = pair
        used_ids.append(self.id)
        Logic.projectile_buffer[self.id] = self
        Logic.projectile_buffer[self.id] = deque(path)

    # def checkCollision(self, target):
    #     # uma bala é destruida sempre que atinge alguma coisa
    #     if target.id != self.parent_id: # projetil não colide com a entidade que gerou ele
    #         if self.position == target.position: # posição sempre é uma tupla (x,y)

                

    #                 if self.id.startswith("4") and randint(1,100) <= 10: # se é artilharia, pode criar um buraco
    #                     T = Terrain(self.position[0], self.position[1], (1,1))
    #                     T.setNonBlocker()
    #                     Logic.terrain_list[T.id] = T
    #                 del self

    #             elif target.id.statswith("9"): 
    #                 del Logic.projectile_list[self.id]
    #                 del self # se uma bala normal atinge algo do terreno, nada acontece

    #             else: # se o alvo não é um terreno então é uma entidade - não vamos lidar com colisão entre projéteis
    #                 del Logic.projectile_list[self.id]
    #                 target.takeDamage(self.damage)
    #                 del self

    def zeroTTL(self): # se TTL = 0, projétil é deletado
        del Logic.projectile_list[self.id] 

        if self.id.startswith("32") or self.id.startswith("4"): # se é explosivo, explode
            Logic.createExplosion(self.position, self.radius, self.damage)

            if self.id.startswith("4") and randint(1,100) <= 10: # se é artilharia, pode criar um buraco
                T = Terrain(self.position[0], self.position[1], (1,1))
                T.setNonBlocker()
                Logic.terrain_list[T.id] = T
        
        del self

class RifleRound(Projectile):
    
    def __init__(self, position, target, parent_id):
        super().__init__(position, target, parent_id)
        self.id = "2"+self.id
        while self.id in used_ids:
            self.id = "2"+str(randint(1000, 9999))
        self.damage = 10 + randint(-5,5)
        self.armor_penetration = randint(0,10)
        self.ttl = 40 + randint(-20, 20)
        x = randint(0,1)
        x = 1 if x == 0 else -1
        self.dispersion = (25, x)
        Logic.projectile_list[self.id] = self

class TankAPRound(Projectile):

    def __init__(self, position, target, parent_id):
        super().__init__(position, target,parent_id)
        self.id = "31"+self.id
        while self.id in used_ids:
            self.id = "31"+str(randint(1000, 9999))
        self.damage = 100 + randint(-20,20)
        self.armor_penetration = 40 + randint(-5,15)
        self.ttl = 60 + randint(-10, 10)
        x = randint(0,1)
        x = 1 if x == 0 else -1
        self.dispersion = (10, x)
        Logic.projectile_list[self.id] = self

class TankHERound(Projectile):

    def __init__(self, position, target, parent_id):
        super().__init__(position, target,parent_id)
        self.id = "32"+self.id
        while self.id in used_ids:
            self.id = "32"+str(randint(1000, 9999))
        self.damage = 150 + randint(-20,20)
        self.armor_penetration = 5 + randint(0,5)
        self.ttl = 50 + randint(-20, 20)
        self.radius = 2
        x = randint(0,1)
        x = 1 if x == 0 else -1
        self.dispersion = (20, x)
        Logic.projectile_list[self.id] = self

class ArtilleryRound(Projectile):

    def __init__(self, position, target, parent_id):
        super().__init__(position, target, parent_id)
        self.id = "4"+self.id
        while self.id in used_ids:
            self.id = "4"+str(randint(1000, 9999))
        self.damage = 500
        self.armor_penetration = 5 + randint(-5,15)
        self.ttl = 100 + randint(-50, 0)
        self.radius = 5
        x = randint(0,1)
        x = 1 if x == 0 else -1
        self.dispersion = (35, x)
        Logic.projectile_list[self.id] = self

class Terrain(object):
    id = ""
    position = (-1,-1)
    size = (-1, -1)
    blocks_path = False

    def __init__(self, pos_x, pos_y, size):
        self.id = "91" + str(randint(100, 999))
        while self.id in used_ids:
            self.id = "91" + str(randint(100, 999))
        self.position = (pos_x, pos_y)
        self.size = size # tamnho em x e y do objeto
        self.blocks_path = True
        Logic.terrain_list[self.id] = self

    def setNonBlocker(self):
        del Logic.terrain_list[self.id]
        self.id = "92" + self.id[2:]
        self.blocks_path = False
        Logic.terrain_list[self.id] = self

