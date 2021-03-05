# 警告：本文件是在每次运行时自动生成的，修改此文件没有任何意义
###############
#     Code from characters/base:
###############
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
    attack_range_add = 0
    actions_bak = {"attack": {"name": "攻击", "arg": "玩家序号", "count": 1},
                   "goto": {"name": "移动", "arg": "坐标", "count": 1},
                   "item": {"name": "查看背包", "arg": "", "count": -1},
                   "use": {"name": "使用", "arg": "物品ID (目标ID(如果有的话))", "count": -1},
                   "end": {"name": "结束回合", "arg": "", "count": 1}
                   }

    def init_custom(self):
        pass

    def __init__(self):
        self.actions = dict()
        self.item = list()
        self.buff = list()
        # WARNING: 每个可变对象（list,dict）等都必须在这里初始化，否则不同的实例会共享一个对象
        self.actions_bak = self.actions_bak.copy()
        for i in self.actions_bak.keys():
            self.actions_bak[i] = self.actions_bak[i].copy()
        self.life = self.max_life
        self.energy = self.max_energy
        self.init_custom()
        for i in self.actions_bak.keys():
            self.actions[i] = self.actions_bak[i].copy()

    def round(self):
        global random_step
        self.random_step = random_step
        global action_result
        action_result = ""
        print("="*10)
        for i in mopai(get_cards):
            self.item.append(i)
            print("你摸到了1张"+i.name+"！")
        print("="*10)
        while self.actions["end"]["count"]:
            if action_result != "":
                print("="*10)
                print(action_result)
                print("="*10)
            drawAll()
            action_result = ""
            self.action()
            cls()
        self.end_of_round()

    def action(self):
        global players, DEBUG, action_result
        for i in list(self.actions.keys()):
            if self.actions[i]["count"] != 0:
                print("{}：{} {}".format(
                    self.actions[i]["name"], i, self.actions[i]["arg"]))
        if self.actions["goto"]["count"] != 0:
            print("*你可以走的距离为："+str(self.random_step +
                                   shoes[self.shoe]["value"]+self.speed_add))
        max_card = (self.life+cards_limit-1)//cards_limit
        if len(self.item) > max_card:
            print("*回合结束时，你需要弃{}张牌".format(len(self.item)-max_card))
        command = input().split(' ', 1)
        if command[0].find("debug") != -1:  # handle debug commands
            self.debug_handle(command)
            return
        if command[0] not in list(self.actions.keys()):
            action_result = "未知命令"
            return
        if self.actions[command[0]]["count"] == 0:
            action_result = "你已经进行过此操作了！"
            return
        try:
            eval("self.{}_(command)".format(command[0]))
        except AttributeError:
            action_result = "你遇到bug了！告诉作者！（详情：命令对应的函数不存在）"
        except IndexError as e:
            if str(e) == "list index out of range":
                action_result = "命令参数过少！"

    def debug_handle(self,command):
        if command[0] == 'debug_eval':
            command = command[1]
            try:
                eval(command)
            except Exception as e:
                print("[debug_eval] 命令执行时出错。详情：")
                print(e)
        elif command[0] == 'debug_showbuff':
            print(self.buff)
        elif command[0] == 'debug_showitem':
            command = command[1].split()
            command[0] = int(command[0])
            target = players[command[0]-1]
            if target.item == list():
                action_result = "他的背包什么都没有！"
            else:
                action_result = "他的背包的物品为：\n"
                unnamed_id = 1
                for i in target.item:
                    action_result += str(unnamed_id)+' '
                    unnamed_id += 1
                    action_result += i.name+'\n'
        return

    def end_(self, command):
        self.actions[command[0]]["count"] -= 1

    def attack_(self, command):
        global action_result
        target = players[int(command[1])-1]
        if "chanzhang_cd_2" in self.buff and self.weapon == "禅杖":
            action_result = "禅杖冷却中..."
            self.actions[command[0]]["count"] -= 1
            return
        if target == self:
            self.attack(self)
            self.actions[command[0]]["count"] -= 1
            action_result = "最好不要自刀，当然你要真想也可以..."
            return
        route = (astar.astar(gameMapWithPlayers(self, target),
                             self.pos[0], self.pos[1], target.pos[0], target.pos[1]))
        if route == list():
            action_result = "无法到达！"
            return
        if "remote" in weapons[self.weapon].keys() and weapons[self.weapon]["remote"]:
            if getDistance_ou(self.pos, target.pos) > weapons[self.weapon]["distance"]+self.attack_range_add:
                action_result = "太远了！"
                return
            if not lineAvaibale(self.pos, target.pos):
                action_result = "与目标间存在障碍物！"
                return
        elif len(route) > weapons[self.weapon]["distance"]+self.attack_range_add:
            action_result = "太远了！"
            return
        self.attack(target)
        self.actions[command[0]]["count"] -= 1

    def goto_(self, command):
        global action_result
        try:
            command[1] = command[1].replace("(", "").replace(")", "")
            command[1] = command[1].replace(",", " ")
            a, b = [int(i) for i in command[1].split()]
        except:
            return
        if (not isBlockEmpty(a, b)) and self.pos != (a, b):
            action_result = "此位置已被占用，请换一个位置。"
            return
        if self.pos == (a, b):
            self.actions[command[0]]["count"] -= 1
            return
        route = (astar.astar(gameMapWithPlayers(
            self), self.pos[0], self.pos[1], a, b))
        if route == list():
            action_result = "无法到达！"
            return
        if len(route) > (self.random_step+shoes[self.shoe]["value"]+self.speed_add):
            action_result = "太远了！"
            return
        action_result = "走法：\n"
        for i in route:
            action_result += i
        self.pos = (a, b)
        self.actions[command[0]]["count"] -= 1

    def item_(self, command=None):
        global action_result
        if self.item == list():
            action_result = "你的背包什么都没有！"
        else:
            action_result = "你的背包的物品为：\n"
            unnamed_id = 1
            for i in self.item:
                action_result += str(unnamed_id)+' '
                unnamed_id += 1
                action_result += i.name+'\n'
            action_result = action_result[:-1]

    def use_(self, command):
        global action_result
        command = command[1].split()
        command[0] = int(command[0])
        if command[0] > len(self.item):
            action_result = "此ID的物品不存在！"
            return
        if len(command) >= 2:
            if int(command[1])-1 < 0:
                action_result = "玩家ID错误！"
                return
        return_value = True
        try:
            return_value = self.item[command[0] -
                                     1].use(self, players[int(command[1])-1])
        except IndexError:
            try:
                return_value = self.item[command[0]-1].use(self)
            except TypeError:
                action_result = "你没有指定目标！"
        if return_value != True:
            self.item.pop(command[0]-1)

    def attack(self, target):
        if self.weapon == "禅杖":
            self.buff.append("chanzhang_cd")
        hurt = target.damage((weapons[self.weapon]["value"] +
                              self.attack_add)*self.attack_percent//100)
        self.update()
        return hurt

    def damage(self, value):
        hurt = 0
        if ((value-shields[self.shield]["value"]-self.damage_minus)*self.damage_percent//100) > 0:
            hurt = round(
                (value-shields[self.shield]["value"] - self.damage_minus)*self.damage_percent//100)
        self.life -= hurt
        self.update()
        return hurt

    def update(self):
        if not self.alive:
            return
        if self.life <= 0:
            self.zhiliao()
        if self.life > self.max_life:
            self.life = self.max_life
        self.max_energy = self.max_energy_bak + \
            energy_books[self.energy_book]["value"]
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def zhiliao(self):
        # TODO:check
        global players,action_result
        myid = players.index(self)
        print("玩家{}({})失败了！".format(myid+1, self.name))
        print("你当前的血量为{}".format(self.life))
        if self.life <= 0:
            has_drug=True
            drug_index = -999
            while self.life<=0:
                drugs=[i for i in self.item if type(i)==drug]
                if len(drugs)==0:
                    break
                input_str = ""
                while input_str != "yes" and input_str != "no":
                    input_str = input("你要使用背包里的药吗？(yes/no)")
                if input_str == "yes":
                    self.life+=drugs[0].value
                    self.item.remove(drugs[0])
                    drugs.pop(0)
                else:
                    break
            for i in players:
                if self.life>=1:
                    break
                if (not i.alive) or i==self:
                    continue
                input_str=""
                end_round=False
                has_drug=False
                print("*玩家{}({})操作".format(players.index(i)+1,i.name))
                print("item:列出物品\nuse:对他用药\nend:结束操作")
                while not end_round and self.life<=0:
                    while input_str not in ["item","use","end"]:
                        input_str=input("输入你的操作：")
                    if input_str=="end":
                        end_round=True
                        cls()
                        break
                    if input_str=="item":
                        i.item_()
                        print(action_result)
                    if input_str=="use":
                        for k in i.item:
                            if k.name=="药":
                                has_drug=True
                                self.life+=k.value
                                i.item.remove(k)
                                if self.life>=1:
                                    break
                        if not has_drug:
                            print("你的背包里没有药！")
                        has_drug=False
                    input_str=""
                if self.life>=1:
                    break
                if end_round:
                    cls()
                    continue
        if self.life<=0:
            print("玩家{}({})彻底无了！".format(myid+1, self.name))
            self.alive = False
        else:
            self.update()

    def end_of_round(self):
        if not self.alive:
            return
        self.energy += 10
        for i in self.actions_bak.keys():
            self.actions[i] = self.actions_bak[i].copy()
        self.update()
        if "chanzhang_cd_2" in self.buff:
            self.buff = [i for i in self.buff if (
                i != "chanzhang_cd" and i != "chanzhang_cd_2")]
        if "chanzhang_cd" in self.buff:
            self.buff.append("chanzhang_cd_2")
        self.qipai()

    def qipai(self):
        global action_result
        max_card = (self.life+cards_limit-1)//cards_limit
        if len(self.item) <= max_card:
            return
        while len(self.item) > max_card:
            print("你还需要弃{}张牌".format(len(self.item)-max_card))
            self.item_()
            print("="*10+"\n"+action_result+"\n"+"="*10)
            removelist = -1
            realremove = list()
            while removelist == -1:
                rawstr = input().split()
                try:
                    removelist = [int(i) for i in rawstr]
                    for i in removelist:
                        if i <= 0 or i > len(self.item):
                            raise ValueError
                except ValueError:
                    removelist = -1
                    print("输入非法，请重输：", end="")
                    continue
                if len(removelist) > len(self.item)-max_card:
                    removelist = -1
                    print("你只能弃{}张牌，请重输：".format(
                        len(self.item)-max_card), end="")
            for i in removelist:
                realremove.append(self.item[i-1])
            for i in realremove:
                qipai.append(i)
                self.item.remove(i)
            realremove = list()
            cls()


###############
#     Code from characters/gaoqiu:
###############
class gaoqiu(Player):
    name="高俅"
    max_life=50
    max_energy=100
    attack_range_add=1
    def attack(self, target):
        if self.weapon == "禅杖":
            self.buff.append("chanzhang_cd")
        hurt = target.damage((weapons[self.weapon]["value"] +
                       self.attack_add)*self.attack_percent//100)
        self.life+=hurt
        self.update()
        return hurt

###############
#     Code from characters/likui:
###############
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


###############
#     Code from characters/try1:
###############
class try1(Player):
    name="测试工具人1"
    life = 10000
    def init_custom(self):
        self.actions_bak["zhudong1"]={"name": "回复", "arg": "", "count": 1}
    def zhudong1_(self,command):
        self.actions["zhudong1"]["count"]-=1
        self.life+=1000
        self.update()


###############
#     Code from characters/try2:
###############
class try2(Player):
    name="测试工具人2"


###############
#     Code from characters/try3:
###############
class try3(Player):
    name="测试工具人3"


###############
#     Code from inits:
###############
import platform
import sys
import os
import codecs
from time import sleep
import random
from math import sqrt, degrees, acos

import astar


chesslist = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
current_file = os.path.abspath(__file__)
current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(current_dir)
players = list()
special_blocks = list()
action_result = str()
qipai=list()

running = False
turn = 1
random_step=0
current_player_id = 0


print("你正在使用的系统是：{}".format(platform.platform()))
is_windows = (platform.platform().find("Windows")) != -1
print("Python版本：{}".format(platform.python_version()))
print("程序目录：{}".format(current_dir))


characters_file = [i for i in os.listdir(os.path.join(os.getcwd(), "characters")) if i[-3:] == '.py' and i!="tempCodeRunnerFile.py"]
characters=list()
for i in characters_file:
    with codecs.open("characters/"+i, "r", encoding='utf-8') as f:
        cont=f.read().replace("\xef\xbb\xbf", '')
        if cont.find("class") == -1:
            continue
        cont=cont.replace("(Player)","")
        name_1=cont.find("class ")+6
        name_2=cont.find(":")
        characters.append(cont[name_1:name_2])

characters = [i for i in characters if i!='Player']

error_list_ch=list()
for i in range(len(characters)):
    try:
        characters[i] = eval(characters[i]+"()")
    except NameError as ne:
        print("[警告]",ne,"请将警告信息发给作者")
        error_list_ch.append(characters[i])
for i in error_list_ch:
    characters.remove(i)



###############
#     Code from functions:
###############
class GameError(RuntimeError):
    pass


class MapError(GameError):
    pass


def exit(code: int):
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


def str2coordinates(s: str):
    try:
        s = s.replace("(", "").replace(")", "")
        s = s.replace(",", " ")
        a, b = [int(i) for i in s.split()]
        return (a, b)
    except:
        return inputCoordinates(msg="坐标非法，请重输：")


def inputCoordinates(msg: str = ""):
    rawstr = input(msg)
    return str2coordinates(rawstr)


def inputJuese(avaibale: list, msg: str = ""):
    rawstr = input(msg)
    try:
        val = int(rawstr)
    except ValueError:
        return inputJuese(avaibale, msg="角色非法，请重输：")
    if val <= 0 or val > len(characters):
        return inputJuese(avaibale, msg="角色非法，请重输：")
    return avaibale[val-1]


def drawAll():
    drawInfo()
    print("")
    drawPlayers()
    print("")
    drawMap()


def drawInfo():
    global turn, players, current_player_id
    print("* 第{}轮".format(turn), "玩家{}操作".format(current_player_id+1))
    print(
        "* 玩家数:{}/{}".format(len([i for i in players if i.alive]), len(players)))


def drawPlayers():
    global players
    display_index = 1
    for i in players:
        print("玩家"+str(display_index)+"  "+i.name, end="\t:")
        if i.alive:
            print("生命 {}/{};能量 {}/{}".format(i.life,
                                             i.max_life, i.energy, i.max_energy))
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
    except ValueError:
        return inputPlayerCount()


def getDistance_man(pos1: tuple, pos2: tuple):  # 曼哈顿距离
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])


def getDistance_ou(pos1: tuple, pos2: tuple):  # 欧几里得距离
    return sqrt(abs(pos1[0]-pos2[0])**2+abs(pos1[1]-pos2[1])**2)


def setblock(mapp: list, x: int, y: int, to):
    x = round(x)
    y = round(y)
    cchang = len(mapp[0])
    ckuan = len(mapp)
    if x >= ckuan:
        x = ckuan-1
    if y >= cchang:
        y = cchang-1
    mapp[x] = mapp[x][:y]+str(to)+mapp[x][y+1:]


def cal_ang(point_1, point_2, point_3):
    """
    根据三点坐标计算夹角
    :param point_1: 点1坐标
    :param point_2: 点2坐标
    :param point_3: 点3坐标
    :return: 返回任意角的夹角值，这里只是返回点2的夹角
    """
    a = sqrt((point_2[0]-point_3[0])*(point_2[0]-point_3[0]) +
             (point_2[1]-point_3[1])*(point_2[1] - point_3[1]))
    b = sqrt((point_1[0]-point_3[0])*(point_1[0]-point_3[0]) +
             (point_1[1]-point_3[1])*(point_1[1] - point_3[1]))
    c = sqrt((point_1[0]-point_2[0])*(point_1[0]-point_2[0]) +
             (point_1[1]-point_2[1])*(point_1[1] - point_2[1]))
    A = degrees(acos((a*a-b*b-c*c)/(-2*b*c)))
    B = degrees(acos((b*b-a*a-c*c)/(-2*a*c)))
    C = degrees(acos((c*c-a*a-b*b)/(-2*a*b)))
    return B


def posOnLine(mapp: list, a: tuple, b: tuple):
    result = list()
    chax = abs(a[0]-b[0])
    chay = abs(a[1]-b[1])
    if (chax == 0 or chay == 0) and chax+chay == 1:
        return list()
    if chax > chay:
        if a[0] > b[0]:
            a, b = b, a
    else:
        if a[1] > b[1]:
            a, b = b, a
    if a[0] == b[0]:
        return [(a[0], i) for i in range(a[1]+1, b[1])]
    k = (a[1]-b[1])/(a[0]-b[0])  # y=kx+d
    d = a[1]-a[0]*k
    # print("函数解析式：y={}x+{}".format(k, d))
    if chax > chay:
        # print("x>y")
        lasty = a[1]
        for i in range(a[0]+1, b[0]):  # i is x in function y=kx+d
            posx = i
            posy = round(k*i+d)
            res = [posx, posy]
            if lasty != posy:
                angle1 = round(cal_ang(a, (posx, posy-1), b))
                angle2 = round(cal_ang(a, (posx-1, posy), b))
                # print("angle1={};angle2={}".format(angle1, angle2))
                if angle1 == angle2:
                    # print("* branch#-1")
                    result.append([(posx, posy-1), (posx-1, posy)])
                if angle1 < angle2:
                    # print("* branch#1")
                    result.append((posx, posy-1))
                if angle1 > angle2:
                    result.append((posx-1, posy))
            result.append(tuple(res))
            lasty = posy
            # print("")
        posx = b[0]
        posy = round(k*b[0]+d)
        res = [posx, posy]
        if lasty != posy:
            angle1 = round(cal_ang(a, (posx, posy-1), b))
            angle2 = round(cal_ang(a, (posx-1, posy), b))
            # print("angle1={};angle2={}".format(angle1, angle2))
            if angle1 == angle2:
                # print("* branch#-1")
                result.append([(posx, posy-1), (posx-1, posy)])
            if angle1 < angle2:
                # print("* branch#1")
                result.append((posx, posy-1))
            if angle1 > angle2:
                # print("* branch#2")
                result.append((posx-1, posy))
    else:
        # print("y>x")
        lastx = a[0]
        for i in range(a[1]+1, b[1]):  # i is y in function y=kx+d
            posx = round((i-d)/k)
            posy = i
            res = [posx, posy]
            if lastx != posx:
                angle1 = round(cal_ang(a, (posx, posy-1), b))
                angle2 = round(cal_ang(a, (posx-1, posy), b))
                # print("angle1={};angle2={}".format(angle1, angle2))
                if angle1 == angle2:
                    # print("* branch#-1")
                    result.append([(posx, posy-1), (posx-1, posy)])
                if angle1 < angle2:
                    # print("* branch#1")
                    result.append((posx, posy-1))
                if angle1 > angle2:
                    # print("* branch#2")
                    result.append((posx-1, posy))
            result.append(tuple(res))
            lastx = posx
            # print("")
        posx = round((b[1]-d)/k)
        posy = b[1]
        res = [posx, posy]
        if lastx != posx:
            angle1 = round(cal_ang(a, (posx, posy-1), b))
            angle2 = round(cal_ang(a, (posx-1, posy), b))
            # print("angle1={};angle2={}".format(angle1, angle2))
            if angle1 == angle2:
                # print("* branch#-1")
                result.append([(posx, posy-1), (posx-1, posy)])
            if angle1 < angle2:
                # print("* branch#1")
                result.append((posx, posy-1))
            if angle1 > angle2:
                # print("* branch#2")
                result.append((posx-1, posy))
    return result


def lineAvaibale(a: tuple, b: tuple):
    global game_map
    poss = posOnLine(game_map, a, b)
    for i in poss:
        if type(i) == list:
            cur = False
            for j in i:
                if game_map[j[0]][j[1]] == '0':
                    cur = True
                    break
            if not cur:
                return False
        else:
            if game_map[i[0]][i[1]] != '0':
                return False
    return True


def getFangXiang(source: tuple, target: tuple):
    """
    返回一个形如(1,1)的元组，表示source元组x、y坐标的偏移
    """
    chax = abs(source[0]-target[0])
    chay = abs(source[1]-target[1])
    if chax == chay == 0:
        raise Exception("所给坐标错误！（反馈作者）")
    if chax == 0:
        return (0, 1) if (target[1]-source[1]) > 0 else (0, -1)
    if chay == 0:
        return (1, 0) if (target[0]-source[0]) > 0 else (-1, 0)
    if chax == chay == 1:
        return(target[0]-source[0], target[1]-source[1])
    k = (source[1]-target[1])/(source[0]-target[0])  # y=kx+d
    d = source[1]-source[0]*k
    #print("函数解析式：y={}x+{}".format(k, d))
    if chax > chay:
        # print("x>y")
        if source[0] > target[0]:
            step = -1
        else:
            step = 1
        for i in range(source[0], target[0], step):  # i is x in function y=kx+d
            if i == source[0]:
                continue
            return tuple([i-source[0], round(k*i+d)-source[1]])
    else:
        # print("y>x")
        if source[1] > target[1]:
            step = -1
        else:
            step = 1
        for i in range(source[1], target[1], step):  # i is y in function y=kx+d
            if i == source[1]:
                continue
            return tuple([round((i-d)/k)-source[0], i-source[1]])


def getFangXiangPos(source: tuple, target: tuple):
    fx = getFangXiang(source, target)
    return (source[0]+fx[0], source[1]+fx[1])

def mopai(count):
    global qipai,cards
    result_mopai=list()
    if len(cards) < count:
        for i in qipai:
            cards.append(i)
        qipai=list()
    for i in range(count):
        try:
            selected = random.choice(cards)
        except IndexError:
            print("[警告] 你牌堆里的牌设置的太少了")
            return result_mopai
        cards.remove(selected)
        result_mopai.append(selected)
    return result_mopai


###############
#     Code from items:
###############
import astar
import random

weapons = {
    None: {"name": "无", "value": 5, "distance": 1},
    "测试-伤害10": {"name": "测试1", "value": 10, "distance": 3},
    "测试-伤害15": {"name": "测试2", "value": 15, "distance": 5},
    "禅杖": {"name": "禅杖", "value": 20, "distance": 100},
    "屠龙宝刀": {"name": "屠龙宝刀", "value": 100, "distance": 100},
    "弓": {"name":"弓","value":8,"distance":6,"remote":True}
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
    "典籍": {"name": "典籍", "value": 30}
}
# -药- -武器- -鞋子- -盾牌- -能量书- ~钩爪~ ~偷窃~ -五雷天罡法- ~无懈可击(被动)~


class drug:
    name = "药"
    value = 50

    def use(self, sender, *arg):
        sender.life += self.value
        sender.update()


class weapon_base:
    name = "武器_父类"
    value = "测试-伤害10"

    def use(self, sender, *arg):
        sender.weapon = self.value
        self.use_custom(sender)
    def use_custom(self,sender):
        pass

class weapon_None(weapon_base):
    name = "不使用武器"
    value = None


class tlbd(weapon_base):
    name = "屠龙宝刀"
    value = "屠龙宝刀"


class bow(weapon_base):
    name = "弓"
    value = "弓"

class cz(weapon_base):
    name = "禅杖"
    value = "禅杖"

    def use_custom(self,sender):
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
    name = "典籍"
    value = "典籍"

    def use(self, sender, *arg):
        sender.energy_book = self.value


class energy_book_None(energy_book):
    name = "不使用典籍"
    value = None

# 直线上没有障碍物：偷窃必须，五雷天罡法可以没有


class remote_attack:
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


class wltg(remote_attack):
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


class gz(remote_attack):
    name = "钩爪"
    value = 10
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
            target.pos = getFangXiangPos(sender.pos,target.pos)
        sender.update()
        target.update()


class steal:
    name = "偷窃"
    value = 2
    distance = 5

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


###############
#     Code from game_config:
###############
# “#”号后面的内容没有实际作用，只用于说明
# GUI设置
screen_width = 640
screen_height = 480
bg_img_file = "./imgs/bg_img.png"

GRID_X_LEN = 10
GRID_Y_LEN = 12

REC_SIZE = 50

# 游戏设置
DEBUG = True  # 是否开启调试模式，True是“是”，False是“否”
random_steps = [1, 2, 3, 4, 5, 6]  # 可能随机得到的步数列表
random_characters=3#随机给出的角色数量
player_count = 2  # 固定的玩家数，如果要固定就将None改为玩家数，否则写None
get_cards = 2  # 每局摸牌数
cards_limit = 20 # 手牌上限每多少血增加1张，如：
# 当此值为20时，1~20血可持1张，21~40血可持2张，依此类推
cards_dict = {"drug": 5,
              "tlbd": 2,
              "gz": 2,
              "kp": 2,
              "bow": 2
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


###############
#     Code from core:
###############
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
random_characters_new=random_characters
for i in range(player_count):
    a, b = inputCoordinates("请输入玩家"+str(i+1)+"的坐标：")
    while not isBlockEmpty(a, b):
        a, b = inputCoordinates("此位置已被占用，请换一个位置：")
    if random_characters_new>len(characters):
        random_characters_new=len(characters)
    avaibale=random.sample(characters,random_characters_new)
    print("请选择你的角色：")
    for i in range(len(avaibale)):
        print("({}) {}".format(i+1,avaibale[i].name))
    juese=inputJuese(avaibale)
    characters.remove(juese)
    current_player = juese
    current_player.pos = (a, b)
    players.append(current_player)
    cls()
    drawMap()
cls()
print("#############")
print("#  游戏开始 #")
print("#############")
running=True
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


