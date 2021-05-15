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

# 参数
infoObject = pygame.display.Info()
SCREEN_SIZE = (infoObject.current_w, infoObject.current_h)
REC_SIZE = 50
底栏高度 = 250
技能数 = 3
底栏各元素比例 = [96,20, 21, 20, 25,10]
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
MAP_RIGHTDOWN=(MAP_LEFT_SPACING+MAP_WIDTH,MAP_UP_SPACING+MAP_HEIGHT)
底栏上 = SCREEN_HEIGHT - 底栏高度
底栏各元素坐标 = [i*SCREEN_WIDTH//(sum(底栏各元素比例)) for i in 底栏各元素比例]
# CONFIG END


screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill([255, 255, 205])


def rect(color, place):
    pygame.draw.rect(screen, color, place)


def drawMap(clicked=(-1,-1)):
    pygame.draw.rect(screen, LIGHTYELLOW, pygame.Rect(
        MAP_LEFT_SPACING, MAP_UP_SPACING, MAP_WIDTH, MAP_HEIGHT))
    for x in range(GRID_X_LEN):
        for y in range(GRID_Y_LEN):
            if clicked==(x,y):
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
    if not((MAP_LEFT_SPACING<pos[0]<MAP_LEFT_SPACING+MAP_WIDTH)and(MAP_UP_SPACING<pos[1]<MAP_UP_SPACING+MAP_HEIGHT)):
        return (-1,-1)
    clicked=((pos[0]-MAP_LEFT_SPACING)//REC_SIZE,(pos[1]-MAP_UP_SPACING)//REC_SIZE)
    return clicked


#rect(FIGMA, (358, 0, 724, 89))
#rect(FIGMA, (0, 188, 89, 647))
#rect(FIGMA, (1351, 188, 89, 647))
# 其他玩家
drawMap()
# 地图
rect((0, 128, 0), (0, 底栏上, 底栏各元素坐标[0], 底栏高度))
# 背包
for i in range(4):
    rect([k+i*20 for k in GREY], (sum(底栏各元素坐标[0:1]), 底栏上+i*底栏高度//4, 底栏各元素坐标[1], 底栏高度//4+1))
# 装备
for i in range(技能数):
    rect([k+i*20 for k in NAVYBLUE], (sum(底栏各元素坐标[0:2]), 底栏上+i*底栏高度//技能数, 底栏各元素坐标[2], 底栏高度//技能数+1))
# 技能
rect(BLUE, (sum(底栏各元素坐标[0:3]), 底栏上, 底栏各元素坐标[3], 50))
rect(YELLOW, (sum(底栏各元素坐标[0:3]), 底栏上+50, 底栏各元素坐标[3], 200))
# 血量&buff
rect(GREEN, (sum(底栏各元素坐标[0:4]), 底栏上, 底栏高度, 底栏高度))
# 角色头像
rect((0xb1, 0x9d, 0x9d), (sum(底栏各元素坐标[0:4])+底栏高度, 底栏上, SCREEN_WIDTH-(sum(底栏各元素坐标[0:4])+底栏高度), 底栏高度))
# 结束按钮

pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked=getBlock(event.pos)
            drawMap(clicked=clicked)
            pygame.display.flip()
        if event.type == pygame.QUIT:  # QUIT用户请求程序关闭
            sys.exit()
