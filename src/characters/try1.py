class try1(Player):
    name = "测试工具人1-回复"
    life = 10000

    def init_custom(self):
        self.actions_bak["zhudong1"] = {"name": "回复", "arg": "", "count": 1}

    def zhudong1_(self, command):
        self.actions["zhudong1"]["count"] -= 1
        self.life += 1000
        self.update()
