class gaoqiu(Player):
    name = "高俅"
    max_life = 50
    max_energy = 100
    attack_range_add = 1

    def attack(self, target):
        if type(self.weapon) == cz and "chanzhang_cd" not in self.buff:
            self.buff.append("chanzhang_cd")
        hurt = target.damage((self.weapon.value +
                              self.attack_add)*self.attack_percent//100)
        self.life += hurt
        self.update()
        return hurt