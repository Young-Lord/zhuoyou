# 警告：本文件是在每次运行时自动生成的，修改此文件没有任何意义

#@# Code from base.py:

class Player:
    name = "默认角色"
    life = 80
    max_life = 80
    energy = 80
    max_energy = 80
    max_energy_bak = 80
    pos = (-1, -1)
    alive = True
    team = 0
    item = list()
    buff = list()  # 这是存各种技能的标记（如“义”）用的
    weapon = None
    shield = None
    shoe = None
    energy_book = None
    attack_add = 0  # 先add在percent
    attack_percent = 100
    damage_minus = 0
    damage_percent = 100
    speed_add = 0
    random_step = 0
    actions_bak = {"attack": {"name": "攻击", "arg": "玩家序号", "count": 1}, "goto": {"name": "移动", "arg": "坐标", "count": 1}, "item": {
        "name": "查看背包", "arg": "", "count": -1}, "use": {"name": "使用", "arg": "物品ID (目标ID(如果有的话))", "count": -1}, "end": {"name": "结束回合", "arg": "", "count": 1}}

    def __init__(self):
        self.init_custom()
        self.actions = dict()
        self.item = list()
        self.buff = list()
        # WARNING: 每个可变对象（list,dict）等都必须在这里初始化，否则不同的实例会共享一个对象
        for i in self.actions_bak.keys():
            self.actions[i] = self.actions_bak[i].copy()
        self.life = self.max_life
        self.energy = self.max_energy

    def round(self):
        global random_step
        self.random_step = random_step
        global error_hint
        error_hint = ""
        if len(cards) > get_cards:
            print("="*10)
            for i in range(get_cards):
                selected = random.choice(cards)
                print("你摸到了1张"+selected.name+"！")
                cards.remove(selected)
                self.item.append(selected)
            print("="*10)
        while self.actions["end"]["count"]:
            if error_hint != "":
                print("="*10)
                print(error_hint)
                print("="*10)
            drawAll()
            error_hint = ""
            self.action()
            cls()
        self.end_of_round()

    def action(self):
        global players, DEBUG, error_hint
        for i in list(self.actions.keys()):
            if self.actions[i]["count"] != 0:
                print("{}：{} {}".format(
                    self.actions[i]["name"], i, self.actions[i]["arg"]))
        if self.actions["goto"]["count"] != 0:
            print("你可以走的距离为："+str(self.random_step +
                                  shoes[self.shoe]["value"]+self.speed_add))
        command = input().split(' ', 1)
        if command[0].find("debug")!=-1:#handle debug commands
            if command[0] == 'debug_eval':
                command = command[1]
                eval(command)
            elif command[0] == 'debug_showbuff':
                print(self.buff)
            elif command[0] == 'debug_showitem':
                command = command[1].split()
                command[0] = int(command[0])
                target = players[command[0]-1]
                if target.item == list():
                    error_hint = "他的背包什么都没有！"
                else:
                    error_hint = "他的背包的物品为：\n"
                    unnamed_id = 1
                    for i in target.item:
                        error_hint += str(unnamed_id)+' '
                        unnamed_id += 1
                        error_hint += i.name+'\n'
            return
        if command[0] not in list(self.actions.keys()):
            error_hint = "未知命令"
            return
        if self.actions[command[0]]["count"] == 0:
            error_hint = "你已经进行过此操作了！"
            return
        try:
            eval("self.{}_(command)".format(command[0]))
        except AttributeError:
            print("你遇到bug了！告诉作者！")
    def end_(self,command):
        self.actions[command[0]]["count"] -= 1
    def attack_(self, command):
        global error_hint
        if "chanzhang_cd_2" in self.buff and self.weapon == "禅杖":
            error_hint = "禅杖冷却中..."
            self.actions[command[0]]["count"] -= 1
            return
        if players[int(command[1])-1] == self:
            self.attack(self)
            self.actions[command[0]]["count"] -= 1
            error_hint = "最好不要自刀，当然你要真想也可以..."
            return
        route = (astar.astar(gameMapWithPlayers(self, players[int(
            command[1])-1]), self.pos[0], self.pos[1], players[int(command[1])-1].pos[0], players[int(command[1])-1].pos[1]))
        if route == list():
            error_hint = "无法到达！"
            return
        if len(route) > weapons[self.weapon]["distance"]:
            error_hint = "太远了！"
            return
        self.attack(players[int(command[1])-1])
        self.actions[command[0]]["count"] -= 1

    def goto_(self, command):
        global error_hint
        try:
            command[1] = command[1].replace("(", "").replace(")", "")
            command[1] = command[1].replace(",", " ")
            a, b = [int(i) for i in command[1].split()]
        except:
            return
        if (not isBlockEmpty(a, b)) and self.pos != (a, b):
            error_hint = "此位置已被占用，请换一个位置。"
            return
        if self.pos == (a, b):
            self.actions[command[0]]["count"] -= 1
            return
        route = (astar.astar(gameMapWithPlayers(
            self), self.pos[0], self.pos[1], a, b))
        if route == list():
            error_hint = "无法到达！"
            return
        if len(route) > (self.random_step+shoes[self.shoe]["value"]+self.speed_add):
            error_hint = "太远了！"
            return
        error_hint = "走法：\n"
        for i in route:
            error_hint += i
        self.pos = (a, b)
        self.actions[command[0]]["count"] -= 1

    def item_(self, command):
        global error_hint
        if self.item == list():
            error_hint = "你的背包什么都没有！"
        else:
            error_hint = "你的背包的物品为：\n"
            unnamed_id = 1
            for i in self.item:
                error_hint += str(unnamed_id)+' '
                unnamed_id += 1
                error_hint += i.name+'\n'
            error_hint=error_hint[:-1]

    def use_(self, command):
        global error_hint
        command = command[1].split()
        command[0] = int(command[0])
        if command[0] > len(self.item):
            error_hint = "此ID的物品不存在！"
            return
        if len(command) >= 2:
            if int(command[1])-1 < 0:
                error_hint = "玩家ID错误！"
                return
        return_value = True
        try:
            return_value = self.item[command[0] -
                                     1].use(self, players[int(command[1])-1])
        except IndexError:
            try:
                return_value = self.item[command[0]-1].use(self)
            except TypeError:
                error_hint = "你没有指定目标！"
        if return_value != True:
            self.item.pop(command[0]-1)

    def attack(self, target):
        if self.weapon == "禅杖":
            self.buff.append("chanzhang_cd")
        target.damage((weapons[self.weapon]["value"] +
                       self.attack_add)*self.attack_percent//100)
        self.update()

    def damage(self, value):
        if ((value-shields[self.shield]["value"]-self.damage_minus)*self.damage_percent//100) > 0:
            self.life -= (value-shields[self.shield]["value"] -
                          self.damage_minus)*self.damage_percent//100
        self.update()

    def update(self):
        if self.life <= 0:
            self.alive = False
        if self.life > self.max_life:
            self.life = self.max_life
        self.max_energy = self.max_energy_bak + energy_books[self.energy_book]["value"]
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def end_of_round(self):
        self.energy += 10
        for i in self.actions_bak.keys():
            self.actions[i] = self.actions_bak[i].copy()
        self.update()
        if "chanzhang_cd_2" in self.buff:
            self.buff = [i for i in self.buff if (
                i != "chanzhang_cd" and i != "chanzhang_cd_2")]
        if "chanzhang_cd" in self.buff:
            self.buff.append("chanzhang_cd_2")
#@# Code from try1.py:

class tryyy(Player):
    life = 10000
    def init_custom(self):
        self.actions_bak["zhudong1"]={"name": "回复", "arg": "", "count": 1}
    def zhudong1_(self,command):
        self.actions["zhudong1"]["count"]-=1
        self.life+=1000
        self.update()
#@# Code from 李逵.py:

class likui(Player):
    name = "李逵"
    life = 8000
    max_life = 8000
    energy = 0
    max_energy = 0
    max_energy_bak = 0

    def init_custom(self):
        self.actions_bak["attack"]["count"] = 3

    def update(self):
        if self.life <= 0:
            self.alive = False
        self.energy = 0
        self.max_energy = 0


#@# Items:
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
        sender.buff = [i for i in sender.buff if (
            i != "chanzhang_cd" and i != "chanzhang_cd_2")]


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
        global error_hint
        route = (astar.astar(gameMapWithPlayers(sender, target),
                             sender.pos[0], sender.pos[1], target.pos[0], target.pos[1]))
        if route == list():
            error_hint = "无法到达！"
            return True
        if len(route) > self.distance:
            error_hint = "太远了！"
            return True
        target.damage(self.value)
        sender.update()


class wltg(remote_attack):
    name = "五雷天罡法"
    value = 30
    distance = 5

    def use(self, sender, target, *arg):
        global error_hint
        if sender == target:
            error_hint = "别对自己下手！"
            return True
        if getDistance_ou(sender.pos, target.pos) > self.distance:
            error_hint = "太远了！"
            return True
        target.damage(self.value)
        sender.update()


class gz(remote_attack):
    name = "钩爪"
    value = 10
    distance = 4

    def use(self, sender, target, *arg):
        global game_map
        global error_hint
        if sender == target:
            error_hint = "别对自己下手！"
            return True
        #error_hint="***几何什么的最烦了 钩爪拐弯就随他吧！"
        route = (astar.astar(gameMapWithPlayers(sender, target),
                             sender.pos[0], sender.pos[1], target.pos[0], target.pos[1]))
        if route == list():
            error_hint = "无法到达！"
            return True
        distance = getDistance_ou(sender.pos, target.pos)
        if distance > self.distance:
            error_hint = "太远了！"
            return True
        target.damage(self.value)
        # 即target在sender附近8格
        if distance == 1 or (distance == 2 and (abs(sender.pos[0]-target.pos[0]) == 1)):
            pass
        else:
            poss = posOnLine(game_map, sender.pos, target.pos)
            for i in poss:
                if game_map[i[0]][i[1]] != '0':
                    error_hint = "直线上存在障碍物！"
                    return True
            target.pos = poss[0]
        sender.update()


class steal:
    name = "偷窃"
    value = 2
    distance = 5

    def use(self, sender, target, *arg):
        global error_hint
        if sender == target:
            error_hint = "别对自己下手！"
            return True
        route = (astar.astar(gameMapWithPlayers(sender, target),
                             sender.pos[0], sender.pos[1], target.pos[0], target.pos[1]))
        if route == list():
            error_hint = "无法到达！"
            return True
        if len(route) > self.distance:
            error_hint = "太远了！"
            return True
        i = 0
        if len(target.item) == 0:
            error_hint = "他的背包什么都没有！"
            return True
        while len(target.item) != 0 and i < self.value:
            selected = random.choice(target.item)
            while selected.value == None:
                selected = random.choice(target.item)
            error_hint = "* 你偷到了他的"+selected.name+"!"
            i += 1
            sender.item.append(selected)
            target.item.remove(selected)
            sender.update()
            target.update()


class kp:
    name = "看破"
    value = 1

    def use(self, *arg):
        global error_hint
        error_hint = "这张牌属于被动牌！"
        return True


#@# Configs:
# “#”号后面的内容没有实际作用，只用于说明
# GUI设置
screen_width = 640
screen_height = 480
bg_img_file = "./imgs/bg_img.png"

GRID_X_LEN = 10
GRID_Y_LEN = 12

REC_SIZE = 50

# 游戏设置
random_steps = [1, 2, 3, 4, 5, 6]  # 这里是可能随机得到的步数列表
player_count = 2  # 这是固定的玩家数，如果要固定就将None改为玩家数，否则写None
get_cards = 2  # 每局摸牌数
DEBUG = True  # 是否开启调试模式，True是“是”，False是“否”
cards_dict = {"drug": 1,
              "tlbd": 2,
              "cz": 3,
              "shoe": 2,
              "shield": 2,
              "energy_book": 2,
              "wltg": 2,
              "steal": 2,
              "gz": 2,
              "kp": 2
              }
# 这是牌堆


# 不要修改下面的内容
if type(random_steps) == int:
    random_steps = list(random_steps)
cards = "["
for i in cards_dict.keys():
    cards += (i+"(),")*cards_dict[i]
cards += "]"
cards = eval(cards)


def set_map(changg, kuann):
    global GRID_X_LEN, GRID_Y_LEN, MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHTSCREEN_SIZE, screen
    GRID_X_LEN = changg
    GRID_Y_LEN = kuann
    MAP_WIDTH = GRID_X_LEN * REC_SIZE
    MAP_HEIGHT = GRID_Y_LEN * REC_SIZE
    SCREEN_WIDTH = MAP_WIDTH
    SCREEN_HEIGHT = MAP_HEIGHT
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(SCREEN_SIZE)


MAP_WIDTH = GRID_X_LEN * REC_SIZE
MAP_HEIGHT = GRID_Y_LEN * REC_SIZE


SCREEN_WIDTH = MAP_WIDTH
SCREEN_HEIGHT = MAP_HEIGHT
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


WHITE = (255, 255, 255)
NAVYBLUE = (60,  60, 100)
SKY_BLUE = (39, 145, 251)
BLACK = (0,   0,   0)
GREY = (127,   127,   127)
LIGHTYELLOW = (247, 238, 214)
RED = (255,   0,   0)
PURPLE = (255,   0, 255)
GOLD = (255, 215,   0)
GREEN = (0, 255,   0)


#@# Core code:
# https://www.jianshu.com/p/8e508c6a05ce
# 桌游_命令行
# -*- coding: UTF-8 -*-

import platform
import sys
import os
import codecs
from time import sleep
import random
from math import sqrt

import astar
chesslist = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
current_file = os.path.abspath(__file__)
current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(current_dir)
players = list()
special_blocks = list()
error_hint = str()


class GameError(RuntimeError):
    pass


class MapError(GameError):
    pass


def exit(code):
    print("\n**********")
    if code > 100:
        print("[致命错误] 退出代码"+str(code))
        print("**********\n")
        sys.exit(code)
    if code == 0:
        print("[正常退出]")
        print("**********\n")
        sys.exit(0)
    if code == 1:
        print("[程序错误] 退出代码1（请将报错截图提交给作者）")
        print("**********\n")
        sys.exit(1)
    else:
        print("[未知错误] 退出代码"+str(code)+"（请将报错截图提交给作者）")
        print("**********\n")
        sys.exit(code)


def cls():
    global is_windows
    global DEBUG
    if DEBUG:
        print("######cls#####")
        return
    if is_windows:
        cls_return_value_handler = os.system("cls")
    else:
        cls_return_value_handler = os.system("clear")


def str2coordinates(s):
    try:
        s = s.replace("(", "").replace(")", "")
        s = s.replace(",", " ")
        a, b = [int(i) for i in s.split()]
        return (a, b)
    except:
        return inputCoordinates(msg="坐标非法，请重输：")


def inputCoordinates(msg=""):
    rawstr = input(msg)
    return str2coordinates(rawstr)


def drawAll():
    drawInfo()
    print("")
    drawPlayers()
    print("")
    drawMap()


def drawInfo():
    global turn, players, current_player_id
    print("* 第{}轮".format(turn),"玩家{}操作".format(current_player_id+1))
    print(
        "* 玩家数:{}/{}".format(len([i for i in players if i.alive]), len(players)))


def drawPlayers():
    global players
    display_index = 1
    for i in players:
        print("玩家"+str(display_index)+"  "+i.name, end="\t:")
        if i.alive:
            print("生命 {};能量 {}".format(i.life, i.energy))
        else:
            print("已死亡")
        display_index += 1


def drawMap():
    global game_map, special_blocks
    display_map = [i[:] for i in game_map]
    for i in range(len(players)):
        if players[i].alive:
            setblock(display_map, players[i].pos[0],
                     players[i].pos[1], chesslist[i])
    for i in special_blocks:
        if display_map[i[0]][i[1]] == '0':
            setblock(display_map, i[0], i[1], 'O')
    display_map = [i.replace("0", "□").replace("1", "■") for i in display_map]
    for i in display_map:
        print(i)


def isBlockEmpty(a, b=None):
    global chang, kuan
    if a >= kuan or b >= chang:
        return False
    if type(a) == tuple or type(a) == list:
        a, b = a
    global players, game_map
    if game_map[a][b] == '1':
        return False
    for i in players:
        if i.alive:
            if i.pos == (a, b):  # type((a,b))==tuple
                return False
    return True


def gameMapWithPlayers(*paichu):
    global game_map, players
    paichu = list(paichu)
    gen_map = [i[:] for i in game_map]
    for i in players:
        if i.alive and (i not in paichu):
            setblock(gen_map, i.pos[0], i.pos[1], "1")
    return gen_map


def inputPlayerCount():
    try:
        return int(input("输入玩家数量："))
    except:
        return inputPlayerCount()


def getDistance_man(pos1, pos2):  # 曼哈顿距离
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])


