import astar
import random

zhuangbei_list = {"武器": {"code": "weapon", "key": "w"},
                  "护盾": {"code": "shield", "key": "h"},
                  "能量书": {"code": "energy_book", "key": "n"},
                  "鞋子": {"code": "shoe", "key": "s"}}
# use in function zhuangbei_(),characters/base.py

weapons = {
    None: {"name": "空手", "value": 5, "distance": 1},
    "测试-伤害15": {"name": "测试2", "value": 15, "distance": 5},
    "禅杖": {"name": "禅杖", "value": 20, "distance": 100},
    "屠龙宝刀": {"name": "屠龙宝刀", "value": 100, "distance": 100},
    "板斧": {"name": "板斧", "value": 12, "distance": 1},
    "朴刀": {"name": "朴刀", "value": 10, "distance": 2},
    "弓": {"name": "弓", "value": 8, "distance": 6, "remote": True}
}
shields = {
    None: {"name": "无", "value": 0},
    "盾牌": {"name": "盾牌", "value": 5}
}
shoes = {
    None: {"name": "无", "value": 0},
    "鞋子": {"name": "鞋子", "value": 1},
    "测试-加速3": {"name": "测试2", "value": 3}
}
energy_books = {
    None: {"name": "无", "value": 0},
    "典籍": {"name": "典籍", "value": 30}
}
# -药- -武器- -鞋子- -盾牌- -能量书- ~钩爪~ ~偷窃~ -五雷天罡法- ~无懈可击(被动)~


class drug:
    name = "药"
    value = 10

    def use(self, sender, *arg):
        sender.life += self.value
        sender.update()


class mhy:
    name = "蒙汗药"
    value = -1

    def use(self, sender, target, *arg):
        global action_result, mhy_chance
        if sender == target:
            action_result = "别对自己下手！"
            return True
        if target.disabled:
            action_result = "他已经有这个标记了！（TODO：修改提示语）"
            return True
        if random.randint(1, 100) <= mhy_chance:  # 蒙汗药可以生效
            action_result = "蒙汗药使用成功！"
            target.disabled = True
        else:
            action_result = "蒙汗药使用失败！"


class weapon_base:
    name = "武器_父类"
    value = "测试-伤害15"

    def use(self, sender, *arg):
        if sender.weapon != None:
            qipai.append(sender.weapon)
        sender.weapon = self.value
        self.use_custom(sender)

    def use_custom(self, sender):
        pass


class weapon_None(weapon_base):
    name = "不使用武器"
    value = None


class tlbd(weapon_base):
    name = "屠龙宝刀"
    value = "屠龙宝刀"


class bf(weapon_base):
    name = "板斧"
    value = "板斧"


class pd(weapon_base):
    name = "朴刀"
    value = "朴刀"


class bow(weapon_base):
    name = "弓"
    value = "弓"


class cz(weapon_base):
    name = "禅杖"
    value = "禅杖"

    def use_custom(self, sender):
        sender.buff = [i for i in sender.buff if (
            i != "chanzhang_cd" and i != "chanzhang_cd_2")]


class shoe_base:
    name = "鞋子_父类"
    value = "测试-加速3"

    def use(self, sender, *arg):
        if sender.shoe != None:
            qipai.append(sender.shoe)
        sender.shoe = self.value


class shoe_None(shoe_base):
    name = "不使用鞋子"
    value = None


class shoe(shoe_base):
    name = "鞋子"
    value = "鞋子"


class shield_base:
    name = "盾牌_父类"
    value = "盾牌_父类"

    def use(self, sender, *arg):
        if sender.shield != None:
            qipai.append(sender.shield)
        sender.shield = self.value


class shield(shield_base):
    name = "盾牌"
    value = "盾牌"


class shield_None(shield_base):
    name = "不使用盾牌"
    value = None


class energy_book_base:
    name = "能量书_父类"
    value = "能量书_父类"

    def use(self, sender, *arg):
        if sender.energy_book != None:
            qipai.append(sender.energy_book)
        sender.energy_book = self.value


class energy_book_base:
    name = "典籍"
    value = "典籍"


class energy_book_None(energy_book_base):
    name = "不使用典籍"
    value = None

# 直线上没有障碍物：偷窃必须，五雷天罡法可以没有


class remote_attack_base:
    name = "远程攻击_父类"
    value = 1
    distance = 1

    def use(self, sender, target, *arg):
        global action_result
        route = (astar.astar(gameMapWithPlayers(sender, target),
                             sender.pos[0], sender.pos[1], target.pos[0], target.pos[1]))
        if route == list():
            action_result = "无法到达！"
            return True
        if len(route) > self.distance:
            action_result = "太远了！"
            return True
        target.damage(self.value)
        sender.update()


class wltg(remote_attack_base):
    name = "五雷天罡法"
    value = 30
    distance = 5

    def use(self, sender, target, *arg):
        global action_result
        if sender == target:
            action_result = "别对自己下手！"
            return True
        if getDistance_ou(sender.pos, target.pos) > self.distance:
            action_result = "太远了！"
            return True
        target.damage(self.value)
        sender.update()


class gz(remote_attack_base):
    name = "钩爪"
    value = 5
    distance = 4

    def use(self, sender, target, *arg):
        global game_map
        global action_result
        if sender == target:
            action_result = "别对自己下手！"
            return True
        #action_result="***几何什么的最烦了 钩爪拐弯就随他吧！"
        route = (astar.astar(gameMapWithPlayers(sender, target),
                             sender.pos[0], sender.pos[1], target.pos[0], target.pos[1]))
        if route == list():
            action_result = "无法到达！"
            return True
        distance = getDistance_ou(sender.pos, target.pos)
        if distance > self.distance:
            action_result = "太远了！"
            return True
        target.damage(self.value)
        # 即target在sender附近8格
        if distance == 1 or (distance == 2 and (abs(sender.pos[0]-target.pos[0]) == 1)):
            pass
        else:
            if not lineAvaibale(sender.pos, target.pos):
                action_result = "直线上存在障碍物！"
                return True
            target.pos = getFangXiangPos(sender.pos, target.pos)
        sender.update()
        target.update()


class steal:
    name = "偷窃"
    value = 1
    distance = 2

    def use(self, sender, target, *arg):
        global action_result
        if sender == target:
            action_result = "别对自己下手！"
            return True
        route = (astar.astar(gameMapWithPlayers(sender, target),
                             sender.pos[0], sender.pos[1], target.pos[0], target.pos[1]))
        if route == list():
            action_result = "无法到达！"
            return True
        if len(route) > self.distance:
            action_result = "太远了！"
            return True

        i = 0
        if len(target.item) == 0:
            action_result = "他的背包什么都没有！"
            return True
        while len(target.item) != 0 and i < self.value:
            selected = random.choice(target.item)
            while selected.value == None:
                selected = random.choice(target.item)
            action_result = "* 你偷到了他的"+selected.name+"!"
            i += 1
            sender.item.append(selected)
            target.item.remove(selected)
            sender.update()
            target.update()


class kp:
    name = "看破"
    value = 1

    def use(self, *arg):
        global action_result
        action_result = "这张牌属于被动牌！"
        return True
