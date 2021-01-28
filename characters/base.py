class Player:
    name="默认角色"
    life = 80
    max_life = 80
    energy = 80
    max_energy = 80
    max_energy_bak = 80
    pos = (-1, -1)
    alive = True
    team = 0
    item = list()
    buff = list() # 这是存各种技能的标记（如“义”）用的
    weapon = None
    shield=None
    shoe=None
    energy_book=None
    attack_add = 0 #先add在percent
    attack_percent = 100
    damage_minus = 0
    damage_percent = 100
    speed_add = 0
    random_step=0
    actions_bak={"attack":{"name":"攻击","arg":"玩家序号","count":1},"goto":{"name":"移动","arg":"坐标","count":1},"item":{"name":"查看背包","arg":"","count":-1},"use":{"name":"使用","arg":"物品ID (目标ID(如果有的话))","count":-1},"end":{"name":"结束回合","arg":"","count":1}}
    def __init__(self):
        self.actions=dict()
        self.item = list()
        buff = list()
        #WARNING: 每个可变对象（list,dict）等都必须在这里初始化，否则不同的实例会共享一个对象
        for i in self.actions_bak.keys():
            self.actions[i]=self.actions_bak[i].copy()
        self.life=self.max_life
        self.energy=self.max_energy
    def round(self):
        global random_step
        self.random_step=random_step
        if len(cards)>get_cards:
            for i in range(get_cards):
                selected=random.choice(cards)
                print("你摸到了1张"+selected.name+"！")
                cards.remove(selected)
                self.item.append(selected)
        while self.actions["end"]["count"]:
            #print("HELLO!")
            self.action()
        self.end_of_round()
    def action(self):
        global players,DEBUG
        for i in list(self.actions.keys()):
            if self.actions[i]["count"]!=0:
                print("{}：{} {}".format(self.actions[i]["name"],i,self.actions[i]["arg"]))
        if self.actions["goto"]["count"]!=0:
            print("你可以走的距离为："+str(self.random_step+shoes[self.shoe]["value"]+self.speed_add))
        command=input().split(' ',1)
        if (command[0] not in list(self.actions.keys())) and command[0].find("debug")=="-1":
            print("未知命令")
            return
        if command[0].find("debug")=="-1" and self.actions[command[0]]["count"]==0:
            print("你已经进行过此操作了！")
            return
        if command[0]=='attack':
            if players[int(command[1])-1]==self:
                self.attack(self)
                self.actions[command[0]]["count"]-=1
                print("最好不要自刀，当然你要真想也可以...")
                cls()
                drawAll()
                sleep(1 if not DEBUG else 0)
                return
            route=(astar.astar(gameMapWithPlayers(self,players[int(command[1])-1]),self.pos[0],self.pos[1],players[int(command[1])-1].pos[0],players[int(command[1])-1].pos[1]))
            if route==list():
                print("无法到达！")
                return
            if len(route)>weapons[self.weapon]["distance"]:
                print("太远了！")
                return
            self.attack(players[int(command[1])-1])
            self.actions[command[0]]["count"]-=1
            cls()
            drawAll()
        elif command[0]=='goto':
            try:
                command[1]=command[1].replace("(","").replace(")","")
                command[1]=command[1].replace(","," ")
                a,b=[int(i) for i in command[1].split()]
            except:
                return
            if (not isBlockEmpty(a,b)) and self.pos!=(a,b):
                print("此位置已被占用，请换一个位置。")
                return
            if self.pos==(a,b):
                self.actions[command[0]]["count"]-=1
                return
            route=(astar.astar(gameMapWithPlayers(self),self.pos[0],self.pos[1],a,b))
            if route==list():
                print("无法到达！")
                return
            if len(route)>(self.random_step+shoes[self.shoe]["value"]+self.speed_add):
                print("太远了！")
                return self.action()
            print("走法",end="：")
            for i in route:
                print(i,end="")
            print("")
            self.pos=(a,b)
            self.actions[command[0]]["count"]-=1
            cls()
            drawAll()
        elif command[0]=='end':
            self.actions[command[0]]["count"]-=1
            return
        elif command[0]=='item':
            if self.item==list():
                print("你的背包什么都没有！")
            else:
                print("你的背包的物品为：")
                unnamed_id=1
                for i in self.item:
                    print(unnamed_id,end=" ")
                    unnamed_id+=1
                    print(i.name)
        elif command[0]=='use':
            command=command[1].split()
            command[0]=int(command[0])
            if command[0]>len(self.item):
                print("此ID的物品不存在！")
                return
            return_value=True
            try:
                return_value=self.item[command[0]-1].use(self,players[int(command[1])-1])
            except IndexError:
                try:
                    return_value=self.item[command[0]-1].use(self)
                except TypeError:
                    print("你没有指定目标！")
            if return_value!=True:
                self.item.pop(command[0]-1)
        elif command[0]=='debug_eval':
            command=command[1]
            eval(command)
        elif command[0]=='debug_showitem':
            command=command[1].split()
            command[0]=int(command[0])
            target=players[command[0]-1]
            if target.item==list():
                print("他的背包什么都没有！")
            else:
                print("他的背包的物品为：")
                unnamed_id=1
                for i in target.item:
                    print(unnamed_id,end=" ")
                    unnamed_id+=1
                    print(i.name)
        else:
            print("你遇到bug了！告诉作者！")
    def attack(self, target):
        target.damage((weapons[self.weapon]["value"]+self.attack_add)*self.attack_percent//100)
        self.update()
    def damage(self,value):
        if ((value-shields[self.shield]["value"]-self.damage_minus)*self.damage_percent//100)>0:
            self.life-=(value-shields[self.shield]["value"]-self.damage_minus)*self.damage_percent//100
        self.update()
    def update(self):
        if self.life<=0:
            self.alive=False
        if self.life>self.max_life:
            self.life=self.max_life
        self.max_energy=self.max_energy_bak+energy_books[self.energy_book]["value"]
        if self.energy>self.max_energy:
            self.energy=self.max_energy
    def end_of_round(self):
        self.energy+=10
        for i in self.actions_bak.keys():
            self.actions[i]=self.actions_bak[i].copy()
        self.update()
        


