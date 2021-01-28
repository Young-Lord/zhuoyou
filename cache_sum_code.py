# 警告：本文件是在每次运行时自动生成的，修改此文件没有任何意义

#@# Code from base.py:

class Player:
    name="默认角色"
    life = 80
    max_life = 80
    energy = 80
    max_energy = 80
    max_energy_bak = 80
    pos = (-1, -1)
    alive = True
    team = 0
    item = list()
    buff = list() # 这是存各种技能的标记（如“义”）用的
    weapon = None
    shield=None
    shoe=None
    energy_book=None
    attack_add = 0 #先add在percent
    attack_percent = 100
    damage_minus = 0
    damage_percent = 100
    speed_add = 0
    random_step=0
    actions_bak={"attack":{"name":"攻击","arg":"玩家序号","count":1},"goto":{"name":"移动","arg":"坐标","count":1},"item":{"name":"查看背包","arg":"","count":-1},"use":{"name":"使用","arg":"物品ID (目标ID(如果有的话))","count":-1},"end":{"name":"结束回合","arg":"","count":1}}
    def __init__(self):
        self.actions=dict()
        self.item = list()
        buff = list()
        #WARNING: 每个可变对象（list,dict）等都必须在这里初始化，否则不同的实例会共享一个对象
        for i in self.actions_bak.keys():
            self.actions[i]=self.actions_bak[i].copy()
        self.life=self.max_life
        self.energy=self.max_energy
    def round(self):
        global random_step
        self.random_step=random_step
        print("="*10)
        if len(cards)>get_cards:
            for i in range(get_cards):
                selected=random.choice(cards)
                print("你摸到了1张"+selected.name+"！")
                cards.remove(selected)
                self.item.append(selected)
        while self.actions["end"]["count"]:
            self.action()
        self.end_of_round()
    def action(self):
        global players,DEBUG
        print("="*10)
        for i in list(self.actions.keys()):
            if self.actions[i]["count"]!=0:
                print("{}：{} {}".format(self.actions[i]["name"],i,self.actions[i]["arg"]))
        if self.actions["goto"]["count"]!=0:
            print("你可以走的距离为："+str(self.random_step+shoes[self.shoe]["value"]+self.speed_add))
        command=input().split(' ',1)
        cls()
        drawAll()
        print("="*10)
        if (command[0] not in list(self.actions.keys())) and command[0].find("debug")==-1:
            print("未知命令")
            return
        if command[0].find("debug")=="-1" and self.actions[command[0]]["count"]==0:
            print("你已经进行过此操作了！")
            return
        if command[0]=='attack':
            if players[int(command[1])-1]==self:
                self.attack(self)
                self.actions[command[0]]["count"]-=1
                print("最好不要自刀，当然你要真想也可以...")
                return
            route=(astar.astar(gameMapWithPlayers(self,players[int(command[1])-1]),self.pos[0],self.pos[1],players[int(command[1])-1].pos[0],players[int(command[1])-1].pos[1]))
            if route==list():
                print("无法到达！")
                return
            if len(route)>weapons[self.weapon]["distance"]:
                print("太远了！")
                return
            self.attack(players[int(command[1])-1])
            self.actions[command[0]]["count"]-=1
        elif command[0]=='goto':
            try:
                command[1]=command[1].replace("(","").replace(")","")
                command[1]=command[1].replace(","," ")
                a,b=[int(i) for i in command[1].split()]
            except:
                return
            if (not isBlockEmpty(a,b)) and self.pos!=(a,b):
                print("此位置已被占用，请换一个位置。")
                return
            if self.pos==(a,b):
                self.actions[command[0]]["count"]-=1
                return
            route=(astar.astar(gameMapWithPlayers(self),self.pos[0],self.pos[1],a,b))
            if route==list():
                print("无法到达！")
                return
            if len(route)>(self.random_step+shoes[self.shoe]["value"]+self.speed_add):
                print("太远了！")
                return self.action()
            print("走法",end="：")
            for i in route:
                print(i,end="")
            print("")
            self.pos=(a,b)
            self.actions[command[0]]["count"]-=1
            cls()
            drawAll()
        elif command[0]=='end':
            self.actions[command[0]]["count"]-=1
            return
        elif command[0]=='item':
            if self.item==list():
                print("你的背包什么都没有！")
            else:
                print("你的背包的物品为：")
                unnamed_id=1
                for i in self.item:
                    print(unnamed_id,end=" ")
                    unnamed_id+=1
                    print(i.name)
        elif command[0]=='use':
            command=command[1].split()
            command[0]=int(command[0])
            if command[0]>len(self.item):
                print("此ID的物品不存在！")
                return
            return_value=True
            try:
                return_value=self.item[command[0]-1].use(self,players[int(command[1])-1])
            except IndexError:
                try:
                    return_value=self.item[command[0]-1].use(self)
                except TypeError:
                    print("你没有指定目标！")
            if return_value!=True:
                self.item.pop(command[0]-1)
        elif command[0]=='debug_eval':
            command=command[1]
            eval(command)
        elif command[0]=='debug_showitem':
            command=command[1].split()
            command[0]=int(command[0])
            target=players[command[0]-1]
            if target.item==list():
                print("他的背包什么都没有！")
            else:
                print("他的背包的物品为：")
                unnamed_id=1
                for i in target.item:
                    print(unnamed_id,end=" ")
                    unnamed_id+=1
                    print(i.name)
        else:
            print("你遇到bug了！告诉作者！")
    def attack(self, target):
        target.damage((weapons[self.weapon]["value"]+self.attack_add)*self.attack_percent//100)
        self.update()
    def damage(self,value):
        if ((value-shields[self.shield]["value"]-self.damage_minus)*self.damage_percent//100)>0:
            self.life-=(value-shields[self.shield]["value"]-self.damage_minus)*self.damage_percent//100
        self.update()
    def update(self):
        if self.life<=0:
            self.alive=False
        if self.life>self.max_life:
            self.life=self.max_life
        self.max_energy=self.max_energy_bak+energy_books[self.energy_book]["value"]
        if self.energy>self.max_energy:
            self.energy=self.max_energy
    def end_of_round(self):
        self.energy+=10
        for i in self.actions_bak.keys():
            self.actions[i]=self.actions_bak[i].copy()
        self.update()
        


#@# Code from try1.py:

class tryyy:
    life = 1#@# Code from 李逵.py:

class likui(Player):
    life=80
    max_life=80
    energy=0
    max_energy=0
    max_energy_bak=0
    def update(self):
        if life<=0:
            self.alive=False
        energy=0
        max_energy=0
    actions_bak={"attack":{"name":"攻击","arg":"玩家序号","count":3},"goto":{"name":"移动","arg":"坐标","count":1},"info":{"name":"查看","arg":"","count":-1},"use":{"name":"使用","arg":"物品ID","count":-1},"end":{"name":"结束回合","arg":"","count":1}}

#@# Items:
import astar
import random

weapons={
None:{"name":"无","value":5,"distance":1},
"测试-伤害10":{"name":"测试1","value":10,"distance":3},
"测试-伤害15":{"name":"测试2","value":15,"distance":5},
"屠龙宝刀":{"name":"屠龙宝刀1","value":1000,"distance":100}
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
#-药- -武器- -鞋子- -盾牌- -能量书- ~钩爪~ ~偷窃~ -五雷天罡法- ~无懈可击(被动)~
class drug:
    name="药"
    value=5
    def use(self,sender,*arg):
        sender.life+=self.value
        sender.update()

class weapon:
    name="武器_父类"
    value="测试-伤害10"
    def use(self,sender,*arg):
        sender.weapon=self.value
class weapon_None(weapon):
    name="不使用武器"
    value=None
class tlbd(weapon):
    name="屠龙宝刀"
    value="屠龙宝刀"

class shoe:
    name="鞋子"
    value="鞋子"
    def use(self,sender,*arg):
        sender.shoe=self.value
class shoe_None(shoe):
    name="不使用鞋子"
    value=None

class shield:
    name="盾牌"
    value="盾牌"
    def use(self,sender,*arg):
        sender.shield=self.value
class shield_None(shield):
    name="不使用盾牌"
    value=None

class energy_book:
    name="魔法书"
    value="魔法书"
    def use(self,sender,*arg):
        sender.energy_book=self.value
class energy_book_None(energy_book):
    name="不使用能量书"
    value=None

#直线上没有障碍物：偷窃必须，五雷天罡法可以没有
class remote_attack:
    name="远程攻击_父类"
    value=1
    distance=1
    def use(self,sender,target,*arg):
        route=(astar.astar(gameMapWithPlayers(sender,target),sender.pos[0],sender.pos[1],target.pos[0],target.pos[1]))
        if route==list():
            print("无法到达！")
            return True
        if len(route)>self.distance:
            print("太远了！")
            return True
        target.damage(self.value)
        sender.update()
class wltg(remote_attack):
    name="五雷天罡法"
    value=30
    distance=5
    def use(self,sender,target,*arg):
        if sender==target:
            print("别对自己下手！")
            return True
        if getDistance(sender.pos,target.pos)>self.distance:
            print("太远了！")
            return True
        target.damage(self.value)
        sender.update()
class gz(remote_attack):
    name="钩爪"
    value=10
    distance=4
    def use(self,sender,target,*arg):
        if sender==target:
            print("别对自己下手！")
            return True
        print("***几何什么的最烦了 钩爪拐弯就随他吧！")
        route=(astar.astar(gameMapWithPlayers(sender,target),sender.pos[0],sender.pos[1],target.pos[0],target.pos[1]))
        if route==list():
            print("无法到达！")
            return True
        if len(route)>self.distance:
            print("太远了！")
            return True
        target.damage(self.value)
        sender.update()

class steal:
    name="偷窃"
    value=2
    distance=5
    def use(self,sender,target,*arg):
        if sender==target:
            print("别对自己下手！")
            return True
        route=(astar.astar(gameMapWithPlayers(sender,target),sender.pos[0],sender.pos[1],target.pos[0],target.pos[1]))
        if route==list():
            print("无法到达！")
            return True
        if len(route)>self.distance:
            print("太远了！")
            return True
        i=0
        if len(target.item)==0:
            print("他的背包什么都没有！")
            return True
        while len(target.item)!=0 and i<self.value:
            selected=random.choice(target.item)
            while selected.value==None:
                selected=random.choice(target.item)
            print("* 你偷到了他的"+selected.name+"!")
            i+=1
            sender.item.append(selected)
            target.item.remove(selected)
            sender.update()
            target.update()

class kp:
    name="看破"
    value=1
    def use(self,*arg):
        print("这张牌属于被动牌！")
        return True


#@# Configs:
#“#”号后面的内容没有实际作用，只用于说明
random_steps = [1,2,3,4,5,6]#这里是可能随机得到的步数列表
player_count = 2#这是固定的玩家数，如果要固定就将None改为玩家数，否则写None
get_cards = 2#每局摸牌数
DEBUG=True#是否开启调试模式，True是“是”，False是“否”
cards_dict={"drug":1,
            "tlbd":2,
            "shoe":2,
            "shield":2,
            "energy_book":2,
            "wltg":2,
            "steal":2,
            "gz":2,
            "kp":2
            }
#这是牌堆
            


#不要修改下面的内容
if type(random_steps)==int:
    random_steps=list(random_steps)
cards="["
for i in cards_dict.keys():
    cards+=(i+"(),")*cards_dict[i]
cards+="]"
cards=eval(cards)


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

import astar
chesslist=["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
current_file = os.path.abspath(__file__)
current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(current_dir)
players=list()
special_blocks=list()



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
        if DEBUG:
                print("######cls#####")
                return
        if is_windows:
                cls_return_value_handler = os.system("cls")
        else:
                cls_return_value_handler = os.system("clear")


def str2coordinates(s):
        try:
                s=s.replace("(","").replace(")","")
                s=s.replace(","," ")
                a,b=[int(i) for i in s.split()]
                return (a,b)
        except:
                return inputCoordinates(msg="坐标非法，请重输：")

def inputCoordinates(msg=""):
        rawstr=input(msg)
        return str2coordinates(rawstr)
def drawAll():
        drawInfo()
        print("")
        drawPlayers()
        print("")
        drawMap()
def drawInfo():
        global turn,players,current_player_id
        print("* 第{}轮".format(turn))
        print("* 玩家数:{}/{}".format(len([i for i in players if i.alive]),len(players)))
def drawPlayers():
        global players
        display_index=1
        for i in players:
                print("玩家"+str(display_index)+"  "+i.name,end="\t:")
                if i.alive:
                        print("生命 {};能量 {}".format(i.life,i.energy))
                else:
                        print("已死亡")
                display_index+=1
def drawMap():
        global game_map,special_blocks
        display_map=[i[:] for i in game_map]
        for i in range(len(players)):
                if players[i].alive:
                        display_map[players[i].pos[0]]=display_map[players[i].pos[0]][:players[i].pos[1]]+chesslist[i]+display_map[players[i].pos[0]][players[i].pos[1]+1:]
                        #same as display_map[players[i].pos[0]][players[i].pos[1]]=chr(ord('A')+i)
        for i in special_blocks:
                if display_map[i[0]][i[1]]=='0':
                        display_map[i[0]][i[1]]='O'
        display_map=[i.replace("0", "□").replace("1", "■") for i in display_map]
        for i in display_map:
                print(i)
def isBlockEmpty(a,b=None):
        global chang,kuan
        if a>=kuan or b>=chang:
                return False
        if type(a)==tuple or type(a)==list:
                a,b=a
        global players,game_map
        if game_map[a][b]=='1':
                return False
        for i in players:
                if i.alive:
                        if i.pos==(a,b):#type((a,b))==tuple
                                return False
        return True
def gameMapWithPlayers(*paichu):
        global game_map,players
        paichu=list(paichu)
        gen_map=[i[:] for i in game_map]
        for i in players:
                if i.alive and (i not in paichu):
                        gen_map[i.pos[0]]=gen_map[i.pos[0]][:i.pos[1]]+"1"+gen_map[i.pos[0]][i.pos[1]+1:]
                        #same as gen_map[i.pos[0]][i.pos[1]]="1"
        return gen_map
def inputPlayerCount():
        try:
                return int(input("输入玩家数量："))
        except:
                return inputPlayerCount()
def getDistance(pos1,pos2):
        if type(pos1)!=tuple and type(pos1)!=list:
                pos1=pos1.pos
                pos2=pos2.pos
        return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

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

if player_count==None:
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
        a,b=inputCoordinates("请输入玩家"+str(i+1)+"的坐标：")
        while not isBlockEmpty(a,b):
                a,b=inputCoordinates("此位置已被占用，请换一个位置：")
        current_player_id=Player()
        current_player_id.pos=(a,b)
        players.append(current_player_id)
        cls()
        drawMap()
cls()
print("#############")
print("#  游戏开始 #")
print("#############")
running=True
turn = 1
current_player_id=0
drawAll()
while running:
        random_step=random.choice(random_steps)
        current_player=players[current_player_id]
        print("玩家{}操作".format(current_player_id+1))
        current_player.random_step=random_step
        current_player.round()
        current_player_id+=1
        if current_player_id==len(players):
                current_player_id=0
                turn+=1
        if len([i for i in players if i.alive])==0:
                print("？？？你们是怎么做到所有人都死亡的，能给我（作者）康康吗")
                running=False
                break
        if len([i for i in players if i.alive])==1:
                print("游戏结束！\r\n玩家{} {}胜利！\r\n".format(players.index([i for i in players if i.alive][0])+1,[i for i in players if i.alive][0].name))
                running=False
                break
        while not players[current_player_id].alive:
                current_player_id+=1
                if current_player_id==len(players):
                        current_player_id=0
                        turn+=1
        cls()
        drawAll()
os.system("pause")
exit(0)


