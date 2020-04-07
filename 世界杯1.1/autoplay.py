# coding=gbk


import numpy as np

cold_random = 0.05
cool_random = 0.4


def autoplay_get_random(number):
    path = "data/rand.txt"
    f = open(path, "r")
    line = [256]
    for lines in f.readlines():
        line = lines.split(",")
    # print("play_rand", number, int(line[number]))
    return int(line[number])


def play(team1, team2, number, verbose=True):
    # print("play_number",number)
    seed1 = autoplay_get_random(4)
    seed1 += number * 10

    ability1 = team1.ability
    ability2 = team2.ability

    fw1, mf1, df1 = team1.other_ability
    fw2, mf2, df2 = team2.other_ability
    abl_diff = ability1 - ability2
    fw_diff = fw1 - df2
    mf_diff = mf1 - mf2
    df_diff = fw2 - df1
    mean1, mean2 = max(-0.2, 0.1 * (abl_diff // 15)), max(-0.2, -0.1 * (abl_diff // 15))
    std1, std2 = 1 + min(0.5, (0.1 * (mf_diff // 10))), min(0.5, (1 - 0.1 * (mf_diff // 10)))
    std1, std2 = max(0.5, std1), max(0.5, std2)
    mean1 = mean1 + max(-0.2, (0.15 * (fw_diff // 10) - 0.15 * (df_diff // 10)))
    mean2 = mean2 + max(-0.2, (- 0.15 * (fw_diff // 10) + 0.15 * (df_diff // 10)))

    np.random.seed(seed1)
    record1 = np.random.lognormal(mean1, std1, 1)
    record1 = np.where(record1 > 4, 4, record1.astype(int))

    np.random.seed(seed1 + 30)
    record2 = np.random.lognormal(mean2, std2, 1)
    record2 = np.where(record2 > 4, 4, record2.astype(int))

    np.random.seed(seed1 + 40)
    cold = np.random.rand()
    if cold < cold_random:
        if record1[0] > record2[0]:
            record1[0] = max(0, record1[0] - 2)
            record2[0] += 2
        elif record1[0] == record2[0]:
            pass
        else:
            record2[0] = max(0, record2[0] - 2)
            record1[0] += 2
    elif cold < cool_random:
        if record1[0] > record2[0]:
            record1[0] = max(0, record1[0] - 1)
            record2[0] += 1
        elif record1[0] == record2[0]:
            pass
        else:
            record2[0] = max(0, record2[0] - 1)
            record1[0] += 1
    else:
        pass
    if verbose:
        if cold < cold_random:
            print(" 【爆冷。】 {}vs{} : {}-{}".format(team1.name, team2.name, record1[0], record2[0]))
        else:
            print("  {}vs{} : {}-{}".format(team1.name, team2.name, record1[0], record2[0]))
    # return "1-1" if np.random.rand() > 0.5 else "2-2"
    return "{}-{}".format(record1[0], record2[0])


class AutoPlay:
    def __init__(self, team1, team2, number):
        self.result = play(team1, team2, number)
        self.team1 = team1
        self.team2 = team2
        self.team1_gal = None
        self.team2_gal = None
        self.team1_flag = None
        self.team2_flag = None
        self.team1_diff = None
        self.team2_diff = None
        self.process(team1, team2)

    def process(self, team1, team2):
        record = self.result.split("-")
        if int(record[0]) > int(record[1]):
            self.team1_flag = 3
            self.team2_flag = 0
        elif int(record[0]) == int(record[1]):
            self.team1_flag = 1.5
            self.team2_flag = 1.5
        else:
            self.team1_flag = 0
            self.team2_flag = 3

        team1.game_set(int(record[0]), self.team1_flag, int(record[0]) - int(record[1]), team2)

        team2.game_set(int(record[1]), self.team2_flag, int(record[1]) - int(record[0]), team1)
