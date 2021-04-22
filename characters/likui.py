class likui(Player):
    name = "李逵"
    life = 8000
    max_life = 8000
    energy = 0
    max_energy = 0
    max_energy_bak = 0

    def init_custom(self):
        self.actions_bak["attack"]["count"] = 3

    def update(self):
        if not self.alive:
            return
        if self.life <= 0:
            self.zhiliao()
        if not self.alive:
            return
        if self.life > self.max_life:
            self.life = self.max_life
        self.energy = 0
        self.max_energy = 0
