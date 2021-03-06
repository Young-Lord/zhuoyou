import platform
import sys
import os
import codecs
from time import sleep
import random
from math import sqrt, degrees, acos

import astar


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