def getDistance_ou(pos1, pos2):  # 欧几里得距离
    return sqrt(abs(pos1[0]-pos2[0])**2+abs(pos1[1]-pos2[1])**2)


def setblock(mapp, x, y, to):
    x = round(x)
    y = round(y)
    cchang = len(mapp[0])
    ckuan = len(mapp)
    if x >= ckuan:
        x = ckuan
    if y >= cchang:
        y = cchang
    mapp[x] = mapp[x][:y]+to+mapp[x][y+1:]


def posOnLine(mapp, a, b):
    result = list()
    chax = abs(a[0]-b[0])
    chay = abs(a[1]-b[1])
    k = (a[1]-b[1])/(a[0]-b[0])  # y=kx+d
    d = a[1]-a[0]*k
    #print("函数解析式：y={}x+{}".format(k, d))
    if chax > chay:
        # print("x>y")
        for i in range(a[0], b[0]):  # i is x in function y=kx+d
            if i == a[0]:
                continue
            result.append(tuple([round(i, k*i)+round(d)]))
    else:
        # print("y>x")
        for i in range(a[1], b[1]):  # i is y in function y=kx+d
            if i == a[1]:
                continue
            result.append(tuple([round((i-d)/k), round(i)]))
    return result


print("你正在使用的系统是：{}".format(platform.platform()))
is_windows = (platform.platform().find("Windows")) != -1
print("Python版本：{}".format(platform.python_version()))
print("程序目录：{}".format(current_dir))

