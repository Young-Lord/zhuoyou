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
        print("\n\n\n\n\ntesttttttt")
    for i in range(count):
        try:
            selected = random.choice(cards)
        except IndexError:
            print("[警告] 你牌堆里的牌设置的太少了")
            return result_mopai
        cards.remove(selected)
        result_mopai.append(selected)
    return result_mopai
