class likui(Player):
    name="李逵"
    life=80
    max_life=80
    energy=0
    max_energy=0
    max_energy_bak=0
    def update(self):
        if self.life<=0:
            self.alive=False
        self.energy=0
        self.max_energy=0
    actions_bak={"attack":{"name":"攻击","arg":"玩家序号","count":3},"goto":{"name":"移动","arg":"坐标","count":1},"info":{"name":"查看","arg":"","count":-1},"use":{"name":"使用","arg":"物品ID","count":-1},"end":{"name":"结束回合","arg":"","count":1}}

