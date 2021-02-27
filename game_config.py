# “#”号后面的内容没有实际作用，只用于说明
# GUI设置
screen_width = 640
screen_height = 480
bg_img_file = "./imgs/bg_img.png"

GRID_X_LEN = 10
GRID_Y_LEN = 12

REC_SIZE = 50

# 游戏设置
DEBUG = True  # 是否开启调试模式，True是“是”，False是“否”
random_steps = [1, 2, 3, 4, 5, 6]  # 可能随机得到的步数列表
random_characters=3#随机给出的角色数量
player_count = 2  # 固定的玩家数，如果要固定就将None改为玩家数，否则写None
get_cards = 2  # 每局摸牌数
cards_limit = 20 # 手牌上限每多少血增加1张，如：
# 当此值为20时，1~20血可持1张，21~40血可持2张，依此类推
cards_dict = {"drug": 1,
              "tlbd": 2,
              "cz": 2,
              "shoe": 2,
              "shield": 2,
              "energy_book": 2,
              "wltg": 2,
              "steal": 2,
              "gz": 2,
              "kp": 2,
              "bow": 4
              }
# 这是牌堆


# 不要修改下面的内容
if type(random_steps) == int:
    random_steps = list(random_steps)
cards = "["
for i in cards_dict.keys():
    cards += (i+"(),")*cards_dict[i]
cards += "]"
cards = eval(cards)


def set_map(changg, kuann):
    global GRID_X_LEN, GRID_Y_LEN, MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHTSCREEN_SIZE, screen
    GRID_X_LEN = changg
    GRID_Y_LEN = kuann
    MAP_WIDTH = GRID_X_LEN * REC_SIZE
    MAP_HEIGHT = GRID_Y_LEN * REC_SIZE
    SCREEN_WIDTH = MAP_WIDTH
    SCREEN_HEIGHT = MAP_HEIGHT
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(SCREEN_SIZE)


MAP_WIDTH = GRID_X_LEN * REC_SIZE
MAP_HEIGHT = GRID_Y_LEN * REC_SIZE


SCREEN_WIDTH = MAP_WIDTH
SCREEN_HEIGHT = MAP_HEIGHT
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


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
