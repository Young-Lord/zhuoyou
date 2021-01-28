#“#”号后面的内容没有实际作用，只用于说明
random_steps = [1,2,3,4,5,6]#这里是可能随机得到的步数列表
player_count = 2#这是固定的玩家数，如果要固定就将None改为玩家数，否则写None
get_cards = 2#每局摸牌数
DEBUG=False#是否开启调试模式，True是“是”，False是“否”
cards_dict={"drug":1,
            "tlbd":2,
            "shoe":2,
            "shield":2,
            "energy_book":2,
            "wltg":2,
            "steal":2,
            "gz":2,
            "kp":2
            }
#这是牌堆
            


#不要修改下面的内容
if type(random_steps)==int:
    random_steps=list(random_steps)
cards="["
for i in cards_dict.keys():
    cards+=(i+"(),")*cards_dict[i]
cards+="]"
cards=eval(cards)
