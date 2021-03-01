class Player:
    name = "默认角色"
    life = 80
    max_life = 80
    energy = 80
    max_energy = 80
    max_energy_bak = 80
    pos = (-1, -1)
    alive = True
    team = 0
    item = list()
    buff = list()  # 这是存各种技能的标记（如“义”）用的
    weapon = None
    shield = None
    shoe = None
    energy_book = None
    attack_add = 0  # 先add在percent
    attack_percent = 100
    damage_minus = 0
    damage_percent = 100
    speed_add = 0
    random_step = 0
    attack_range_add = 0
    actions_bak = {"attack": {"name": "攻击", "arg": "玩家序号", "count": 1}, "goto": {"name": "移动", "arg": "坐标", "count": 1}, "item": {
        "name": "查看背包", "arg": "", "count": -1}, "use": {"name": "使用", "arg": "物品ID (目标ID(如果有的话))", "count": -1}, "end": {"name": "结束回合", "arg": "", "count": 1}}
    def init_custom(self):
        pass

    def __init__(self):
        self.actions = dict()
        self.item = list()
        self.buff = list()
        # WARNING: 每个可变对象（list,dict）等都必须在这里初始化，否则不同的实例会共享一个对象
        self.actions_bak=self.actions_bak.copy()
        for i in self.actions_bak.keys():
            self.actions_bak[i] = self.actions_bak[i].copy()
        self.life = self.max_life
        self.energy = self.max_energy
        self.init_custom()
        for i in self.actions_bak.keys():
            self.actions[i] = self.actions_bak[i].copy()

    def round(self):
        global random_step
        self.random_step = random_step
        global error_hint
        error_hint = ""
        print("="*10)
        for i in mopai(get_cards):
            self.item.append(i)
            print("你摸到了1张"+i.name+"！")
        print("="*10)
        while self.actions["end"]["count"]:
            if error_hint != "":
                print("="*10)
                print(error_hint)
                print("="*10)
            drawAll()
            error_hint = ""
            self.action()
            cls()
        self.end_of_round()

    def action(self):
        global players, DEBUG, error_hint
        for i in list(self.actions.keys()):
            if self.actions[i]["count"] != 0:
                print("{}：{} {}".format(
                    self.actions[i]["name"], i, self.actions[i]["arg"]))
        if self.actions["goto"]["count"] != 0:
            print("*你可以走的距离为："+str(self.random_step +
                                  shoes[self.shoe]["value"]+self.speed_add))
        max_card = (self.life+cards_limit-1)//cards_limit
        if len(self.item)>max_card:
            print("*回合结束时，你需要弃{}张牌".format(len(self.item)-max_card))
        command = input().split(' ', 1)
        if command[0].find("debug")!=-1:#handle debug commands
            if command[0] == 'debug_eval':
                command = command[1]
                eval(command)
            elif command[0] == 'debug_showbuff':
                print(self.buff)
            elif command[0] == 'debug_showitem':
                command = command[1].split()
                command[0] = int(command[0])
                target = players[command[0]-1]
                if target.item == list():
                    error_hint = "他的背包什么都没有！"
                else:
                    error_hint = "他的背包的物品为：\n"
                    unnamed_id = 1
                    for i in target.item:
                        error_hint += str(unnamed_id)+' '
                        unnamed_id += 1
                        error_hint += i.name+'\n'
            return
        if command[0] not in list(self.actions.keys()):
            error_hint = "未知命令"
            return
        if self.actions[command[0]]["count"] == 0:
            error_hint = "你已经进行过此操作了！"
            return
        try:
            eval("self.{}_(command)".format(command[0]))
        except AttributeError:
            error_hint = "你遇到bug了！告诉作者！"
    def end_(self,command):
        self.actions[command[0]]["count"] -= 1
    def attack_(self, command):
        global error_hint
        target=players[int(command[1])-1]
        if "chanzhang_cd_2" in self.buff and self.weapon == "禅杖":
            error_hint = "禅杖冷却中..."
            self.actions[command[0]]["count"] -= 1
            return
        if target == self:
            self.attack(self)
            self.actions[command[0]]["count"] -= 1
            error_hint = "最好不要自刀，当然你要真想也可以..."
            return
        route = (astar.astar(gameMapWithPlayers(self,target),self.pos[0], self.pos[1], target.pos[0], target.pos[1]))
        if route == list():
            error_hint = "无法到达！"
            return
        if "remote" in weapons[self.weapon].keys() and weapons[self.weapon]["remote"]:
            if getDistance_ou(self.pos,target.pos)>weapons[self.weapon]["distance"]+self.attack_range_add:
                error_hint = "太远了！"
                return
            if not lineAvaibale(self.pos,target.pos):
                error_hint = "与目标间存在障碍物！"
                return
        elif len(route) > weapons[self.weapon]["distance"]+self.attack_range_add:
            error_hint = "太远了！"
            return
        self.attack(target)
        self.actions[command[0]]["count"] -= 1

    def goto_(self, command):
        global error_hint
        try:
            command[1] = command[1].replace("(", "").replace(")", "")
            command[1] = command[1].replace(",", " ")
            a, b = [int(i) for i in command[1].split()]
        except:
            return
        if (not isBlockEmpty(a, b)) and self.pos != (a, b):
            error_hint = "此位置已被占用，请换一个位置。"
            return
        if self.pos == (a, b):
            self.actions[command[0]]["count"] -= 1
            return
        route = (astar.astar(gameMapWithPlayers(
            self), self.pos[0], self.pos[1], a, b))
        if route == list():
            error_hint = "无法到达！"
            return
        if len(route) > (self.random_step+shoes[self.shoe]["value"]+self.speed_add):
            error_hint = "太远了！"
            return
        error_hint = "走法：\n"
        for i in route:
            error_hint += i
        self.pos = (a, b)
        self.actions[command[0]]["count"] -= 1

    def item_(self, command=None):
        global error_hint
        if self.item == list():
            error_hint = "你的背包什么都没有！"
        else:
            error_hint = "你的背包的物品为：\n"
            unnamed_id = 1
            for i in self.item:
                error_hint += str(unnamed_id)+' '
                unnamed_id += 1
                error_hint += i.name+'\n'
            error_hint=error_hint[:-1]

    def use_(self, command):
        global error_hint
        command = command[1].split()
        command[0] = int(command[0])
        if command[0] > len(self.item):
            error_hint = "此ID的物品不存在！"
            return
        if len(command) >= 2:
            if int(command[1])-1 < 0:
                error_hint = "玩家ID错误！"
                return
        return_value = True
        try:
            return_value = self.item[command[0] -
                                     1].use(self, players[int(command[1])-1])
        except IndexError:
            try:
                return_value = self.item[command[0]-1].use(self)
            except IOError:
                error_hint = "你没有指定目标！"
        if return_value != True:
            self.item.pop(command[0]-1)

    def attack(self, target):
        if self.weapon == "禅杖":
            self.buff.append("chanzhang_cd")
        hurt = target.damage((weapons[self.weapon]["value"] +
                       self.attack_add)*self.attack_percent//100)
        self.update()
        return hurt

    def damage(self, value):
        hurt=0
        if ((value-shields[self.shield]["value"]-self.damage_minus)*self.damage_percent//100) > 0:
            hurt = (value-shields[self.shield]["value"] -
                          self.damage_minus)*self.damage_percent//100
        self.life-=hurt
        self.update()
        return hurt

    def update(self):
        if self.life <= 0:
            self.alive = False
        if self.life > self.max_life:
            self.life = self.max_life
        self.max_energy = self.max_energy_bak + energy_books[self.energy_book]["value"]
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def end_of_round(self):
        self.energy += 10
        for i in self.actions_bak.keys():
            self.actions[i] = self.actions_bak[i].copy()
        self.update()
        if "chanzhang_cd_2" in self.buff:
            self.buff = [i for i in self.buff if (
                i != "chanzhang_cd" and i != "chanzhang_cd_2")]
        if "chanzhang_cd" in self.buff:
            self.buff.append("chanzhang_cd_2")
        self.qipai()
    def qipai(self):
        global error_hint
        max_card = (self.life+cards_limit-1)//cards_limit
        if len(self.item)<=max_card:
            return
        while len(self.item)>max_card:
            print("你还需要弃{}张牌".format(len(self.item)-max_card))
            self.item_()
            print("="*10+"\n"+error_hint+"\n"+"="*10)
            removelist=-1
            realremove=list()
            while removelist==-1:
                rawstr=input().split()
                try:
                    removelist=[int(i) for i in rawstr]
                    for i in removelist:
                        if i<=0 or i>len(self.item):
                            raise ValueError
                except ValueError:
                    removelist=-1
                    print("输入非法，请重输：",end="")
            for i in removelist:
                realremove.append(self.item[i-1])
            for i in realremove:
                qipai.append(i)
                self.item.remove(i)
            realremove=list()
            cls()
