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
    disabled=False
    actions_bak = {"attack": {"name": "攻击", "arg": "玩家序号", "count": 1},
                   "goto": {"name": "移动", "arg": "坐标", "count": 1},
                   "item": {"name": "查看背包", "arg": "", "count": -1},
                   "use": {"name": "使用", "arg": "物品ID (目标ID(如果有的话))", "count": -1},
                   "end": {"name": "结束回合", "arg": "", "count": 1}
                   }

    def init_custom(self):
        pass

    def __init__(self):
        self.actions = dict()
        self.item = list()
        self.buff = list()
        # WARNING: 每个可变对象（list,dict）等都必须在这里初始化，否则不同的实例会共享一个对象
        self.actions_bak = self.actions_bak.copy()
        for i in self.actions_bak.keys():
            self.actions_bak[i] = self.actions_bak[i].copy()
        self.life = self.max_life
        self.energy = self.max_energy
        self.init_custom()
        for i in self.actions_bak.keys():
            self.actions[i] = self.actions_bak[i].copy()

    def round(self):
        global random_step,players
        self.random_step = random_step
        global action_result
        action_result = ""
        print("="*10)
        for i in mopai(get_cards):
            self.item.append(i)
            print("你摸到了1张"+i.name+"！")
        print("="*10)
        while self.actions["end"]["count"] and len([i for i in players if i.alive]) >=2:
            if action_result != "":
                print("="*10)
                print(action_result)
                print("="*10)
            drawAll()
            action_result = ""
            self.action()
            cls()
        self.end_of_round()

    def action(self):
        global players, DEBUG, action_result
        for i in list(self.actions.keys()):
            if self.actions[i]["count"] != 0:
                print("{}：{} {}".format(
                    self.actions[i]["name"], i, self.actions[i]["arg"]))
        if self.actions["goto"]["count"] != 0:
            print("*你可以走的距离为："+str(self.random_step +
                                   shoes[self.shoe]["value"]+self.speed_add))
        max_card = (self.life+cards_limit-1)//cards_limit
        if len(self.item) > max_card:
            print("*回合结束时，你需要弃{}张牌".format(len(self.item)-max_card))
        command = input().split(' ', 1)
        if command[0].find("debug") != -1:  # handle debug commands
            self.debug_handle(command)
            return
        if command[0] not in list(self.actions.keys()):
            action_result = "未知命令"
            return
        if self.actions[command[0]]["count"] == 0:
            action_result = "你已经进行过此操作了！"
            return
        try:
            eval("self.{}_(command)".format(command[0]))
        except AttributeError:
            action_result = "你遇到bug了！告诉作者！（详情：命令对应的函数不存在）"
        except IndexError as e:
            if str(e) == "list index out of range":
                action_result = "命令参数过少！"

    def debug_handle(self,command):
        if command[0] == 'debug_eval':
            command = command[1]
            try:
                eval(command)
            except Exception as e:
                print("[debug_eval] 命令执行时出错。详情：")
                print(e)
        elif command[0] == 'debug_showbuff':
            print(self.buff)
        elif command[0] == 'debug_showitem':
            command = command[1].split()
            command[0] = int(command[0])
            target = players[command[0]-1]
            if target.item == list():
                action_result = "他的背包什么都没有！"
            else:
                action_result = "他的背包的物品为：\n"
                unnamed_id = 1
                for i in target.item:
                    action_result += str(unnamed_id)+' '
                    unnamed_id += 1
                    action_result += i.name+'\n'
        return

    def end_(self, command):
        self.actions[command[0]]["count"] -= 1

    def attack_(self, command):
        global action_result
        target = players[int(command[1])-1]
        if "chanzhang_cd_2" in self.buff and self.weapon == "禅杖":
            action_result = "禅杖冷却中..."
            self.actions[command[0]]["count"] -= 1
            return
        if target == self:
            self.attack(self)
            self.actions[command[0]]["count"] -= 1
            action_result = "最好不要自刀，当然你要真想也可以..."
            return
        route = (astar.astar(gameMapWithPlayers(self, target),
                             self.pos[0], self.pos[1], target.pos[0], target.pos[1]))
        if route == list():
            action_result = "无法到达！"
            return
        if "remote" in weapons[self.weapon].keys() and weapons[self.weapon]["remote"]:
            if getDistance_ou(self.pos, target.pos) > weapons[self.weapon]["distance"]+self.attack_range_add:
                action_result = "太远了！"
                return
            if not lineAvaibale(self.pos, target.pos):
                action_result = "与目标间存在障碍物！"
                return
        elif len(route) > weapons[self.weapon]["distance"]+self.attack_range_add:
            action_result = "太远了！"
            return
        self.attack(target)
        self.actions[command[0]]["count"] -= 1

    def goto_(self, command):
        global action_result
        try:
            command[1] = command[1].replace("(", "").replace(")", "")
            command[1] = command[1].replace(",", " ")
            a, b = [int(i) for i in command[1].split()]
        except:
            return
        if (not isBlockEmpty(a, b)) and self.pos != (a, b):
            action_result = "此位置已被占用，请换一个位置。"
            return
        if self.pos == (a, b):
            self.actions[command[0]]["count"] -= 1
            return
        route = (astar.astar(gameMapWithPlayers(
            self), self.pos[0], self.pos[1], a, b))
        if route == list():
            action_result = "无法到达！"
            return
        if len(route) > (self.random_step+shoes[self.shoe]["value"]+self.speed_add):
            action_result = "太远了！"
            return
        action_result = "走法：\n"
        for i in route:
            action_result += i
        self.pos = (a, b)
        self.actions[command[0]]["count"] -= 1

    def item_(self, command=None):
        global action_result
        if self.item == list():
            action_result = "你的背包什么都没有！"
        else:
            action_result = "你的背包的物品为：\n"
            unnamed_id = 1
            for i in self.item:
                action_result += str(unnamed_id)+' '
                unnamed_id += 1
                action_result += i.name+'\n'
            action_result = action_result[:-1]

    def use_(self, command):
        global action_result
        command = command[1].split()
        command[0] = int(command[0])
        if command[0] > len(self.item):
            action_result = "此ID的物品不存在！"
            return
        if len(command) >= 2:
            if int(command[1])-1 < 0:
                action_result = "玩家ID错误！"
                return
        return_value = True
        try:
            return_value = self.item[command[0] -
                                     1].use(self, players[int(command[1])-1])
        except IndexError:
            try:
                return_value = self.item[command[0]-1].use(self)
            except TypeError:
                action_result = "你没有指定目标！"
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
        hurt = 0
        if ((value-shields[self.shield]["value"]-self.damage_minus)*self.damage_percent//100) > 0:
            hurt = round(
                (value-shields[self.shield]["value"] - self.damage_minus)*self.damage_percent//100)
        self.life -= hurt
        self.update()
        return hurt

    def update(self):
        if not self.alive:
            return
        if self.life <= 0:
            self.zhiliao()
        if self.life > self.max_life:
            self.life = self.max_life
        self.max_energy = self.max_energy_bak + \
            energy_books[self.energy_book]["value"]
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def zhiliao(self):
        global players,action_result
        myid = players.index(self)
        print("玩家{}({})失败了！".format(myid+1, self.name))
        print("你当前的血量为{}".format(self.life))
        if self.life <= 0:
            has_drug=True
            drug_index = -999
            while self.life<=0:
                drugs=[i for i in self.item if type(i)==drug]
                if len(drugs)==0:
                    break
                input_str = ""
                while input_str != "yes" and input_str != "no":
                    input_str = input("你要使用背包里的药吗？(yes/no)")
                if input_str == "yes":
                    self.life+=drugs[0].value
                    self.item.remove(drugs[0])
                    drugs.pop(0)
                else:
                    break
            for i in players:
                if self.life>=1:
                    break
                if (not i.alive) or i==self:
                    continue
                input_str=""
                end_round=False
                has_drug=False
                print("*玩家{}({})操作".format(players.index(i)+1,i.name))
                print("item:列出物品\nuse:对他用药\nend:结束操作")
                while not end_round and self.life<=0:
                    while input_str not in ["item","use","end"]:
                        input_str=input("输入你的操作：")
                    if input_str=="end":
                        end_round=True
                        cls()
                        break
                    if input_str=="item":
                        i.item_()
                        print(action_result)
                    if input_str=="use":
                        for k in i.item:
                            if k.name=="药":
                                has_drug=True
                                self.life+=k.value
                                i.item.remove(k)
                                if self.life>=1:
                                    break
                        if not has_drug:
                            print("你的背包里没有药！")
                        has_drug=False
                    input_str=""
                if self.life>=1:
                    break
                if end_round:
                    cls()
                    continue
        if self.life<=0:
            print("玩家{}({})彻底无了！".format(myid+1, self.name))
            self.alive = False
        else:
            self.update()

    def end_of_round(self):
        if not self.alive:
            return
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
        global players
        if len([i for i in players if i.alive]) <=1:
            return
        global action_result
        max_card = (self.life+cards_limit-1)//cards_limit
        if len(self.item) <= max_card:
            return
        while len(self.item) > max_card:
            print("你还需要弃{}张牌".format(len(self.item)-max_card))
            self.item_()
            print("="*10+"\n"+action_result+"\n"+"="*10)
            removelist = -1
            realremove = list()
            while removelist == -1:
                rawstr = input().split()
                try:
                    removelist = [int(i) for i in rawstr]
                    for i in removelist:
                        if i <= 0 or i > len(self.item):
                            raise ValueError
                except ValueError:
                    removelist = -1
                    print("输入非法，请重输：", end="")
                    continue
                if len(removelist) > len(self.item)-max_card:
                    removelist = -1
                    print("你只能弃{}张牌，请重输：".format(
                        len(self.item)-max_card), end="")
            for i in removelist:
                realremove.append(self.item[i-1])
            for i in realremove:
                qipai.append(i)
                self.item.remove(i)
            realremove = list()
            cls()
