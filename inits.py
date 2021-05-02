import platform
import sys
import os
import codecs
from time import sleep
import random
from math import sqrt, degrees, acos
import astar

try:
    import pygame
except ModuleNotFoundError:
    print("你需要安装pygame模块！")
    os.system("pause")
    sys.exit(155)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("桌游")  # 标题
pygame.font.Font("./msyh.ttc", 20)  # 微软雅黑
bg_img = pygame.image.load(bg_img_file)  # 相对路径

chess_list = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
current_file = os.path.abspath(__file__)
current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(current_dir)
players = list()
special_blocks = list()
action_result = str()
qipai = list()

running = False
turn = 1
random_step = 0
current_player_id = 0


print("你正在使用的系统是：{}".format(platform.platform()))
is_windows = (platform.platform().find("Windows")) != -1
print("Python版本：{}".format(platform.python_version()))
print("程序目录：{}".format(current_dir))


characters_file = [i for i in os.listdir(os.path.join(
    os.getcwd(), "characters")) if i[-3:] == '.py' and i != "tempCodeRunnerFile.py"]
characters = list()
for i in characters_file:
    with codecs.open("characters/"+i, "r", encoding='utf-8') as f:
        cont = f.read().replace("\xef\xbb\xbf", '')
        if cont.find("class") == -1:
            continue
        cont = cont.replace("(Player)", "")
        name_1 = cont.find("class ")+6
        name_2 = cont.find(":")
        characters.append(cont[name_1:name_2])

characters = [i for i in characters if i != 'Player']

error_list_ch = list()
for i in range(len(characters)):
    try:
        characters[i] = eval(characters[i]+"()")
    except NameError as ne:
        print("[警告]", ne, "请将警告信息发给作者")
        error_list_ch.append(characters[i])
for i in error_list_ch:
    characters.remove(i)

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
set_map(chang,kuan)
cls()
