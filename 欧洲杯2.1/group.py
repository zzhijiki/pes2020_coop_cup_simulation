# coding=gbk

from team import Team


class Group:
    def __init__(self, name, team_num_list, information):
        self.name = name + "��"
        self.team = []
        self.team_name_num_list = team_num_list
        for number in team_num_list:
            self.team.append(Team(information, number))
        for team in self.team:
            team.group_name = self.name

    def my_show(self):
        print("��ǰС��:{}".format(self.name))
        column = "{0:{7}<6}\t{1:{7}<3}\t{2:{7}<3}\t{3:{7}<3}\t{4:{7}<3}\t{5:{7}<3}\t{6:{7}<3}"
        print(column.format("������", "��", "ʤ", "ƽ", "��", "��", "��", chr(12288)))
        # ����[]
        self.team = self.group_sort
        for team in self.team:
            print(column.format(
                team.name, team.score,
                team.win, team.draw, team.lose, team.goal, team.goal_diff, chr(12288)))

    def show(self):
        print("{}��С���Ա:{}".format(self.name, [x.name for x in self.team]))

    @property
    def group_sort(self):
        # ����>����ս��>���ྻʤ��>�������>��ʤ��>������\n"
        score_map = {}
        team_score_list = [x.score for x in self.team]
        team_score_list = sorted(team_score_list, reverse=True)
        if len(set(team_score_list)) == 4:
            team_list = sorted(self.team, key=lambda x: x.score, reverse=True)
            return team_list
        else:
            for team in self.team:
                if team.score in score_map:
                    score_map[team.score].append(team)
                else:
                    score_map[team.score] = [team]
            for key, value in score_map.items():
                if len(value) == 2:
                    if value[1].name in value[0].fight:  # 2���Ѿ���ս
                        if value[0].fight[value[1].name][2] == 0:
                            score_map[key] = [value[1], value[0]]
                        elif value[0].fight[value[1].name][2] == 1.5:  # 2�ӻ���ս����ƽ
                            score_map[key] = sorted(value, key=lambda x: (x.score, x.goal_diff, x.goal, x.ability),
                                                    reverse=True)
                        else:
                            continue
                    else:  # 2�ӻ�û��ս
                        score_map[key] = sorted(value, key=lambda x: (x.score, x.goal_diff, x.goal, x.ability),
                                                reverse=True)
                elif len(value) == 3:  # 3��ѭ��ս��
                    for team in self.team:
                        if team.score not in score_map:
                            another = team
                    for team in self.team:
                        if len(score_map[team.score]) == 3:
                            for team_copy in value:
                                if team_copy.name in team.fight:
                                    team.sup1 += team.fight[team_copy.name][2]
                                    team.sup2 += team.fight[team_copy.name][0] - team.fight[team_copy.name][1]
                                    team.sup3 += team.fight[team_copy.name][0]
                    score_map[key] = sorted(value, key=lambda x: (
                        x.score, x.sup1, x.sup2, x.sup3, x.goal_diff, x.goal, x.ability),
                                            reverse=True)
                else:  # �Ķ�ͬ�֣�����ս������ȫ��ս��
                    score_map[key] = sorted(value, key=lambda x: (x.score, x.goal_diff, x.goal, x.ability),
                                            reverse=True)

        b = sorted(score_map.items(), key=lambda kv: kv[0], reverse=True)
        b = [x[1] for x in b]
        team_list = []
        for item in b:
            team_list.extend(item)
        return team_list
