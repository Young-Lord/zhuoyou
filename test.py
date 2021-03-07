from os import system
from math import *
map_bak = ["0000000000",
           "0000000000",
           "0000000000",
           "0000000000",
           "0000000000",
           "0000000000",
           "0000000000",
           "0000000000",
           "0000000000"]
map = [i[:] for i in map_bak]
chang = len(map_bak[0])
kuan = len(map_bak)


def cls():
    handleeeeeeee = system("cls")


def draw():
    global map
    # cls()
    display_map = [i.replace("0", "□").replace("1", "■") for i in map]
    for i in display_map:
        print(i)
        map = [i[:] for i in map_bak]


def setblock(x, y, to):
    global map
    x = round(x)
    y = round(y)
    if x >= kuan:
        x = kuan-1
    if y >= chang:
        y = chang-1
    #print("*setblock "+str(x)+", "+str(y))
    map[x] = map[x][:y]+str(to)+map[x][y+1:]


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
    #print("函数解析式：y={}x+{}".format(k, d))
    if chax > chay:
        print("x>y")
        lasty = a[1]
        for i in range(a[0]+1, b[0]):  # i is x in function y=kx+d
            posx = i
            posy = round(k*i+d)
            res = [posx, posy]
            if lasty != posy:
                angle1 = round(cal_ang(a, (posx, posy-1), b))
                angle2 = round(cal_ang(a, (posx-1, posy), b))
                print("angle1={};angle2={}".format(angle1, angle2))
                if angle1 == angle2:
                    print("* branch#-1")
                    result.append([(posx, posy-1), (posx-1, posy)])
                if angle1 < angle2:
                    print("* branch#1")
                    result.append((posx, posy-1))
                if angle1 > angle2:
                    print("* branch#2")
                    result.append((posx-1, posy))
            result.append(tuple(res))
            lasty = posy
            print("")
        posx = b[0]
        posy = round(k*b[0]+d)
        res = [posx, posy]
        if lasty != posy:
            angle1 = round(cal_ang(a, (posx, posy-1), b))
            angle2 = round(cal_ang(a, (posx-1, posy), b))
            print("angle1={};angle2={}".format(angle1, angle2))
            if angle1 == angle2:
                print("* branch#-1")
                result.append([(posx, posy-1), (posx-1, posy)])
            if angle1 < angle2:
                print("* branch#1")
                result.append((posx, posy-1))
            if angle1 > angle2:
                print("* branch#2")
                result.append((posx-1, posy))
    else:
        print("y>x")
        lastx = a[0]
        for i in range(a[1]+1, b[1]):  # i is y in function y=kx+d
            posx = round((i-d)/k)
            posy = i
            res = [posx, posy]
            if lastx != posx:
                angle1 = round(cal_ang(a, (posx, posy-1), b))
                angle2 = round(cal_ang(a, (posx-1, posy), b))
                print("angle1={};angle2={}".format(angle1, angle2))
                if angle1 == angle2:
                    print("* branch#-1")
                    result.append([(posx, posy-1), (posx-1, posy)])
                if angle1 < angle2:
                    print("* branch#1")
                    result.append((posx, posy-1))
                if angle1 > angle2:
                    print("* branch#2")
                    result.append((posx-1, posy))
            result.append(tuple(res))
            lastx = posx
            print("")
        posx = round((b[1]-d)/k)
        posy = b[1]
        res = [posx, posy]
        if lastx != posx:
            angle1 = round(cal_ang(a, (posx, posy-1), b))
            angle2 = round(cal_ang(a, (posx-1, posy), b))
            print("angle1={};angle2={}".format(angle1, angle2))
            if angle1 == angle2:
                print("* branch#-1")
                result.append([(posx, posy-1), (posx-1, posy)])
            if angle1 < angle2:
                print("* branch#1")
                result.append((posx, posy-1))
            if angle1 > angle2:
                print("* branch#2")
                result.append((posx-1, posy))
    return result


def work(a, b):
    poss = posOnLine(map, a, b)
    for i in poss:
        if type(i) != list:
            setblock(i[0], i[1], 1)
        else:
            for k in i:
                setblock(k[0], k[1], "~")


while True:
    ss, dd = input().split()
    setblock(int(ss), int(dd), "A")
    ff, gg = input().split()
    setblock(int(ff), int(gg), "B")
    a = (int(ss), int(dd))
    b = (int(ff), int(gg))
    work(a, b)
    draw()
