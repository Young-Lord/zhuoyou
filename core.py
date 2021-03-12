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
set_map(chang,kuan)
cls()
drawMap()
while True:
    for event in pygame.event.get():
        # 每次循环都会重新绘制屏幕
        if event.type==pygame.MOUSEMOTION:
            continue
        if event.type == pygame.QUIT:  # QUIT用户请求程序关闭
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.KEYDOWN:
            if event.unicode=='d':
                drawMap()
    pygame.display.flip()


random_characters_new = random_characters
for i in range(player_count):
    a, b = inputCoordinates("请输入玩家"+str(i+1)+"的坐标：")
    while not isBlockEmpty(a, b):
        a, b = inputCoordinates("此位置已被占用，请换一个位置：")
    if random_characters_new > len(characters):
        random_characters_new = len(characters)
    avaibale = random.sample(characters, random_characters_new)
    print("请选择你的角色：")
    for i in range(len(avaibale)):
        print("({}) {}".format(i+1, avaibale[i].name))
    juese = inputJuese(avaibale)
    characters.remove(juese)
    current_player = juese
    current_player.pos = (a, b)
    players.append(current_player)
>>>>>>> origin/master
    cls()
    drawMap()
cls()
print("#############")
print("#  游戏开始 #")
print("#############")
running = True
while running:
    random_step = random.choice(random_steps)
    current_player = players[current_player_id]
    current_player.random_step = random_step
    current_player.round()
    current_player_id += 1
    if current_player_id == player_count:
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
    while (not players[current_player_id].alive) or (players[current_player_id].disabled):
        if players[current_player_id].disabled:
            players[current_player_id].disabled = False
        current_player_id += 1
        if current_player_id == player_count:
            current_player_id = 0
            turn += 1
os.system("pause")
exit(0)
