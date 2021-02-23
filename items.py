import astar
import random

weapons = {
    None: {"name": "无", "value": 5, "distance": 1},
    "测试-伤害10": {"name": "测试1", "value": 10, "distance": 3},
    "测试-伤害15": {"name": "测试2", "value": 15, "distance": 5},
    "禅杖": {"name": "禅杖", "value": 20, "distance": 100},
    "屠龙宝刀": {"name": "屠龙宝刀1", "value": 1000, "distance": 100}
}
shields = {
    None: {"name": "无", "value": 0},
    "盾牌": {"name": "盾牌", "value": 1},
    "测试-防御3": {"name": "测试2", "value": 3}
}
shoes = {
    None: {"name": "无", "value": 0},
    "鞋子": {"name": "鞋子", "value": 3},
    "测试-加速1": {"name": "测试1", "value": 1},
    "测试-加速3": {"name": "测试2", "value": 3}
}
energy_books = {
    None: {"name": "无", "value": 0},
    "魔法书": {"name": "魔法书", "value": 3}
}
# -药- -武器- -鞋子- -盾牌- -能量书- ~钩爪~ ~偷窃~ -五雷天罡法- ~无懈可击(被动)~


class drug:
    name = "药"
    value = 5

    def use(self, sender, *arg):
        sender.life += self.value
        sender.update()


class weapon:
    name = "武器_父类"
    value = "测试-伤害10"

    def use(self, sender, *arg):
        sender.weapon = self.value


class weapon_None(weapon):
    name = "不使用武器"
    value = None


class tlbd(weapon):
    name = "屠龙宝刀"
    value = "屠龙宝刀"


class cz(weapon):
    name = "禅杖"
    value = "禅杖"
    def use(self, sender, *arg):
        sender.weapon = self.value
        sender.buff.remove("chanzhang_cd")
        sender.buff.remove("chanzhang_cd_2")


class shoe:
    name = "鞋子"
    value = "鞋子"

    def use(self, sender, *arg):
        sender.shoe = self.value


class shoe_None(shoe):
    name = "不使用鞋子"
    value = None


class shield:
    name = "盾牌"
    value = "盾牌"

    def use(self, sender, *arg):
        sender.shield = self.value


class shield_None(shield):
    name = "不使用盾牌"
    value = None


class energy_book:
    name = "魔法书"
    value = "魔法书"

    def use(self, sender, *arg):
        sender.energy_book = self.value


class energy_book_None(energy_book):
    name = "不使用能量书"
    value = None

# 直线上没有障碍物：偷窃必须，五雷天罡法可以没有


class remote_attack:
    name = "远程攻击_父类"
    value = 1
    distance = 1

    def use(self, sender, target, *arg):
        route = (astar.astar(gameMapWithPlayers(sender, target),
                             sender.pos[0], sender.pos[1], target.pos[0], target.pos[1]))
        if route == list():
            error_hint="无法到达！"
            return True
        if len(route) > self.distance:
            error_hint="太远了！"
            return True
        target.damage(self.value)
        sender.update()


class wltg(remote_attack):
    name = "五雷天罡法"
    value = 30
    distance = 5

    def use(self, sender, target, *arg):
        if sender == target:
            error_hint="别对自己下手！"
            return True
        if getDistance(sender.pos, target.pos) > self.distance:
            error_hint="太远了！"
            return True
        target.damage(self.value)
        sender.update()


class gz(remote_attack):
    name = "钩爪"
    value = 10
    distance = 4

    def use(self, sender, target, *arg):
        global game_map
        if sender == target:
            error_hint="别对自己下手！"
            return True
        #error_hint="***几何什么的最烦了 钩爪拐弯就随他吧！"
        route = (astar.astar(gameMapWithPlayers(sender, target),
                             sender.pos[0], sender.pos[1], target.pos[0], target.pos[1]))
        if route == list():
            error_hint="无法到达！"
            return True
        distance= getDistance(sender.pos, target.pos)
        if distance>self.distance:
            error_hint="太远了！"
            return True
        target.damage(self.value)
        if distance == 1 or (distance == 2 and (abs(sender.pos[0]-target.pos[0]) == 1)):#即target在sender附近8格
            pass
        else:
            poss=posOnLine(game_map,sender.pos, target.pos)
            for i in poss:
                if game_map[i[0]][i[1]]!='0':
                    error_hint="直线上存在障碍物！"
                    return True
            target.pos=poss[0]
        sender.update()


class steal:
    name = "偷窃"
    value = 2
    distance = 5

    def use(self, sender, target, *arg):
        if sender == target:
            error_hint="别对自己下手！"
            return True
        route = (astar.astar(gameMapWithPlayers(sender, target),
                             sender.pos[0], sender.pos[1], target.pos[0], target.pos[1]))
        if route == list():
            error_hint="无法到达！"
            return True
        if len(route) > self.distance:
            error_hint="太远了！"
            return True
        i = 0
        if len(target.item) == 0:
            error_hint="他的背包什么都没有！"
            return True
        while len(target.item) != 0 and i < self.value:
            selected = random.choice(target.item)
            while selected.value == None:
                selected = random.choice(target.item)
            error_hint="* 你偷到了他的"+selected.name+"!"
            i += 1
            sender.item.append(selected)
            target.item.remove(selected)
            sender.update()
            target.update()


class kp:
    name = "看破"
    value = 1

    def use(self, *arg):
        error_hint="这张牌属于被动牌！"
        return True
