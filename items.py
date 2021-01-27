weapons={
None:{"name":"无","value":5,"distance":1},
"测试-伤害10":{"name":"测试1","value":"10","distance":3},
"测试-伤害15":{"name":"测试2","value":"15","distance":5},
"屠龙宝刀":{"name":"屠龙宝刀1","value":"1000","distance":100}
    }
shields={
None:{"name":"无","value":0},
"盾牌":{"name":"盾牌","value":1},
"测试-防御3":{"name":"测试2","value":3}
    }
shoes={
None:{"name":"无","value":0},
"鞋子":{"name":"鞋子","value":3},
"测试-加速1":{"name":"测试1","value":1},
"测试-加速3":{"name":"测试2","value":3}
    }
energy_books={
None:{"name":"无","value":0},
"魔法书":{"name":"魔法书","value":3}
    }
#-药- -武器- -鞋子- -盾牌- -能量书- 钩爪 偷窃 五雷天罡法 无懈可击(被动)
class drug:
    display_name="药"
    value=5
    def use(self,sender,*arg):
        sender.life+=self.value
        sender.update()

class weapon:
    diplay_name="武器_父类"
    value="测试-伤害10"
    def use(self,sender,*arg):
        if sender.weapon==None:
            sender.item.append(weapon_None())
        sender.weapon=self.value
class weapon_None(weapon):
    display_name="不使用武器"
    value=None

class shoe:
    diplay_name="鞋子"
    value="鞋子"
    def use(self,sender,*arg):
        if sender.shoe==None:
            sender.item.append(shoe_None())
        sender.shoe=self.value
class shoe_None(shoe):
    display_name="不使用鞋子"
    value=None

class shield:
    diplay_name="盾牌"
    value="盾牌"
    def use(self,sender,*arg):
        if sender.shield==None:
            sender.item.append(shield_None())
        sender.shield=self.value
class shield_None(shoe):
    display_name="不使用盾牌"
    value=None

class energy_book:
    diplay_name="魔法书"
    value="魔法书"
    def use(self,sender,*arg):
        if sender.energy_book==None:
            sender.item.append(energy_book_None())
        sender.energy_book=self.value
class energy_book_None(shoe):
    display_name="不使用能量书"
    value=None
