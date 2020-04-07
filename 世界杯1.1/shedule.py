# coding=gbk

import numpy as np


def get_random():
    path = "data/rand.txt"
    f = open(path, "r")
    line = [256]
    for lines in f.readlines():
        line = lines.split(",")
    return int(line[0])


class schedule:
    def __init__(self, group):
        self.name = group.name + "赛程"
        self.stage = np.array([[[group.team[0], group.team[3]],
                                [group.team[2], group.team[1]]],
                               [[group.team[0], group.team[2]],
                                [group.team[1], group.team[3]]],
                               [[group.team[0], group.team[1]],
                                [group.team[3], group.team[2]]]])
        seed1 = get_random()
        np.random.seed(seed=seed1)
        np.random.shuffle(self.stage)

    def __getitem__(self, index):
        return self.stage[index]
