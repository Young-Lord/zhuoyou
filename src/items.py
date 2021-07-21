import astar
import random

zhuangbei_list = {"武器": {"code": "weapon", "key": "w"},
                  "护盾": {"code": "shield", "key": "h"},
                  "能量书": {"code": "energy_book", "key": "n"},
                  "鞋子": {"code": "shoe", "key": "s"}}
# use in function zhuangbei_(),characters/base.py


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
    value = -1
    distance= -1

    def use(self, sender, *arg):
        if type(sender.weapon) != weapon_None:
            qipai.append(sender.weapon)
        sender.weapon = self
        self.use_custom(sender)

    def use_custom(self, sender):
        pass


class weapon_None(weapon_base):
    name = "无"
    value = 5
    distance=1


class tlbd(weapon_base):
    name = "屠龙宝刀"
    value = 100
    distance = 100


class bf(weapon_base):
    name = "板斧"
    value = 12
    distance=1


class pd(weapon_base):
    name = "朴刀"
    value = 10
    distance=2


class bow(weapon_base):
    name = "弓"
    value = 8
    distance = 6
    remote=True


class cz(weapon_base):
    name = "禅杖"
    value = 20
    distance = 2

    def use_custom(self, sender):
        sender.buff = [i for i in sender.buff if (
            i != "chanzhang_cd" and i != "chanzhang_cd_2")]


class shoe_base:
    name = "鞋子_父类"
    value = -1

    def use(self, sender, *arg):
        if type(sender.shoe) != shoe_None:
            qipai.append(sender.shoe)
        sender.shoe = self


class shoe_None(shoe_base):
    name = "无"
    value = 0


class shoe(shoe_base):
    name = "鞋子"
    value = 1


class shield_base:
    name = "盾牌_父类"
    value = -1

    def use(self, sender, *arg):
        if type(sender.shield) != shield_None:
            qipai.append(sender.shield)
        sender.shield = self


class shield(shield_base):
    name = "盾牌"
    value = 5


class shield_None(shield_base):
    name = "无"
    value = 0


class energy_book_base:
    name = "能量书_父类"
    value = -1

    def use(self, sender, *arg):
        if type(sender.energy_book) != energy_book_None:
            qipai.append(sender.energy_book)
        sender.energy_book = self


class energy_book:
    name = "典籍"
    value = 30


class energy_book_None(energy_book_base):
    name = "无"
    value = 0

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
        global action_result, zhuangbei_list
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
        selectable = []
        for i in zhuangbei_list:
            my_item = type(target.__getattribute__(zhuangbei_list[i]["code"])).__name__
            if my_item.find("None")==-1:
                selectable.append((i, my_item))
        if len(selectable)+len(target.item) == 0:
            action_result = "他什么都没有！"
            return True
        for i in target.item:
            selectable.append(("beibao", i))
        card_count = 0
        beibao = 1
        while len(selectable) != 0 and card_count < self.value:
            print("他的物品为：")
            for i in range(len(selectable)):
                if selectable[i][0] != "beibao":
                    print("({}) {}\t:{}".format(
                        i+1, selectable[i][0], selectable[i][1]))
                else:
                    print("({}) 背包物品{}\t:???".format(i+1, beibao))
                    beibao += 1
            select = ""
            while True:
                select = input("请选择你要偷窃的牌：")
                try:
                    if 1 <= int(select) <= len(selectable):
                        break
                except:
                    pass
            card_count += 1
            selected = selectable[int(select)-1]
            selectable.remove(selected)
            if selected[0] == "beibao":
                selected = selected[1]
                action_result = "* 你偷到了他的"+selected.name+"!"
                sender.item.append(selected)
                target.item.remove(selected)
            else:
                the_card = selected[1]
                exec("target.{}={}_None()".format(zhuangbei_list[selected[0]]["code"],zhuangbei_list[selected[0]]["code"]))
                sender.item.append(the_card)


class kp:
    name = "看破"
    value = 1

    def use(self, *arg):
        global action_result
        action_result = "这张牌属于被动牌！"
        return True
