from os import system
map_bak=["0000000000", "0000000000", "0000000000", "0000000000", "0000000000", "0000000000", "0000000000", "0000000000", "0000000000"]
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
    x=round(x)
    y=round(y)
    if x>=kuan:
        x=kuan-1
    if y>=chang:
        y=chang-1
    #print("*setblock "+str(x)+", "+str(y))
    map[x] = map[x][:y]+str(to)+map[x][y+1:]


def posOnLine(mapp, a, b):
    result = list()
    chax = abs(a[0]-b[0])
    chay = abs(a[1]-b[1])
    if (chax==0 or chay==0) and chax+chay==1:
        return list()
    if chax>chay:
        if a[0]>b[0]:
            a,b=b,a
    else:
        if a[1]>b[1]:
            a,b=b,a
    k = (a[1]-b[1])/(a[0]-b[0])  # y=kx+d
    d = a[1]-a[0]*k
    print("函数解析式：y={}x+{}".format(k, d))
    if chax > chay:
        print("x>y")
        lasty=a[1]
        for i in range(a[0]+1, b[0]):  # i is x in function y=kx+d
            posx=i
            posy=round(k*i+d)
            res=[posx,posy]
            if lasty!=posy:
                xielv1 = (a[1]-posy-1)/(a[0]-posx)
                xielv2 = (a[1]-posy)/(a[0]-posx-1)
                print("abs1={};abs2={}".format(abs(xielv1-k),abs(xielv2-k)))
                if abs(xielv1-k) == abs(xielv2-k):
                    print("* branch#-1")
                    result.append([(posx,posy-1),(posx-1,posy)])
                if abs(xielv1-k) < abs(xielv2-k):
                    print("* branch#1")
                    result.append((posx,posy-1))
                if abs(xielv1-k) > abs(xielv2-k):
                    print("* branch#2")
                    result.append((posx-1,posy))
            result.append(tuple(res))
            lasty=posy
            print("")
        posx=b[0]
        posy=round(k*b[0]+d)
        res=[posx,posy]
        if lasty!=posy:
            xielv1 = (a[1]-posy-1)/(a[0]-posx)
            xielv2 = (a[1]-posy)/(a[0]-posx-1)
            if abs(xielv1-k) == abs(xielv2-k):
                print("* branch#-1")
                result.append([(posx,posy-1),(posx-1,posy)])
            print("abs1={};abs2={}".format(abs(xielv1-k),abs(xielv2-k)))
            if abs(xielv1-k) < abs(xielv2-k):
                print("* branch#1")
                result.append((posx,posy-1))
            if abs(xielv1-k) > abs(xielv2-k):
                print("* branch#2")
                result.append((posx-1,posy))
    else:
        print("y>x")
        lastx=a[0]
        for i in range(a[1]+1, b[1]):  # i is y in function y=kx+d
            posx=round((i-d)/k)
            posy=i
            res=[posx, posy]
            if lastx!=posx:
                xielv1 = (a[1]-posy-1)/(a[0]-posx)
                xielv2 = (a[1]-posy)/(a[0]-posx-1)
                print("abs1={};abs2={}".format(abs(xielv1-k),abs(xielv2-k)))
                if abs(xielv1-k) == abs(xielv2-k):
                    print("* branch#-1")
                    result.append([(posx,posy-1),(posx-1,posy)])
                if abs(xielv1-k) < abs(xielv2-k):
                    print("* branch#1")
                    result.append((posx,posy-1))
                if abs(xielv1-k) > abs(xielv2-k):
                    print("* branch#2")
                    result.append((posx-1,posy))
            result.append(tuple(res))
            lastx=posx
            print("")
        posx=round((b[1]-d)/k)
        posy=b[1]
        res=[posx,posy]
        if lastx!=posx:
            xielv1 = (a[1]-posy-1)/(a[0]-posx)
            xielv2 = (a[1]-posy)/(a[0]-posx-1)
            if abs(xielv1-k) == abs(xielv2-k):
                print("* branch#-1")
                result.append([(posx,posy-1),(posx-1,posy)])
            print("abs1={};abs2={}".format(abs(xielv1-k),abs(xielv2-k)))
            if abs(xielv1-k) < abs(xielv2-k):
                print("* branch#1")
                result.append((posx,posy-1))
            if abs(xielv1-k) > abs(xielv2-k):
                print("* branch#2")
                result.append((posx-1,posy))
    return result
            
def work(a,b):
    poss = posOnLine(map, a,b)
    for i in poss:
        if type(i)!=list:
            setblock(i[0],i[1],1)
        else:
            for k in i:
                setblock(k[0],k[1],"~")


while True:
    ss,dd=input().split()
    setblock(int(ss),int(dd),"A")
    ff,gg=input().split()
    setblock(int(ff),int(gg),"B")
    a = (int(ss), int(dd))
    b = (int(ff),int(gg))
    work(a, b)
    draw()
