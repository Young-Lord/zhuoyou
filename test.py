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
REC_SIZE = 60
MAP_LEFT_SPACING = 130
MAP_UP_SPACING = 100
# (50,470,412)
# 参数


# CONFIG
game_map = [
    "0000000000",
    "0110000000",
    "0110001000",
    "0000000000"
]
chang = len(game_map[0])
GRID_X_LEN = chang
kuan = len(game_map)
GRID_Y_LEN = kuan
MAP_WIDTH = GRID_X_LEN * REC_SIZE
MAP_HEIGHT = GRID_Y_LEN * REC_SIZE

SCREEN_WIDTH = MAP_WIDTH+MAP_LEFT_SPACING*2
SCREEN_HEIGHT = MAP_HEIGHT+MAP_UP_SPACING*2
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_SIZE = (1440, 1024)
# print(SCREEN_SIZE)
# print((MAP_WIDTH,MAP_HEIGHT))
MAP_LEFTUP = (MAP_LEFT_SPACING, MAP_UP_SPACING)
# CONFIG END


screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill([255, 255, 205])


def rect(color, place):
    pygame.draw.rect(screen, color, place)


def drawMap():
    pygame.draw.rect(screen, LIGHTYELLOW, pygame.Rect(
        MAP_LEFT_SPACING, MAP_UP_SPACING, MAP_WIDTH, MAP_HEIGHT))
    for x in range(GRID_X_LEN):
        for y in range(GRID_Y_LEN):
            if game_map[y][x] == '0':
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
    

rect(FIGMA, (358, 0, 724, 89))
rect(FIGMA, (0, 188, 89, 647))
rect(FIGMA, (1351, 188, 89, 647))
# 其他玩家
drawMap()
#rect(YELLOW, (309, 289, 822, 446))
# 地图
rect((0xb1, 0x9d, 0x9d), (1037, 753, 188, 72))
# 结束按钮
rect((0, 128, 0), (0, 864, 864, 160))
# 背包
for i in range(864, 984+1, 40):
    rect([k+(i-864)*20//40 for k in GREY], (864, i, 208, 40))
# 装备
for i in range(864, 944+1, 80):
    rect([k+(i-864)*20//80 for k in GREY], (1072, i, 208, 80))
# 技能
rect(BLUE, (1280, 864, 160, 160))
# 角色头像

pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            print(event.pos)

        if event.type == pygame.QUIT:  # QUIT用户请求程序关闭
            sys.exit()
