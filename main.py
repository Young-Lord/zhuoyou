# https://www.jianshu.com/p/8e508c6a05ce
# 桌游_命令行
# -*- coding: UTF-8 -*-
import platform

import sys
import os
import importlib
import codecs
from items import *
current_file = os.path.abspath(__file__)
current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(current_dir)
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


DEBUG = False


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


print("你正在使用的系统是：{}".format(platform.platform()))
is_windows = (platform.platform().find("Windows")) != -1
print("Python版本：{}".format(platform.python_version()))
print("程序目录：{}".format(current_dir))

try:
        map_file = open("map.txt", "r")
        map = [i.strip() for i in map_file.readlines()]
        map_file.close()
except IOError:
        print("[错误]请将map.txt放在程序目录下！")
        exit(101)

try:
        if len(map) <= 2:
                raise MapError
        else:
                if len(map[0]) <= 2:
                        raise MapError
except MapError:
        print("[错误]地图过小！")
        exit(102)

chang = len(map[0])
kuan = len(map)

try:
        for i in map:
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
        for i in map:
                void_block += i.count('0')
        if void_block < player_count:
                raise MapError
except MapError:
        print("[错误]地图可用空格数小于玩家数！")
        exit(104)

print("[信息]成功加载大小为{}x{}的地图".format(chang, kuan))
cls()
for i in map:
        print(i.replace("0", "□").replace("1", "■"))

exit(0)
