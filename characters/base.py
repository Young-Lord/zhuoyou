print(123)
class Player:
    life = -1
    energy = -1
    pos = (-1, -1)
    is_dead = False
    team = 0
    role = None
    item = list()
    buff = list()
    weapon = None
    attack_add = 0
    attack_percent = 100
    damage_minus = 0
    damage_percent = 100
    def attack(self, target):
        pass

    def damage(self):
        pass
