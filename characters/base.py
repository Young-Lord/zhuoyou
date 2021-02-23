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
        self.buff = list()
        #WARNING: 每个可变对象（list,dict）等都必须在这里初始化，否则不同的实例会共享一个对象
        for i in self.actions_bak.keys():
            self.actions[i]=self.actions_bak[i].copy()
        self.life=self.max_life
        self.energy=self.max_energy
    def round(self):
        global random_step
        self.random_step=random_step
        global error_hint
        error_hint=""
        if len(cards)>get_cards:
            print("="*10)
            for i in range(get_cards):
                selected=random.choice(cards)
                print("你摸到了1张"+selected.name+"！")
                cards.remove(selected)
                self.item.append(selected)
            print("="*10)
        while self.actions["end"]["count"]:
            if error_hint!="":
                print("="*10)
                print(error_hint)
                print("="*10)
            drawAll()
            error_hint=""
            self.action()
            cls()
        self.end_of_round()
    def action(self):
        global players,DEBUG,error_hint
        for i in list(self.actions.keys()):
            if self.actions[i]["count"]!=0:
                print("{}：{} {}".format(self.actions[i]["name"],i,self.actions[i]["arg"]))
        if self.actions["goto"]["count"]!=0:
            print("你可以走的距离为："+str(self.random_step+shoes[self.shoe]["value"]+self.speed_add))
        command=input().split(' ',1)
        if (command[0] not in list(self.actions.keys())) and command[0].find("debug")==-1:
            error_hint="未知命令"
            return
        if command[0].find("debug")=="-1" and self.actions[command[0]]["count"]==0:
            error_hint="你已经进行过此操作了！"
            return
        if command[0]=='attack':
            self.attack_(command)
        elif command[0]=='goto':
            self.goto_(command)
        elif command[0]=='end':
            self.actions[command[0]]["count"]-=1
        elif command[0]=='item':
            self.item_(command)
        elif command[0]=='use':
            self.use_(command)
        elif command[0]=='debug_eval':
            command=command[1]
            eval(command)
        elif command[0]=='debug_showbuff':
            print(self.buff)
        elif command[0]=='debug_showitem':
            command=command[1].split()
            command[0]=int(command[0])
            target=players[command[0]-1]
            if target.item==list():
                error_hint="他的背包什么都没有！"
            else:
                error_hint="他的背包的物品为：\n"
                unnamed_id=1
                for i in target.item:
                    error_hint+=str(unnamed_id)+' '
                    unnamed_id+=1
                    error_hint+=i.name+'\n'
        else:
            error_hint="你遇到bug了！告诉作者！"
    def attack_(self,command):
        global error_hint
        if "chanzhang_cd_2" in self.buff:
            error_hint="禅杖冷却中..."
            self.actions[command[0]]["count"]-=1
            return
        if players[int(command[1])-1]==self:
            self.attack(self)
            self.actions[command[0]]["count"]-=1
            error_hint="最好不要自刀，当然你要真想也可以..."
            return
        route=(astar.astar(gameMapWithPlayers(self,players[int(command[1])-1]),self.pos[0],self.pos[1],players[int(command[1])-1].pos[0],players[int(command[1])-1].pos[1]))
        if route==list():
            error_hint="无法到达！"
            return
        if len(route)>weapons[self.weapon]["distance"]:
            error_hint="太远了！"
            return
        self.attack(players[int(command[1])-1])
        self.actions[command[0]]["count"]-=1
    def goto_(self,command):
        global error_hint
        try:
            command[1]=command[1].replace("(","").replace(")","")
            command[1]=command[1].replace(","," ")
            a,b=[int(i) for i in command[1].split()]
        except:
            return
        if (not isBlockEmpty(a,b)) and self.pos!=(a,b):
            error_hint="此位置已被占用，请换一个位置。"
            return
        if self.pos==(a,b):
            self.actions[command[0]]["count"]-=1
            return
        route=(astar.astar(gameMapWithPlayers(self),self.pos[0],self.pos[1],a,b))
        if route==list():
            error_hint="无法到达！"
            return
        if len(route)>(self.random_step+shoes[self.shoe]["value"]+self.speed_add):
            error_hint="太远了！"
            return
        error_hint="走法：\n"
        for i in route:
            error_hint+=i
        self.pos=(a,b)
        self.actions[command[0]]["count"]-=1
    def item_(self,command):
        global error_hint
        if self.item==list():
            error_hint="你的背包什么都没有！"
        else:
            error_hint="你的背包的物品为：\n"
            unnamed_id=1
            for i in self.item:
                error_hint+=str(unnamed_id)+' '
                unnamed_id+=1
                error_hint+=i.name+'\n'
    def use_(self,command):
        command=command[1].split()
        command[0]=int(command[0])
        if command[0]>len(self.item):
            error_hint="此ID的物品不存在！"
            return
        if len(command)>=2:
            if int(command[1])-1<0:
                error_hint="玩家ID错误！"
                return
        return_value=True
        try:
            return_value=self.item[command[0]-1].use(self,players[int(command[1])-1])
        except IndexError:
            try:
                return_value=self.item[command[0]-1].use(self)
            except IOError:
                error_hint="你没有指定目标！"
        if return_value!=True:
            self.item.pop(command[0]-1)
    def attack(self, target):
        if self.weapon=="禅杖":
            self.buff.append("chanzhang_cd")
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
        if "chanzhang_cd_2" in self.buff:
            self.buff.remove("chanzhang_cd")
            self.buff.remove("chanzhang_cd_2")
        if "chanzhang_cd" in self.buff:
            self.buff.append("chanzhang_cd_2")
