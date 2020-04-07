# coding=gbk

import numpy as np

from autoplay import AutoPlay, play
from group import Group
from shedule import schedule

map1 = {0: "16进8决赛", 1: "8进4决赛", 2: "半决赛", 3: "决赛"}


def game_get_random(number):
    path = "data/rand.txt"
    f = open(path, "r")
    line = [256]
    for lines in f.readlines():
        line = lines.split(",")
    # print("game_rand", number, int(line[number]))
    return int(line[number])


def print0():
    print("欢迎来到世界杯!")
    print("世界杯规则:共32支队伍进行比赛，分成8个小组，每个小组4支队伍\n"
          "晋级规则：8个小组前两名，共16支进入淘汰赛\n"
          "小组内排名依据: 积分>净胜球>进球数>互相战绩>互相净胜球>互相进球\n"
          "淘汰赛：16支队伍逐队厮杀，单败淘汰制")
    print("----------------")

    def show():
        information = []
        show_list = []
        path = "data/world_cup.csv"
        f = open(path, "r", encoding="gbk")
        print("编号 ：队伍名")
        for index, lines in enumerate(f.readlines()):
            line = lines.strip().replace("\n", "").split(",")
            line = [line[0], line[4], line[1], line[2], line[3], line[5], index]
            information.append(line)
            show_list.append(line[0])
        for i in range(0, len(show_list), 3):
            if i + 2 < len(show_list):
                print("{0:<4}:{1:{6}<6}"
                      "{2:<4}:{3:{6}<6}"
                      "{4:<4}:{5:{6}<6}".format(i, show_list[i],
                                                i + 1, show_list[i + 1],
                                                i + 2, show_list[i + 2], chr(12288)))
            else:
                print("{0:<4}:{1:{2}<6}".format(i, show_list[i],
                                                chr(12288)))
        return information

    information = show()

    num = input("请选择你的队伍编号:")
    print("---------------")
    while not num.isdigit():
        print("输入数字。")
        num = input("请选择你的队伍编号:")
    num = int(num)
    while num not in range(102):
        print("请输入0-101。")
        num = int(input("请选择你的队伍编号:"))
    print("你选择的队伍是:{}".format(information[num][0:5]))
    return information, num


def print1(information, num):
    print("请选择剩下31支队伍生成的方式：\n"
          "0：2018届世界杯32支队伍\n"
          "1：剩下最强的32支队伍\n"
          "2：随机生成剩下的32支队伍")
    team_world = [0, 1, 2, 3, 4, 5, 6, 8,
                  9, 11, 12, 13, 14, 15, 16, 17,
                  18, 19, 26, 29, 36, 37, 38, 40,
                  41, 42, 43, 52, 53, 54, 69, 83
                  ]
    team_generate_key = input("请输入生成方式(数字)：")
    team_num_list = [num]
    if team_generate_key not in ["0", "1", "2"]:
        print("输入错误，强制设为0：2018届世界杯32支队伍。")
        team_generate_key = "1"

    if team_generate_key == "0":
        seed1 = game_get_random(1)
        np.random.seed(seed1 + 10)
        if team_num_list[0] in team_world:
            team_num_list = team_world
        else:
            temp = np.random.choice(team_world, 31, replace=False)
            team_num_list.extend(temp)

    elif team_generate_key == "1":
        seed1 = game_get_random(1)
        np.random.seed(seed1 + 20)
        temp = sorted(information, key=lambda x: x[1], reverse=True)[0:32]
        strong_num = list(np.array(temp)[:, -1])
        strong_num = list(map(int, strong_num))
        if num in strong_num:
            team_num_list = strong_num
        else:
            team_num_list = team_num_list + strong_num[0:31]

    elif team_generate_key == "2":
        seed1 = game_get_random(1)
        np.random.seed(seed1 + 30)
        choice_list = list(set(range(102)) - set(team_num_list))
        temp = list(np.random.choice(choice_list, 31, replace=False))
        team_num_list = team_num_list + temp

    else:
        assert False

    assert len(set(team_num_list)) == 32
    temp = list(np.array(information)[team_num_list][:, -2])
    temp = list(map(int, temp))
    team_num_list = [x for _, x in sorted(zip(temp, team_num_list))]
    # print("参加世界杯的队伍有：")
    # print(np.array(information)[team_num_list, 0])
    print("-------------------")
    return team_num_list


