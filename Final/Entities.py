from random import randint
import Logic

"""
TODO:   
    Estados de entidades
    Calcular explosões
    Metodo para entidades atirarem
    Metodo para entidades moverem
    Metodo para entidades recarregarem

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
"""

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
    size = (-1,-1)     # tamanho da entidade, usado para desenhar ela na tela

    def __init__(self, pos_x, pos_y):
        self.id = str(randint(100, 999))
        self.position = (pos_x, pos_y)

    def takeDamage(self, damage):
        if damage >= self.armor: # trivialmente verdadeiro no caso do soldado
            if damage >= self.life:
                self.isKilled # mata a entidade
            else:
                self.life -= damage
        else:
            if damage * 2 < self.armor:
                return # se dano for menor que metade do valor da armadura é ignorado
            self.life -= damage//100

    def isKilled(self):
        del Logic.entity_list[self.id] # remove a id da entidade da lista de entidades existentes

        if(isinstance(self, Tank)): # se um tanque morre ele vira um objeto do terreno
            T = Terrain(self.position[0], self.position[1], self.size)
            Logic.terrain_list[T.id] = T

        del self # objeto só é removido inteiramente da memória se não há mais referencias a ele

    def fire(self, isTankFiring = False, projType = None): # metodo para uma entidade disparar um ataque
        self.action_points -= 1
        self.ammo_amount -= 1

        if isTankFiring: # como um tanque tem dois tipos de municao, tem um tratamento especial
            pass
        else:
            if self.ammo_type == 2: # se não é um tanque, ou é um soldado
                P = RifleRound(self.position[0],self.position[1], self.id)
            else: # ou artilharia
                pass

class Soldier(Entity):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x,pos_y)
        self.life = 10
        self.armor = 0 
        self.ammo_type = 2
        self.vision_range = 150 + randint(-25,25)
        self.size = (1,1)

class Rifleman(Soldier):

    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x,pos_y)
        self.id = "11"+self.id
        self.ammo_amount = 8
        self.action_points = 3
        self.attack_range = 50
        Logic.entity_list[self.id] = self # inserindo a entidade criada na lista de entidades existentes

class MachineGunner(Soldier):

    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x,pos_y)
        self.id = "12"+self.id
        self.ammo_amount = 200
        self.action_points = 2
        self.attack_range = 100
        Logic.entity_list[self.id] = self # inserindo a entidade criada na lista de entidades existentes

class Tank(Entity):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x,pos_y)
        self.life = 100
        self.vision_range = 300 + randint(-5,50)

class MediumTank(Tank):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x,pos_y)
        self.id = "13"+self.id
        self.armor = 50
        self.ammo_amount = 1
        self.ammo_type = 3
        self.action_points = 2
        self.attack_range = 150
        self.size = (3,7)
        Logic.entity_list[self.id] = self # inserindo a entidade criada na lista de entidades existentes

class ArtilleryTank(Tank):

    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x,pos_y)
        self.id = "14"+self.id
        self.armor = 25
        self.ammo_amount = 1
        self.ammo_type = 4
        self.action_points = 1
        self.attack_range = 300
        self.size = (2,5)
        Logic.entity_list[self.id] = self # inserindo a entidade criada na lista de entidades existentes

class Projectile(object):
    id = ""
    position = ""
    parent_id = "" # id da entidade que criou este projetil
    damage = 0
    radius = 0
    ttl = 0
    dispersion = (0,0) # (% de chance do projétil desviar, direcao p/ onde vai desviar (-1 esq, 1 dir))
    # projéteis começam a desviar depois de passar 10% do seu TTL

    def __init__(self, pos_x, pos_y, parent_id):
        self.id = str(randint(1000, 9999))
        self.position = (pos_x, pos_y)
        self.parent_id = parent_id

    def checkCollision(self, target):
        # uma bala é destruida sempre que atinge alguma coisa
        if target.id != self.parent_id: # projetil não colide com a entidade que gerou ele
            if self.position == target.position: # posição sempre é uma tupla (x,y)

                if self.id.startswith("32") or self.id.startswith("4"):
                    del Logic.projectile_list[self.id]
                    Logic.createExplosion(self.position, self.radius, self.damage)

                    if self.id.startswith("4") and randint(1,100) <= 10: # se é artilharia, pode criar um buraco
                        T = Terrain(self.position[0], self.position[1], (1,1))
                        T.setNonBlocker()
                        Logic.terrain_list[T.id] = T
                    del self

                elif target.id.statswith("9"): 
                    del Logic.projectile_list[self.id]
                    del self # se uma bala normal atinge algo do terreno, nada acontece

                else: # se o alvo não é um terreno então é uma entidade - não vamos lidar com colisão entre projéteis
                    del Logic.projectile_list[self.id]
                    target.takeDamage(self.damage)
                    del self

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
    
    def __init__(self, pos_x, pos_y, parent_id):
        super().__init__(pos_x, pos_y,parent_id)
        self.id = "2"+self.id
        self.damage = 10 + randint(-5,5)
        self.armor_penetration = randint(0,10)
        self.ttl = 150 + randint(-50, 50)
        x = randint(0,1)
        x = 1 if x == 0 else -1
        self.dispersion = (25, x)
        Logic.projectile_list[self.id] = self

class TankAPRound(Projectile):

    def __init__(self, pos_x, pos_y, parent_id):
        super().__init__(pos_x, pos_y,parent_id)
        self.id = "31"+self.id
        self.damage = 100 + randint(-20,20)
        self.armor_penetration = 40 + randint(-5,15)
        self.ttl = 200 + randint(-50, 50)
        x = randint(0,1)
        x = 1 if x == 0 else -1
        self.dispersion = (10, x)
        Logic.projectile_list[self.id] = self

class TankHERound(Projectile):

    def __init__(self, pos_x, pos_y, parent_id):
        super().__init__(pos_x, pos_y,parent_id)
        self.id = "32"+self.id
        self.damage = 150 + randint(-20,20)
        self.armor_penetration = 5 + randint(0,5)
        self.ttl = 200 + randint(-50, 50)
        self.radius = 2
        x = randint(0,1)
        x = 1 if x == 0 else -1
        self.dispersion = (20, x)
        Logic.projectile_list[self.id] = self

class ArtilleryRound(Projectile):

    def __init__(self, pos_x, pos_y, parent_id):
        super().__init__(pos_x, pos_y,parent_id)
        self.id = "4"+self.id
        self.damage = 500
        self.armor_penetration = 5 + randint(-5,15)
        self.ttl = 500 + randint(-200, 0)
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
        self.position = (pos_x, pos_y)
        self.size = size # tamnho em x e y do objeto
        self.blocks_path = True
        Logic.terrain_list[self.id] = self

    def setNonBlocker(self):
        del Logic.terrain_list[self.id]
        self.id = "92" + self.id[2:]
        self.blocks_path = False
        Logic.terrain_list[self.id] = self

