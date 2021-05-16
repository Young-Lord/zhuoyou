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
    disabled = False
    actions_bak = {"attack": {"name": "攻击", "arg": "目标ID", "count": 1},
                   "goto": {"name": "移动", "arg": "坐标", "count": 1},
                   "item": {"name": "查看背包", "arg": "", "count": -1},
                   "use": {"name": "使用", "arg": "物品ID (目标ID(如果有的话))", "count": -1},
                   "zhuangbei": {"name": "装备界面", "arg": "", "count": -1},
                   "showzhuangbei": {"name": "查看他人装备", "arg": "目标ID", "count": -1},
                   "end": {"name": "结束回合", "arg": "", "count": 1}
                   }

    def init_custom(self):
        pass

    def __init__(self):
        self.weapon = weapon_None()
        self.shield = shield_None()
        self.shoe = shoe_None()
        self.energy_book = energy_book_None()
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
        global random_step, players
        self.random_step = random_step
        global action_result
        action_result = ""
        print("="*10)
        for i in mopai(get_cards):
            self.item.append(i)
            print("你摸到了1张"+i.name+"！")
        print("="*10)
        while self.actions["end"]["count"] and len([i for i in players if i.alive]) >= 2:
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
                                   self.shoe.value+self.speed_add))
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

    def debug_handle(self, command):
        if command[0] == 'debug_eval':
            command = command[1]
            try:
                eval(command)
            except Exception as e:
                print("[debug_eval] 命令执行时出错。详情：")
                print(e)
        elif command[0] == 'debug_exec':  # exec比eval强大，可以进行赋值等操作，但没有返回值
            command = command[1]
            try:
                exec(command)
            except Exception as e:
                print("[debug_exec] 命令执行时出错。详情：")
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
        try:
            target = players[int(command[1])-1]
        except ValueError:
            action_result = "命令非法！"
            return
        if "chanzhang_cd_2" in self.buff and type(self.weapon) == cz:
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
        if "remote" in type(self.weapon).__dict__ and self.weapon.remote:
            if getDistance_ou(self.pos, target.pos) > self.weapon.distance+self.attack_range_add:
                action_result = "太远了！"
                return
            if not lineAvaibale(self.pos, target.pos):
                action_result = "与目标间存在障碍物！"
                return
        elif len(route) > self.weapon.distance+self.attack_range_add:
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
            action_result = "命令非法！"
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
        if len(route) > (self.random_step+self.shoe.value+self.speed_add):
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
        try:
            command[0] = int(command[0])
            if len(command) >= 2:
                command[1] = int(command[1])
        except ValueError:
            action_result = "命令非法！"
            return
        if command[0] > len(self.item):
            action_result = "此ID的物品不存在！"
            return
        if len(command) >= 2:
            if command[1]-1 < 0:
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

    def use_by_content(self, content):
        return self.use_(["use", str(self.item.index(content)+1)])

    def attack(self, target):
        if type(self.weapon) == cz and "chanzhang_cd" not in self.buff:
            self.buff.append("chanzhang_cd")
        hurt = target.damage((self.weapon.value +
                              self.attack_add)*self.attack_percent//100)
        self.update()
        return hurt

    def damage(self, value):
        hurt = 0
        if ((value-self.shield.value-self.damage_minus)*self.damage_percent//100) > 0:
            hurt = round(
                (value-self.shield.value - self.damage_minus)*self.damage_percent//100)
        self.life -= hurt
        self.update()
        return hurt

    def update(self):
        if not self.alive:
            return
        if self.life <= 0:
            self.zhiliao()
        if not self.alive:
            return
        if self.life > self.max_life:
            self.life = self.max_life
        self.max_energy = self.max_energy_bak + \
            self.energy_book.value
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def zhiliao(self):
        global players, action_result
        myid = players.index(self)
        print("玩家{}({})失败了！".format(myid+1, self.name))
        print("你当前的血量为{}".format(self.life))
        if self.life <= 0:
            has_drug = True
            drug_index = -999
            while self.life <= 0:
                drugs = [i for i in self.item if type(i) == drug]
                if len(drugs) == 0:
                    break
                input_str = ""
                while input_str != "yes" and input_str != "no":
                    input_str = input("你要使用背包里的药吗？(yes/no)")
                if input_str == "yes":
                    self.life += drugs[0].value
                    self.item.remove(drugs[0])
                    drugs.pop(0)
                else:
                    break
            for i in players:
                if self.life >= 1:
                    break
                if (not i.alive) or i == self:
                    continue
                input_str = ""
                end_round = False
                has_drug = False
                print("*玩家{}({})操作".format(players.index(i)+1, i.name))
                print("item:列出物品\nuse:对他用药\nend:结束操作")
                while not end_round and self.life <= 0:
                    while input_str not in ["item", "use", "end"]:
                        input_str = input("输入你的操作：")
                    if input_str == "end":
                        end_round = True
                        cls()
                        break
                    if input_str == "item":
                        i.item_()
                        print(action_result)
                    if input_str == "use":
                        for k in i.item:
                            if k.name == "药":
                                has_drug = True
                                self.life += k.value
                                i.item.remove(k)
                                if self.life >= 1:
                                    break
                        if not has_drug:
                            print("你的背包里没有药！")
                        has_drug = False
                    input_str = ""
                if self.life >= 1:
                    break
                if end_round:
                    cls()
                    continue
        if self.life <= 0:
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
        if len([i for i in players if i.alive]) <= 1:
            return
        global action_result
        max_card = (self.life+cards_limit-1)//cards_limit
        if len(self.item) <= max_card:
            return
        while len(self.item) > max_card:
            print("你还需要弃{}张牌".format(len(self.item)-max_card))
            self.item_()
            print("="*10+"\n"+action_result+"\n"+"="*10)
            remove_list = -1
            realremove = list()
            while remove_list == -1:
                rawstr = input().split()
                try:
                    remove_list = [int(i) for i in rawstr]
                    for i in remove_list:
                        if i <= 0 or i > len(self.item):
                            raise ValueError
                except ValueError:
                    remove_list = -1
                    print("输入非法，请重输：", end="")
                    continue
                if len(remove_list) > len(self.item)-max_card:
                    remove_list = -1
                    print("你只能弃{}张牌，请重输：".format(
                        len(self.item)-max_card), end="")
            for i in remove_list:
                realremove.append(self.item[i-1])
            for i in realremove:
                qipai.append(i)
                self.item.remove(i)
            realremove = list()
            cls()

    def showzhuangbei_(self, command, in_code_call=False):
        global players, action_result, zhuangbei_list
        if in_code_call:
            target = command
        else:
            action_result = "他的装备栏为：\n"
            try:
                target = players[int(command[1])-1]
            except:
                action_result = "参数非法！"
                return
            if not 0 <= int(command[1])-1 < player_count:
                action_result = "参数非法！"
                return
        for i in zhuangbei_list:
            my_item = target.__getattribute__(zhuangbei_list[i]["code"])
            my_name = my_item.name
            my_value = my_item.value
            action_result += "({}) {}\t:{}(+{})".format(
                zhuangbei_list[i]["key"],
                i,
                my_name,
                my_value
            )
            if i == "武器":
                action_result += "(距离：{})".format(my_item.distance)
            action_result += '\n'
        action_result = action_result[:-1]
        if in_code_call:
            tmp = action_result[:]
            action_result = ""
            return tmp

    def zhuangbei_(self, command):
        # WARNING:要是变量更名了，此函数很可能会出错
        global zhuangbei_list, action_result
        operations = [zhuangbei_list[i]["key"] for i in zhuangbei_list]+["c"]
        while True:
            input_str = str()
            print("你的装备栏为：")
            print(self.showzhuangbei_(self, True))
            print("(c) 返回")
            while input_str not in operations:
                input_str = input("输入你的操作：")
            if input_str == "c":
                break
            current_type = list(zhuangbei_list.keys())[operations.index(input_str)]
            input_str = ""
            current_item = self.__getattribute__(zhuangbei_list[current_type]["code"])
            current_name = current_item.name
            current_value = current_item.value
            print("当前{}:{}(+{})".format(current_type,
                                        current_name, current_value), end="")
            if current_type == "武器":
                print("(距离：{})".format(current_item.distance), end="")
            print("\n", end="")
            avaibale_changes = [i for i in self.item if type(
                i).__base__.__name__ == zhuangbei_list[current_type]["code"]+"_base"]
            avaibale_values = [i.value for i in avaibale_changes]
            print("可用的选择：")
            print("(0) 返回")
            for i in range(len(avaibale_changes)):
                print("({}) {}:{}({:+})".format(i+1,
                                                avaibale_changes[i].name,
                                                avaibale_values[i],
                                                avaibale_values[i]-current_value), end="")
                if current_type == "武器":
                    print("(距离:{}({:+}))".format(
                        avaibale_changes[i].distance,
                        avaibale_changes[i].distance-current_item.distance), end="")
                print("\n", end="")
            while True:
                input_str = input("输入你的操作：")
                try:
                    input_str = int(input_str)
                except:
                    continue
                if 0 <= input_str <= len(avaibale_changes):
                    break
            if input_str == 0:
                continue
            else:
                if type(current_item).__name__.find("_None") != -1:
                    qipai.append(current_item)
                self.use_by_content(avaibale_changes[input_str-1])
