class try2(Player):
    name = "测试工具人2-给牌"

    def init_custom(self):
        self.actions_bak["zhudong1"] = {
            "name": "给牌", "arg": "目标角色", "count": 1}

    def zhudong1_(self, command):
        global action_result
        try:
            target_index = int(command[1])
        except IndexError:
            action_result = "参数过少！"
            return
        except ValueError:
            action_result = "参数错误！"
            return
        if not 1 <= target_index <= player_count:
            action_result = "玩家不存在！"
            return
        target = players[target_index-1]
        self.actions["zhudong1"]["count"] -= 1
        get_card = mopai(1)
        for i in get_card:
            action_result = "你给了他一张 {}！".format(i.name)
            target.item.append(i)
        self.update()
