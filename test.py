import pygame
import sys

WHITE = (255, 255, 255)
NAVYBLUE = (60,  60, 100)
SKY_BLUE = (39, 145, 251)
BLACK = (0,   0,   0)
GREY = (127,   127,   127)
LIGHTYELLOW = (247, 238, 214)
RED = (255,   0,   0)
PURPLE = (255,   0, 255)
GOLD = (255, 215,   0)
GREEN = (0, 255,   0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
FIGMA = (196, 196, 196)  # 0xc9

pygame.init()
motioned = (-1, -1)
choosen = list()
font = pygame.font.Font("./HanSansNormal.ttc", 20)  # 思源黑体
font_small = pygame.font.Font("./HanSansNormal.ttc", 10)  # 思源黑体
# 参数
infoObject = pygame.display.Info()
SCREEN_SIZE = (infoObject.current_w, infoObject.current_h)
REC_SIZE = 50
底栏高度 = 250*infoObject.current_h//1080
技能数 = 3
底栏各元素比例 = [96, 20, 21, 20, 25, 10]
地图与底栏最小距离 = 20
背包物品数 = 6
# 参数


# CONFIG
game_map = [
    "000000010000000",
    "000111000111000",
    "000111000111000",
    "000111000111000",
    "000000000000000",
    "000000000000110",
    "000000000000110",
    "000001110000000",
    "000001110000000",
    "000001110000000"
]
chang = len(game_map[0])
GRID_X_LEN = chang
kuan = len(game_map)
GRID_Y_LEN = kuan
MAP_WIDTH = GRID_X_LEN * REC_SIZE
MAP_HEIGHT = GRID_Y_LEN * REC_SIZE
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
MAP_LEFTUP = ((SCREEN_WIDTH-MAP_WIDTH)//2, (SCREEN_HEIGHT-MAP_HEIGHT)//2)
MAP_LEFT_SPACING, MAP_UP_SPACING = MAP_LEFTUP
if MAP_UP_SPACING-底栏高度 < 地图与底栏最小距离:
    MAP_UP_SPACING -= (地图与底栏最小距离-(MAP_UP_SPACING-底栏高度))
    MAP_LEFTUP = (MAP_LEFT_SPACING, MAP_UP_SPACING)
MAP_RIGHTDOWN = (MAP_LEFT_SPACING+MAP_WIDTH, MAP_UP_SPACING+MAP_HEIGHT)
底栏上 = SCREEN_HEIGHT - 底栏高度
底栏各元素坐标 = [i*SCREEN_WIDTH//(sum(底栏各元素比例)) for i in 底栏各元素比例]
# CONFIG END


class try1():
    pos = (-1, -1)
    item = ['gz', 'kp', 'cz', 'wltg', 'kp', 'cz', 'wltg']
    weapon = "cz"
    shield = "shield"
    shoe = "shoe"
    energy_book = "energy_book_None"
    life = 40
    max_life = 100
    energy = 40
    max_energy = 100
    buff = ["义", "义"]


tester = try1()
zhuangbei_list = {"武器": {"code": "weapon", "key": "w"},
                  "护盾": {"code": "shield", "key": "h"},
                  "能量书": {"code": "energy_book", "key": "n"},
                  "鞋子": {"code": "shoe", "key": "s"}}


screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill([255, 255, 205])


def rect(color, place):
    pygame.draw.rect(screen, color, place)


def drawMap():
    global motioned, choosen
    pygame.draw.rect(screen, LIGHTYELLOW, pygame.Rect(
        MAP_LEFT_SPACING, MAP_UP_SPACING, MAP_WIDTH, MAP_HEIGHT))
    for x in range(GRID_X_LEN):
        for y in range(GRID_Y_LEN):
            if ('block', (x, y)) in choosen:
                color = RED
            elif motioned == (x, y):
                color = BLUE
            elif game_map[y][x] == '0':
                color = GOLD
            else:
                color = GREY
            pygame.draw.rect(screen, color, (x * REC_SIZE+MAP_LEFT_SPACING, y * REC_SIZE+MAP_UP_SPACING,
                                             REC_SIZE, REC_SIZE))

    for y in range(GRID_Y_LEN+1):
        # draw a horizontal line
        start_pos = (0+MAP_LEFT_SPACING, REC_SIZE * y+MAP_UP_SPACING)
        end_pos = (MAP_WIDTH+MAP_LEFT_SPACING, REC_SIZE * y+MAP_UP_SPACING)
        pygame.draw.line(screen, BLACK, start_pos, end_pos, 1)

    for x in range(GRID_X_LEN+1):
        # draw a horizontal line
        start_pos = (REC_SIZE * x+MAP_LEFT_SPACING, 0+MAP_UP_SPACING)
        end_pos = (REC_SIZE * x+MAP_LEFT_SPACING, MAP_HEIGHT+MAP_UP_SPACING)
        pygame.draw.line(screen, BLACK, start_pos, end_pos, 1)


def getBlock(pos):
    if not((MAP_LEFT_SPACING < pos[0] < MAP_LEFT_SPACING+MAP_WIDTH) and (MAP_UP_SPACING < pos[1] < MAP_UP_SPACING+MAP_HEIGHT)):
        return (-1, -1)
    motioned = ((pos[0]-MAP_LEFT_SPACING)//REC_SIZE,
                (pos[1]-MAP_UP_SPACING)//REC_SIZE)
    return motioned


def getCard(pos):
    global card_bg_WIDTH
    if not((0 < pos[0] < 底栏各元素坐标[0]) and (底栏上 < pos[1] < SCREEN_HEIGHT)):
        return "-1"  # 防止负数下标
    motioned = (pos[0]-0)//card_bg_WIDTH
    if motioned >= len(tester.item):
        return "-1"
    # 检查是否在点击区域内
    pos = (pos[0] % (底栏各元素坐标[0]//max(len(tester.item), 背包物品数)), pos[1]-底栏上)
    # 我也不知道这个max是什么意思，大概是因为卡牌能缩放吧（
    if pygame.transform.smoothscale(pygame.image.load("imgs/card_bg.png"), [card_bg_WIDTH, 底栏高度]).get_at(pos)[3] == 0:
        return "-1"
    return motioned


def drawBag():
    global 背包物品数, card_bg_WIDTH, motioned
    背包物品数_bak = 背包物品数
    if len(tester.item) > 背包物品数:
        背包物品数 = len(tester.item)
    rect((0, 128, 0), (0, 底栏上, 底栏各元素坐标[0], 底栏高度))
    for i in range(len(tester.item)):
        if ('card', i) in choosen:
            card_bg_path = "imgs/card_bg_select.png"
        elif i == motioned:
            card_bg_path = "imgs/card_bg_motion.png"
        else:
            card_bg_path = "imgs/card_bg.png"
        card_bg = pygame.image.load(card_bg_path)
        c_rect = card_bg.get_rect()
        card_bg_WIDTH = c_rect[2]*底栏高度//c_rect[3]
        card_bg = pygame.transform.smoothscale(card_bg, [card_bg_WIDTH, 底栏高度])
        if card_bg_WIDTH*len(tester.item) > 底栏各元素坐标[0]:
            card_bg_WIDTH = 底栏各元素坐标[0]//len(tester.item)
            card_bg = pygame.transform.smoothscale(
                card_bg, [card_bg_WIDTH, 底栏高度])
        screen.blit(card_bg, (0+i*底栏各元素坐标[0]//背包物品数, 底栏上))
    for i in range(len(tester.item)):
        item_image = pygame.image.load(
            'imgs/items/%s.png' % tester.item[i])  # TODO
        item_rect = item_image.get_rect()
        item_HEIGHT = item_rect[3]*card_bg_WIDTH//item_rect[2]
        item_image = pygame.transform.smoothscale(
            item_image, [card_bg_WIDTH, item_HEIGHT])
        up_spacing = (底栏高度-item_HEIGHT)//2+底栏上
        screen.blit(item_image, (0+i*(底栏各元素坐标[0])//背包物品数, up_spacing))
    背包物品数 = 背包物品数_bak


def drawEquiment():
    EACH_HEIGHT = 底栏高度//4
    for i in range(4):
        rect([k+i*20 for k in GREY], (sum(底栏各元素坐标[0:1]),
                                      底栏上+i*EACH_HEIGHT, 底栏各元素坐标[1], EACH_HEIGHT+1))
        cur_ind = list(zhuangbei_list.keys())[i]
        cur_code = zhuangbei_list[cur_ind]["code"]
        item_icon = pygame.image.load(
            "imgs/items/{}.png".format(tester.__getattribute__(cur_code)))
        item_rect = item_icon.get_rect()
        item_width = item_rect[2]*EACH_HEIGHT//item_rect[3]
        item_icon = pygame.transform.smoothscale(
            item_icon, [item_width, EACH_HEIGHT])
        screen.blit(item_icon, (sum(底栏各元素坐标[0:1]), 底栏上+i*EACH_HEIGHT))
        text = font.render('(+{})'.format(99), True, (0, 0, 0))
        screen.blit(text, (sum(底栏各元素坐标[0:1])+item_width, 底栏上+i*EACH_HEIGHT))
        if cur_ind=="武器":
            screen.blit(font_small.render('(距{})'.format(10), True, (10, 10, 10)),
            (sum(底栏各元素坐标[0:1])+item_width+text.get_size()[0], 底栏上+i*EACH_HEIGHT+text.get_size()[1]//2))


def drawAll():
    #rect(FIGMA, (358, 0, 724, 89))
    #rect(FIGMA, (0, 188, 89, 647))
    #rect(FIGMA, (1351, 188, 89, 647))
    # 其他玩家
    drawMap()
    # 地图
    drawBag()
    # 背包
    drawEquiment()
    # 装备
    for i in range(技能数):
        rect([k+i*20 for k in NAVYBLUE], (sum(底栏各元素坐标[0:2]),
                                          底栏上+i*底栏高度//技能数, 底栏各元素坐标[2], 底栏高度//技能数+1))
    # 技能
    rect(BLUE, (sum(底栏各元素坐标[0:3]), 底栏上, 底栏各元素坐标[3], 50))
    rect(YELLOW, (sum(底栏各元素坐标[0:3]), 底栏上+50, 底栏各元素坐标[3], 200))
    # 血量&buff
    rect(GREEN, (sum(底栏各元素坐标[0:4]), 底栏上, 底栏高度, 底栏高度))
    # 角色头像
    rect((0xb1, 0x9d, 0x9d), (sum(
        底栏各元素坐标[0:4])+底栏高度, 底栏上, SCREEN_WIDTH-(sum(底栏各元素坐标[0:4])+底栏高度), 底栏高度))
    # 结束按钮
    pygame.display.flip()


def handleMotion(pos):
    global motioned
    motioned = getBlock(pos)
    drawMap()
    pygame.display.flip()
    if motioned != (-1, -1):
        return
    motioned = getCard(pos)
    drawBag()
    pygame.display.flip()
    if motioned != "-1":
        return


def handlePress(pos, button=1):
    block = getBlock(pos)
    if block != (-1, -1):
        if ('block', block) in choosen:
            choosen.remove(('block', block))
        else:
            choosen.append(('block', block))
        drawMap()
        pygame.display.flip()
        return
    card = getCard(pos)
    if card != "-1":
        if ('card', card) in choosen:
            choosen.remove(('card', card))
        else:
            choosen.append(('card', card))
        drawBag()
        pygame.display.flip()
        return


drawAll()
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            handleMotion(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            handlePress(event.pos, button=event.button)
        if event.type == pygame.QUIT:  # QUIT用户请求程序关闭
            sys.exit()
