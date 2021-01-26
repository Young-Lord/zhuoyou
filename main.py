# https://www.jianshu.com/p/8e508c6a05ce
# 桌游_命令行
# -*- coding: UTF-8 -*-
import platform

import sys
import os
import importlib
import codecs
from items import *
from time import sleep
import astar
chesslist=["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
current_file = os.path.abspath(__file__)
current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(current_dir)
players=list()
special_blocks=list()
# importing characters
characters=os.listdir(os.path.join(os.getcwd(),"characters"))
characters=[i.replace(".py","") for i in characters if i[-3:]=='.py']
characters=["base",]+[i for i in characters if i!='base' and i!='cache_sum_characters']
sum_characters=codecs.open("cache_sum_characters.py","w", encoding='utf-8')
sum_characters.write("# 警告：本文件是在每次运行时自动生成的，修改此文件没有任何意义\r\nfrom items import *\r\n")
for i in characters:
        sum_characters.write("\r\n\r\n# Code from "+i+".py:\r\n")
        with codecs.open("characters/"+i+".py","r", encoding='utf-8') as f:
                sum_characters.write(f.read())
sum_characters.close()
from cache_sum_characters import *
#tester=Player()
#tester2=Player()
#tester.attack(tester2)
#print(tester2.life)

DEBUG = True


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
        for i in players:
                print(i.name,end="\t:")
                if i.alive:
                        print("生命 {};能量 {}".format(i.life,i.energy))
                else:
                        print("已死亡")
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
def gameMapWithPlayers(paichu=None):
        global game_map,players
        gen_map=[i[:] for i in game_map]
        for i in players:
                if i.alive and i!=paichu:
                        gen_map[i.pos[0]]=gen_map[i.pos[0]][:i.pos[1]]+"1"+gen_map[i.pos[0]][i.pos[1]+1:]
                        #same as gen_map[i.pos[0]][i.pos[1]]="1"
        return gen_map        

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

player_count = int(input("输入玩家数量："))
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
        if current_player_id==len(players):
                current_player_id=0
                turn+=1
        if len([i for i in players if i.alive])==0:
                print("？？？你们是怎么做到所有人都死亡的，能给我（作者）康康吗")
                running=False
        if len([i for i in players if i.alive])==1:
                print("游戏结束！\r\n玩家{} {}胜利！\r\n".format(players.index([i for i in players if i.alive][0])+1,[i for i in players if i.alive][0].name))
                running=False
        while not players[current_player_id].alive:
                current_player_id+=1
                if current_player_id==len(players):
                        current_player_id=0
                        turn+=1
        current_player=players[current_player_id]
        print("玩家{}操作".format(current_player_id+1))
        print("攻击：\"attack 玩家序号\"；移动：\"goto 坐标\"")
        command=input().split(' ',1)
        if len(command)!=2:
                continue
        if command[0]=='attack':
                if int(command[1])-1==current_player_id:
                        print("最好不要自刀，当然你要真想也可以...")
                        sleep(1 if not DEBUG else 0)
                current_player.attack(players[int(command[1])-1])
        elif command[0]=='goto':
                a,b=str2coordinates(command[1])
                if not isBlockEmpty(a,b):
                        print("此位置已被占用，请换一个位置。")
                        continue
                if current_player.pos==(a,b):
                        print("我 走 我 自 己")
                        continue
                route=(astar.astar(gameMapWithPlayers(current_player),current_player.pos[0],current_player.pos[1],a,b))
                if route==list():
                        print("无法到达！")
                        continue
                if len(route)>1000:#TODO add shoes
                        print("太远了！")
                        continue
                print("走法",end="：")
                for i in route:
                        print(i,end="")
                print("")
                current_player.pos=(a,b)
        current_player_id+=1
        cls()
        drawAll()
os.system("pause")
exit(0)
