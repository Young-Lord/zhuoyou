# -*- coding: UTF-8 -*-

chesslist = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
current_file = os.path.abspath(__file__)
current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(current_dir)
players = list()
special_blocks = list()
error_hint = str()


print("你正在使用的系统是：{}".format(platform.platform()))
is_windows = (platform.platform().find("Windows")) != -1
print("Python版本：{}".format(platform.python_version()))
print("程序目录：{}".format(current_dir))

characters = os.listdir(os.path.join(os.getcwd(), "characters"))
characters = [i.replace(".py", "") for i in characters if i[-3:] == '.py' and i!='base.py' and i!='tempCodeR1unnerFile.py']
error_list_ch=list()
for i in range(len(characters)):
    try:
        characters[i] = eval(characters[i]+"()")
    except NameError as ne:
        print("[警告]",ne,"请将警告信息发给作者")
        error_list_ch.append(characters[i])
for i in error_list_ch:
    characters.remove(i)

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
    avaibal=random.sample(characters,random_characters_new)
    print("请选择你的角色：")
    for i in range(len(avaibal)):
        print("({}) {}".format(i+1,avaibal[i].name))
    juese=inputJuese(avaibal)
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
