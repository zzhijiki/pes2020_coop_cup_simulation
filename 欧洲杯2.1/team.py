# coding=gbk


class Team:
    def __init__(self, information, num):
        self.name = information[num][0]
        self.index = int(information[num][-1])
        self.ability = int(information[num][1])
        self.other_ability = list(map(int, information[num][2:5]))
        self.level = int(information[num][-2])
        self.score = 0
        self.win = 0
        self.draw = 0
        self.lose = 0
        self.goal = 0
        self.goal_diff = 0
        self.go_to_final = None
        self.fight = {}
        self.sup1 = 0
        self.sup2 = 0
        self.sup3 = 0
        self.group_name = None
        self.position = None

    def game_set(self, gal, flag, diff, team_another):
        if flag == 3:
            self.win += 1
            self.score += 3
        elif flag == 1.5:
            self.draw += 1
            self.score += 1
        else:
            self.lose += 1
            self.score += 0

        self.goal += gal
        self.goal_diff += diff
        self.fight.update({team_another.name: [gal, gal - diff, flag]})
