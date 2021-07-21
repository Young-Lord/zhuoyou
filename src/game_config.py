with open("config.py.txt",encoding="utf-8") as f:
    exec(f.read())

# 不要修改下面的内容
if type(random_steps) == int:
    random_steps = list(random_steps)
cards = "["
for i in cards_dict.keys():
    cards += (i+"(),")*cards_dict[i]
cards += "]"
cards = eval(cards)


def set_map(changg, kuann):
    global GRID_X_LEN, GRID_Y_LEN, MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_SIZE
    GRID_X_LEN = changg
    GRID_Y_LEN = kuann
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
