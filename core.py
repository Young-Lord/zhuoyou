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

def inputJuese(avaibal,msg=""):
    rawstr=input(msg)
    try:
        val=int(rawstr)
    except ValueError:
        return inputJuese(avaibal,msg="角色非法，请重输")
    if val<=0 or val>len(characters):
        return inputJuese(avaibal,msg="角色非法，请重输")
    return val-1


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
    except ValueError:
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

characters = os.listdir(os.path.join(os.getcwd(), "characters"))
characters = [i.replace(".py", "") for i in characters if i[-3:] == '.py' and i!='base.py']
characters = [eval(i+"()") for i in characters]

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
    print("请选择你的角色：")
    for i in range(len(characters)):
        print("({}) {}".format(i+1,characters[i].name))
    juese=inputJuese(random.sample(characters,random_characters_new))
    juese=characters[juese]
    characters.remove(juese)
    current_player_id = juese
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
