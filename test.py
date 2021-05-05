import pygame
import sys

BLACK = [0, 0, 0]
GREY = [127, 127, 127]
YELLOW=[255,255,0]
BLUE=[0,0,255]
FIGMA = [196, 196, 196]  # 0xc4

pygame.init()
screen = pygame.display.set_mode((1440//2, 1024//2))  # 大小为1000px乘以600px
screen.fill([255, 255, 205])


def rect(color, place, fill=0):
    pygame.draw.rect(screen, color, [i/2 for i in place], fill)


rect(FIGMA, (358, 0, 724, 89))
rect(FIGMA,(0,188,89,647))
rect(FIGMA,(1351,188,89,647))
#其他玩家
rect(YELLOW,(309,289,822,446))
#地图
rect((0xb1,0x9d,0x9d),(1037,753,188,72))
#结束按钮
rect((0,128,0),(0,864,864,160))
#背包
for i in range(864,984+1,40):
    rect([k+(i-864)*20//40 for k in GREY],(864,i,208,40))
#装备
for i in range(864,944+1,80):
    rect([k+(i-864)*20//80 for k in GREY],(1072,i,208,80))
#技能
rect(BLUE,(1280,864,160,160))
#角色头像

pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # QUIT用户请求程序关闭
            sys.exit()
