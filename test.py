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
    # print("*setblock "+str(x)+", "+str(y))
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
    chang = len(mapp[0])
    kuan = len(mapp)
    result = list()
    chax = abs(a[0]-b[0])
    chay = abs(a[1]-b[1])
    if (chax == 0 or chay == 0) and chax+chay == 1:
        return list()
    if a[1] > b[1]:
        a, b = b, a#保证a在左b在右
    if a[0] == b[0]:
        return [(a[0], i) for i in range(a[1]+1, b[1])]
    k = (a[1]-b[1])/(a[0]-b[0])  # y=kx+d
    d = a[1] - a[0] * k
    # print("函数解析式：y={}x+{}".format(k, d))
    if a[0]>b[0]:
        print("qingkuang 1")
        for i in range(-1, chang-1):
            if i < a[1] - 1 or i >= b[1]:
                continue  # 看不懂请画图理解
            cury = i+0.5
            curx = (cury-d)/k
            curx = round(curx * 1000) / 1000  # 防止精度问题
            if abs(curx - (floor(curx) + 0.5)) <= 0.0001:
                result.append([(round(curx - 0.5), round(cury - 0.5)),
                               (round(curx + 0.5), round(cury + 0.5))])
                result.append((round(curx + 0.5), round(cury - 0.5)))
                result.append((round(curx - 0.5), round(cury + 0.5)))
            else:
                result.append((round(curx), round(cury+0.5)))
        for i in range(-1, kuan - 1):
            if i < a[0] - 1 or i >= b[0]:
                continue  # 看不懂请画图理解
            curx = i + 0.5
            cury = curx*k+d
            cury = round(cury * 1000) / 1000  # 防止精度问题
            if abs(curx - (floor(curx) + 0.5)) <= 0.0001:
                result.append([(round(curx - 0.5), round(cury - 0.5)),
                               (round(curx + 0.5), round(cury + 0.5))])
                result.append((round(curx + 0.5), round(cury - 0.5)))
                result.append((round(curx - 0.5), round(cury + 0.5)))
            else:
                result.append((round(curx), round(cury+0.5)))
        final_result = list ()
        for i in result:
            if type(i) == tuple:
                if not (a[0] >= i[0] >= b[0] and a[1] <= i[1] <= b[1]):
                    continue
                if a == i or b == i:
                    continue
                final_result.append(i)
            else:
                cur_list=list()
                for j in i:
                    if not (a[0] >= j[0] >= b[0] and a[1] <= j[1] <= b[1]):
                        continue
                    if a == j or b == j:
                        continue
                    cur_list.append(j)
                if len(cur_list) == 1:
                    final_result.append(cur_list[0])
                elif len(cur_list) == 0:
                    continue
                else:
                    final_result.append(cur_list)
    else:
        print("qingkuang 2")
        for i in range(-1, chang-1):
            if i < a[1] - 1 or i >= b[1]:
                continue  # 看不懂请画图理解
            cury = i+0.5
            curx = (cury-d)/k
            curx = round(curx * 1000) / 1000  # 防止精度问题
            if abs(curx - (floor(curx) + 0.5)) <= 0.0001:
                result.append([(round(curx + 0.5), round(cury - 0.5)),
                               (round(curx - 0.5), round(cury + 0.5))])
                result.append((round(curx + 0.5), round(cury + 0.5)))
                result.append((round(curx - 0.5), round(cury - 0.5)))
            else:
                result.append((round(curx), round(cury+0.5)))
        for i in range(-1, kuan - 1):
            if i < a[0] - 1 or i >= b[0]:
                continue  # 看不懂请画图理解
            curx = i + 0.5
            cury = curx*k+d
            cury = round(cury * 1000) / 1000  # 防止精度问题
            if abs(curx - (floor(curx) + 0.5)) <= 0.0001:
                result.append([(round(curx + 0.5), round(cury - 0.5)),
                               (round(curx - 0.5), round(cury + 0.5))])
                result.append((round(curx - 0.5), round(cury - 0.5)))
                result.append((round(curx + 0.5), round(cury + 0.5)))
            else:
                result.append((round(curx), round(cury+0.5)))
        final_result = list ()
        for i in result:
            if type(i) == tuple:
                if not (a[0] <= i[0] <= b[0] and a[1] <= i[1] <= b[1]):
                    continue
                if a == i or b == i:
                    continue
                final_result.append(i)
            else:
                cur_list=list()
                for j in i:
                    if not (a[0] <= j[0] <= b[0] and a[1] <= j[1] <= b[1]):
                        continue
                    if a == j or b == j:
                        continue
                    cur_list.append(j)
                if len(cur_list) == 1:
                    final_result.append(cur_list[0])
                elif len(cur_list) == 0:
                    continue
                else:
                    final_result.append(cur_list)
        print(final_result)
    return final_result


def work(a, b):
    poss = posOnLine(map, a, b)
    for i in poss:
        if type(i) != list:
            setblock(i[0], i[1], 1)
        else:
            for k in i:
                setblock(k[0], k[1], "~")


while True:
    try:
        ss, dd = input("A:").split()
        setblock(int(ss), int(dd), "A")
        ff, gg = input("B:").split()
        setblock(int(ff), int(gg), "B")
        a = (int(ss), int(dd))
        b = (int(ff), int(gg))
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        print("错误，重输")
    work(a, b)
    draw()