class Game:
    def __init__(self):
        # 获取个人球队

        self.information, self.num = print0()
        self.my_team = None
        # 获取所有球队
        self.team_num_list = print1(self.information, self.num)
        self.my_group = None
        self.other_group = None
        self.play = None
        self.my_schedule = None
        self.other_schedule = {}
        self.final_list = None
        self.final_fight_list = None
        self.eight_list = []
        self.four_list = []
        self.two_list = []
        self.winner = None
        self.count = 0

    def chou(self):
        # 获取分组名单（抽签）
        group_map = {
            "A": [], "B": [], "C": [], "D": [], "E": [], "F": [], "G": [], "H": []
        }
        for i in range(0, 32, 8):
            temp = np.array(self.team_num_list[i:i + 8])

            seed1 = game_get_random(i // 8)
            np.random.seed(seed1 + 7)

            np.random.shuffle(temp)
            for key, number in zip(group_map.keys(), temp):
                group_map[key].append(number)

        group_a, group_b = Group("A", group_map["A"], self.information), Group("B", group_map["B"], self.information)
        group_c, group_d = Group("C", group_map["C"], self.information), Group("D", group_map["D"], self.information)
        group_e, group_f = Group("E", group_map["E"], self.information), Group("F", group_map["F"], self.information)
        group_g, group_h = Group("G", group_map["G"], self.information), Group("H", group_map["H"], self.information)

        for index, group_my in enumerate([group_a, group_b, group_c, group_d, group_e, group_f, group_g, group_h]):
            if self.num in group_my.team_name_num_list:
                group_my.my_show()
                self.my_group = group_my
                self.other_group = list(
                    {group_a, group_b, group_c, group_d, group_e, group_f, group_g, group_h} - {self.my_group})
                self.other_group = sorted(self.other_group, key=lambda x: x.name)
                print("-------------------")
            else:
                group_my.show()
                print("-------------------")
        return group_a, group_b, group_c, group_d, group_e, group_f, group_g, group_h

    def my_play(self, index):
        """
        index: 第几轮（自己小组）
        play_station: 放的是team
        """
        if index == 0:
            self.my_schedule = schedule(self.my_group)
            ind = 1
        else:
            ind = index + 1
        self.play = self.my_schedule[index]
        for play_station in self.play:
            if self.num in [x.index for x in play_station]:
                print("***第{}轮对阵:{}vs{}****".format(index + 1, play_station[0].name, play_station[1].name))
                if index == 0:
                    if self.num == play_station[0].index:
                        self.my_team = play_station[0]
                    else:
                        self.my_team = play_station[1]
                else:
                    pass
                #
                record = input("请输入{}vs{}的比分[示例3-1]：".
                               format(play_station[0].name, play_station[1].name))

                record = record.replace(":", "-").replace("：", "-").split("-")

                error_flag = 1
                while error_flag:
                    try:
                        a, b = int(record[0]), int(record[1])
                        assert 0 <= a <= 13
                        assert 0 <= b <= 13
                        error_flag = 0
                    except ValueError:
                        record = input("请输入{}vs{}的比分[示例3-1]：".
                                       format(play_station[0].name, play_station[1].name))
                        record = record.replace(":", "-").replace("：", "-").split("-")
                    except AssertionError:
                        record = input("请输入{}vs{}的比分[示例3-1]：".
                                       format(play_station[0].name, play_station[1].name))
                        record = record.replace(":", "-").replace("：", "-").split("-")
                    except IndexError:
                        record = input("请输入{}vs{}的比分[示例3-1]：".
                                       format(play_station[0].name, play_station[1].name))
                        record = record.replace(":", "-").replace("：", "-").split("-")

                if int(record[0]) > int(record[1]):
                    flag = 3
                elif int(record[0]) == int(record[1]):
                    flag = 1.5
                else:
                    flag = 0

                for index, (team, gal) in enumerate(zip(play_station, record)):
                    gal = int(gal)
                    if index == 0:
                        team.game_set(gal, flag, int(record[0]) - int(record[1]), play_station[1])
                    else:
                        team.game_set(gal, 3 - flag, int(record[1]) - int(record[0]), play_station[0])

            else:
                print("第{}轮本组其他对阵:{}vs{}".format(ind, play_station[0].name, play_station[1].name))
                self.count += 1
                AutoPlay(play_station[0], play_station[1], self.count)

    def other_play(self, index):
        if index == 0:
            for group in self.other_group:
                self.other_schedule.update({group.name: schedule(group)})

        for group in self.other_group:
            self.play = self.other_schedule[group.name][index]
            for play_station in self.play:
                self.count += 1
                AutoPlay(play_station[0], play_station[1], self.count)

    def final_game(self):
        final_list = []

        for group in [self.my_group] + self.other_group:
            for index, team in enumerate(group.team):
                if index == 0:
                    final_list.append(team)
                    team.position = 1
                if index == 1:
                    final_list.append(team)
                    team.position = 2
            print("{}前两名:{},{} 晋级16强！".format(group.name, group.team[0].name, group.team[1].name))

        self.final_list = final_list

    def final_chou(self):
        copy_flag = 1
        loop_num = 0
        while copy_flag:
            copy_flag = 0

            seed1 = game_get_random(3)
            np.random.seed(seed1 + loop_num * 20)
            loop_num += 1
            print("【暗箱操作中】")
            self.final_fight_list = np.array([[None, None] for _ in range(8)])
            self.final_list = sorted(self.final_list, key=lambda x: x.group_name)

            for team in self.final_list:
                if team.group_name == "A组":
                    if team.position == 1:
                        self.final_fight_list[0, 0] = team
                    elif team.position == 2:
                        self.final_fight_list[4, 0] = team
                elif team.group_name == "B组":
                    if team.position == 1:
                        self.final_fight_list[4, 1] = team
                    elif team.position == 2:
                        self.final_fight_list[0, 1] = team
                elif team.group_name == "C组":
                    if team.position == 1:
                        self.final_fight_list[1, 0] = team
                    elif team.position == 2:
                        self.final_fight_list[5, 0] = team
                elif team.group_name == "D组":
                    if team.position == 1:
                        self.final_fight_list[5, 1] = team
                    elif team.position == 2:
                        self.final_fight_list[1, 1] = team
                elif team.group_name == "E组":
                    if team.position == 1:
                        self.final_fight_list[2, 0] = team
                    elif team.position == 2:
                        self.final_fight_list[6, 0] = team
                elif team.group_name == "F组":
                    if team.position == 1:
                        self.final_fight_list[6, 1] = team
                    elif team.position == 2:
                        self.final_fight_list[2, 1] = team
                elif team.group_name == "G组":
                    if team.position == 1:
                        self.final_fight_list[3, 0] = team
                    elif team.position == 2:
                        self.final_fight_list[7, 0] = team
                elif team.group_name == "H组":
                    if team.position == 1:
                        self.final_fight_list[7, 1] = team
                    elif team.position == 2:
                        self.final_fight_list[3, 1] = team
            for stage, (team1, team2) in enumerate(self.final_fight_list):
                print("***{}对阵第{}组:{}vs{}****".format(map1[0], stage + 1, team1.name, team2.name))
            print("-------------------------------------")

    def my_final_play(self):
        for team1, team2 in self.final_fight_list:
            if self.my_team in [team1, team2]:
                record = input("请输入{}vs{}的比分[示例3-1]：".
                               format(team1.name, team2.name))
                record = record.replace(":", "-").replace("：", "-").split("-")

                error_flag = 1
                while error_flag:
                    try:
                        a, b = int(record[0]), int(record[1])
                        assert 0 <= a <= 13
                        assert 0 <= b <= 13
                        assert a != b
                        error_flag = 0
                    except ValueError:
                        record = input("请输入{}vs{}的比分[示例3-1]：".
                                       format(team1.name, team2.name))
                        record = record.replace(":", "-").replace("：", "-").split("-")
                    except AssertionError:
                        record = input("请输入{}vs{}的比分[示例3-1]：".
                                       format(team1.name, team2.name))
                        record = record.replace(":", "-").replace("：", "-").split("-")
                    except IndexError:
                        record = input("请输入{}vs{}的比分[示例3-1]：".
                                       format(team1.name, team2.name))
                        record = record.replace(":", "-").replace("：", "-").split("-")

                if record[0] > record[1]:
                    self.eight_list.append(team1)
                elif record[0] == record[1]:
                    print("错误")
                else:
                    self.eight_list.append(team2)
                print("  {}vs{} : {}-{}".format(team1.name, team2.name, record[0], record[1]))

            else:
                self.count += 1
                record = play(team1, team2, self.count, False)
                record = record.split("-")
                while record[0] == record[1]:
                    self.count += 1
                    record = play(team1, team2, self.count, False)
                    record = record.split("-")

                if record[0] > record[1]:
                    self.eight_list.append(team1)
                else:
                    self.eight_list.append(team2)
                print("  {}vs{} : {}-{}".format(team1.name, team2.name, record[0], record[1]))
        print("{} 晋级8强！".format(",".join([x.name for x in self.eight_list])))

    def eight_chou(self):
        self.eight_list = np.array(self.eight_list).reshape(4, 2)
        for stage, (team1, team2) in enumerate(self.eight_list):
            print("***{}对阵第{}组:{}vs{}****".format(map1[1], stage + 1, team1.name, team2.name))
        print("-------------------------------------")

    def my_eight_play(self):
        for team1, team2 in self.eight_list:
            if self.my_team in [team1, team2]:
                record = input("请输入{}vs{}的比分[示例3-1]：".
                               format(team1.name, team2.name))
                record = record.replace(":", "-").replace("：", "-").split("-")

                error_flag = 1
                while error_flag:
                    try:
                        a, b = int(record[0]), int(record[1])
                        assert 0 <= a <= 13
                        assert 0 <= b <= 13
                        assert a != b
                        error_flag = 0
                    except ValueError:
                        record = input("请输入{}vs{}的比分[示例3-1]：".
                                       format(team1.name, team2.name))
                        record = record.replace(":", "-").replace("：", "-").split("-")
                    except AssertionError:
                        record = input("请输入{}vs{}的比分[示例3-1]：".
                                       format(team1.name, team2.name))
                        record = record.replace(":", "-").replace("：", "-").split("-")
                    except IndexError:
                        record = input("请输入{}vs{}的比分[示例3-1]：".
                                       format(team1.name, team2.name))
                        record = record.replace(":", "-").replace("：", "-").split("-")

                if record[0] > record[1]:
                    self.four_list.append(team1)
                elif record[0] == record[1]:
                    print("错误")
                else:
                    self.four_list.append(team2)
                print("  {}vs{} : {}-{}".format(team1.name, team2.name, record[0], record[1]))

            else:
                self.count += 1
                record = play(team1, team2, self.count, False)
                record = record.split("-")
                while record[0] == record[1]:
                    self.count += 1
                    record = play(team1, team2, self.count, False)
                    record = record.split("-")

                if record[0] > record[1]:
                    self.four_list.append(team1)
                else:
                    self.four_list.append(team2)
                print("  {}vs{} : {}-{}".format(team1.name, team2.name, record[0], record[1]))
        print("{} 晋级4强！".format(",".join([x.name for x in self.four_list])))

    def four_chou(self):
        self.four_list = np.array(self.four_list).reshape(2, 2)
        for stage, (team1, team2) in enumerate(self.four_list):
            print("***{}对阵第{}组:{}vs{}****".format(map1[2], stage + 1, team1.name, team2.name))
        print("-------------------------------------")

    def my_four_play(self):
        for team1, team2 in self.four_list:
            if self.my_team in [team1, team2]:
                record = input("请输入{}vs{}的比分[示例3-1]：".
                               format(team1.name, team2.name))
                record = record.replace(":", "-").replace("：", "-").split("-")

                error_flag = 1
                while error_flag:
                    try:
                        a, b = int(record[0]), int(record[1])
                        assert 0 <= a <= 13
                        assert a != b
                        assert 0 <= b <= 13
                        error_flag = 0
                    except ValueError:
                        record = input("请输入{}vs{}的比分[示例3-1]：".
                                       format(team1.name, team2.name))
                        record = record.replace(":", "-").replace("：", "-").split("-")
                    except AssertionError:
                        record = input("请输入{}vs{}的比分[示例3-1]：".
                                       format(team1.name, team2.name))
                        record = record.replace(":", "-").replace("：", "-").split("-")
                    except IndexError:
                        record = input("请输入{}vs{}的比分[示例3-1]：".
                                       format(team1.name, team2.name))
                        record = record.replace(":", "-").replace("：", "-").split("-")

                if record[0] > record[1]:
                    self.two_list.append(team1)
                elif record[0] == record[1]:
                    print("错误")
                else:
                    self.two_list.append(team2)
                print("  {}vs{} : {}-{}".format(team1.name, team2.name, record[0], record[1]))

            else:
                self.count += 1
                record = play(team1, team2, self.count, False)
                record = record.split("-")
                while record[0] == record[1]:
                    self.count += 1
                    record = play(team1, team2, self.count, False)
                    record = record.split("-")

                if record[0] > record[1]:
                    self.two_list.append(team1)
                else:
                    self.two_list.append(team2)
                print("  {}vs{} : {}-{}".format(team1.name, team2.name, record[0], record[1]))
        print("{} 晋级决赛！".format(",".join([x.name for x in self.two_list])))

    def two_chou(self):
        print("***{}对阵:{}vs{}****".format(map1[3], self.two_list[0].name, self.two_list[1].name))
        print("-------------------------------------")

    def my_two_play(self):
        record = input("请输入{}vs{}的比分[示例3-1]：".format(self.two_list[0].name, self.two_list[1].name))
        record = record.replace(":", "-").replace("：", "-").split("-")

        error_flag = 1
        while error_flag:
            try:
                a, b = int(record[0]), int(record[1])
                assert 0 <= a <= 13
                assert a != b
                assert 0 <= b <= 13
                error_flag = 0
            except ValueError:
                record = input("请输入{}vs{}的比分[示例3-1]：".format(self.two_list[0].name, self.two_list[1].name))
                record = record.replace(":", "-").replace("：", "-").split("-")
            except AssertionError:
                record = input("请输入{}vs{}的比分[示例3-1]：".format(self.two_list[0].name, self.two_list[1].name))
                record = record.replace(":", "-").replace("：", "-").split("-")
            except IndexError:
                record = input("请输入{}vs{}的比分[示例3-1]：".format(self.two_list[0].name, self.two_list[1].name))
                record = record.replace(":", "-").replace("：", "-").split("-")

        if record[0] > record[1]:
            self.winner = self.two_list[0].name
        elif record[0] == record[1]:
            print("错误")
        else:
            self.winner = self.two_list[1].name
        print(" {}vs{} : {}-{}".format(self.two_list[0].name, self.two_list[1].name, record[0], record[1]))
        if self.my_team.name == self.winner:
            print("{} 恭喜你是冠军！".format(self.my_team.name))
        else:
            print("{} 恭喜你获得亚军！".format(self.my_team.name))
