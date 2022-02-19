from random import randint
import Logic

"""
TODO:   
    Explicar ids
    Explicar tipos de projeteis
    Calcular explosões
    Resolver Colisões de projéteis
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
    curret_state = 0   # estado atual da entidade, controlado principalmente pela lógica
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
            damage = damage//100
            self.life -= damage

    def isKilled(self):
        Logic.idList.remove(self.id) # remove a id do soldado da lista de ids livres

        if(isinstance(self, Tank)): # se um tanque morre ele vira um objeto do terreno
            T = Terrain(self.position[0], self.position[1], self.size)
            Logic.idList.append(T.id)

        del self # objeto só é removido inteiramente da memória se não há mais referencias a ele

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
        self.action_points = 2
        self.attack_range = 50

class MachineGunner(Soldier):

    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x,pos_y)
        self.id = "12"+self.id
        self.ammo_amount = 200
        self.action_points = 1
        self.attack_range = 100

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
        self.action_points = 3
        self.attack_range = 150
        self.size = (3,7)

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

class Projectile(object):
    id = ""
    position = ""
    parent_id = "" # id da entidade que criou este projetil
    ttl = 0

    def __init__(self, pos_x, pos_y, parent_id):
        self.id = str(randint(100, 9999))
        self.position = (pos_x, pos_y)
        self.parent_id = parent_id

    def checkCollision(self, target):
        if target.id != self.parent_id: # projetil não colide com a entidade que gerou ele
            if self.position == target.position: # posição sempre é uma tupla (x,y)
                pass # TODO: resolver colisao de projetil

class RifleRound(Projectile):
    
    def __init__(self, pos_x, pos_y, parent_id):
        super().__init__(pos_x, pos_y,parent_id)
        self.id = "2"+self.id
        self.damage = 10 + randint(-5,5)
        self.armor_penetration = 0
        self.velocity = 20
        self.ttl = 150 + randint(-50, 50)

class TankAPRound(Projectile):

    def __init__(self, pos_x, pos_y, parent_id):
        super().__init__(pos_x, pos_y,parent_id)
        self.id = "3"+self.id
        self.damage = 100 + randint(-20,20)
        self.armor_penetration = 40 + randint(-5,15)
        self.velocity = 100
        self.ttl = 200 + randint(-50, 50)

class TankHERound(Projectile):

    def __init__(self, pos_x, pos_y, parent_id):
        super().__init__(pos_x, pos_y,parent_id)
        self.id = "3"+self.id
        self.damage = 150 + randint(-20,20)
        self.armor_penetration = 5 + randint(0,5)
        self.velocity = 100
        self.ttl = 200 + randint(-50, 50)
        self.radius = 10

class ArtilleryRound(Projectile):

    def __init__(self, pos_x, pos_y, parent_id):
        super().__init__(pos_x, pos_y,parent_id)
        self.id = "5"+self.id
        self.damage = 500
        self.armor_penetration = 5 + randint(-5,15)
        self.velocity = 75
        self.ttl = 500 + randint(50, 100)
        self.radius = 50

class Terrain(object):

    def __init__(self, pos_x, pos_y, size):
        self.id = "9" + str(randint(100, 9999))
        self.position = (pos_x, pos_y)
        self.size = size # tamnho em x e y do objeto

    def createTerrain(self, pos_x, pos_y): # gera um objeto de terreno que é colocado no cenário
        x = randint(1,3)
        obj = Terrain(pos_x, pos_y, (x, x))
        return obj.id