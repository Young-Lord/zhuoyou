# 警告：本文件是在每次运行时自动生成的，修改此文件没有任何意义
from items import *


# Code from base.py:
class Player:
    name="默认角色"
    life = 80
    energy = 80
    pos = (-1, -1)
    alive = True
    team = 0
    item = list()
    buff = list() # 这是存各种主动技能的标记（如“义”）用的
    weapon = None
    armor=None
    shoe=None
    attack_add = 0 #先add在percent
    attack_percent = 100
    damage_minus = 0
    damage_percent = 100
    def attack(self, target):
        target.damage((weapons[self.weapon]+self.attack_add)*self.attack_percent//100)
        self.update()
    def damage(self,value):
        if ((value-armors[self.armor]-self.damage_minus)*self.damage_percent//100)>0:
            self.life-=(value-armors[self.armor]-self.damage_minus)*self.damage_percent//100
        self.update()
    def update(self):
        pass


# Code from try1.py:
class tryyy:
    life = 1