try:
    map_file = open("map.txt", "r")
    game_map = [i.strip() for i in map_file.readlines()]
    map_file.close()
except IOError:
    print("[错误]请将map.txt放在程序目录下！")
    exit(101)

try:
    if len(game_map) <= 2:
        raise MapError
    else:
        if len(game_map[0]) <= 2:
            raise MapError
except MapError:
    print("[错误]地图过小！")
    exit(102)

chang = len(game_map[0])
kuan = len(game_map)

try:
    for i in game_map:
        if len(i) != chang:
            raise MapError
        for j in i:
            if j != '0' and j != '1':
                raise MapError
except MapError:
    print("[错误]map.txt格式错误！")
    exit(103)

if player_count == None:
    player_count = inputPlayerCount()
if player_count <= 1:
    print("[错误]玩家过少")
    exit(110)
if player_count > 10:
    print("[错误]玩家过多")
    exit(110)
void_block = 0
try:
    for i in game_map:
        void_block += i.count('0')
    if void_block < player_count:
        raise MapError
except MapError:
    print("[错误]地图可用空格数小于玩家数！")
    exit(104)

print("[信息]成功加载大小为{}x{}的地图".format(chang, kuan))
cls()
drawMap()
for i in range(player_count):
    a, b = inputCoordinates("请输入玩家"+str(i+1)+"的坐标：")
    while not isBlockEmpty(a, b):
        a, b = inputCoordinates("此位置已被占用，请换一个位置：")
    current_player_id = likui()
    current_player_id.pos = (a, b)
    players.append(current_player_id)
    cls()
    drawMap()
cls()
print("#############")
print("#  游戏开始 #")
print("#############")
running = True
turn = 1
current_player_id = 0
while running:
    random_step = random.choice(random_steps)
    current_player = players[current_player_id]
    current_player.random_step = random_step
    current_player.round()
    current_player_id += 1
    if current_player_id == len(players):
        current_player_id = 0
        turn += 1
    if len([i for i in players if i.alive]) == 0:
        print("？？？你们是怎么做到所有人都死亡的，能给我（作者）康康吗")
        running = False
        break
    if len([i for i in players if i.alive]) == 1:
        print("游戏结束！\r\n玩家{} {}胜利！\r\n".format(players.index(
            [i for i in players if i.alive][0])+1, [i for i in players if i.alive][0].name))
        running = False
        break
    while not players[current_player_id].alive:
        current_player_id += 1
        if current_player_id == len(players):
            current_player_id = 0
            turn += 1
os.system("pause")
exit(0)


