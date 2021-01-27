#“#”号后面的内容没有实际作用，只用于说明
random_steps = [1,2,3,4,5,6]#这里是可能随机得到的步数列表
player_count = 2#这是固定的玩家数，如果要固定就将None改为玩家数，否则写None
DEBUG=False#是否开启调试模式，True是“是”，False是“否”


#不要修改下面的内容
if type(random_steps)==int:
    random_steps=list(random_steps)
