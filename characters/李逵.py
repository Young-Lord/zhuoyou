class likui(Player):
    life=80
    max_life=80
    energy=0
    max_energy=0
    def update(self):
        if life<=0:
            self.alive=False
        energy=0
        max_energy=0
