class Player:
    name="默认角色"
    life = 80
    max_life = 80
    energy = 80
    max_energy = 80
    pos = (-1, -1)
    alive = True
    team = 0
    item = list()
    buff = list() # 这是存各种技能的标记（如“义”）用的
    weapon = None
    armor=None
    shoe=None
    attack_add = 0 #先add在percent
    attack_percent = 100
    damage_minus = 0
    damage_percent = 100
    speed_add = 0
    random_step=0
    def action(self):
        global players,DEBUG
        print("攻击：\"attack 玩家序号\"；移动：\"goto 坐标\"")
        print("你可以走的距离为："+str(self.random_step+shoes[self.shoe]["value"]+self.speed_add))
        command=input().split(' ',1)
        if len(command)!=2:
            return self.action()
        if command[0]=='attack':
            if players[int(command[1])-1]==self:
                self.attack(self)
                print("最好不要自刀，当然你要真想也可以...")
                sleep(1 if not DEBUG else 0)
                return
            route=(astar.astar(gameMapWithPlayers(self,players[int(command[1])-1]),self.pos[0],self.pos[1],players[int(command[1])-1].pos[0],players[int(command[1])-1].pos[1]))
            if route==list():
                print("无法到达！")
                return self.action()
            if len(route)>weapons[self.weapon]["distance"]:
                print("太远了！")
                return self.action()
            self.attack(players[int(command[1])-1])
        elif command[0]=='goto':
            try:
                command[1]=command[1].replace("(","").replace(")","")
                command[1]=command[1].replace(","," ")
                a,b=[int(i) for i in command[1].split()]
            except:
                return self.action()
            if (not isBlockEmpty(a,b)) and self.pos!=(a,b):
                print("此位置已被占用，请换一个位置。")
                return self.action()
            if self.pos==(a,b):      
                return
            route=(astar.astar(gameMapWithPlayers(self),self.pos[0],self.pos[1],a,b))
            if route==list():
                print("无法到达！")
                return self.action()
            if len(route)>(self.random_step+shoes[self.shoe]["value"]+self.speed_add):
                print("太远了！")
                return self.action()
            print("走法",end="：")
            for i in route:
                print(i,end="")
            self.pos=(a,b)
        else:
            print("未知命令")
            return self.action()
        self.end_of_round()
    def attack(self, target):
        target.damage((weapons[self.weapon]["value"]+self.attack_add)*self.attack_percent//100)
        self.update()
    def damage(self,value):
        if ((value-armors[self.armor]["value"]-self.damage_minus)*self.damage_percent//100)>0:
            self.life-=(value-armors[self.armor]["value"]-self.damage_minus)*self.damage_percent//100
        self.update()
    def update(self):
        if self.life<=0:
            self.alive=False
        if self.life>self.max_life:
            self.life=self.max_life
        if self.energy>self.max_energy:
            self.energy=self.max_energy
    def end_of_round(self):
        self.energy+=10
        self.update()
        


