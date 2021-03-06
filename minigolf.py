from collections import deque


class Player:

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return 'Player: {}'.format(self._name)

    @property
    def name(self):
        return self._name


class Match:
    MAX_HIT = 10

    def __init__(self, holes, players):
        self.holes = holes
        self.players = [player for player in players]

        self._finished = False
        self.score_list = [[None for _ in range(len(self.players))] for _ in range(self.holes)]

        self.cur_player = 0
        self.cur_hole = 0

    @property
    def finished(self):
        return self._finished

    def get_table(self):
        table = [tuple(elem) for elem in self.score_list]
        table.insert(0, tuple(player.name for player in self.players))
        return table

    def get_all_winners(self,func):
        if self.finished:
            final_score = {i: sum([row[i] for row in self.score_list]) for i in range(len(self.score_list))}
            return [self.players[player] for player, score in final_score.items()
                        if score == func(final_score.values())]
        else:
            raise RuntimeError

    def hit(self, success=False):

        if self.finished:
            raise RuntimeError
        else:
            if success:
                self.success_hit()
            else:
                self.fail_hit()

            self.cur_player += 1
            self.round_analisys()

        if self.cur_hole == self.holes and self.cur_player == len(self.players):
            self._finished = True


class HitsMatch(Match):

    def __init__(self, holes, players):
        super().__init__(holes, players)
        self.hit_list = [{'number': i, 'hit': 0} for i in range(len(self.players))]
        # список игроков попавших в лунку за круг
        self.success_list = []

    def change_hole(self):
        self.cur_hole += 1

        if self.cur_hole == self.holes:
            self._finished = True
            return None

        self.hit_list = deque([{'number': i, 'hit': 0} for i in range(len(self.players))])
        self.hit_list.rotate(-self.cur_hole)

    def cleaning_players(self):
        for i in self.success_list[::-1]:
            del self.hit_list[i]

        self.success_list = []

    def success_hit(self):
        if self.hit_list[self.cur_player]['hit'] == 0:
            self.score_list[self.cur_hole][self.hit_list[self.cur_player]['number']] = 1
        # если игрок попал не с первого раза
        else:
            self.score_list[self.cur_hole][self.hit_list[self.cur_player]['number']] = self.hit_list[self.cur_player][
                                                                                          'hit'] + 1
        self.success_list.append(self.cur_player)

    def fail_hit(self):
        self.hit_list[self.cur_player]['hit'] += 1
        if self.hit_list[self.cur_player]['hit'] == Match.MAX_HIT - 1:
            self.score_list[self.cur_hole][self.hit_list[self.cur_player]['number']] = Match.MAX_HIT
            self.success_list.append(self.cur_player)

    def round_analisys(self):
        if self.cur_player == len(self.hit_list):

            if self.success_list:
                self.cleaning_players()

                if not self.hit_list:
                    self.change_hole()

            self.cur_player = 0

    def get_winners(self):
        return self.get_all_winners(min)


class HolesMatch(Match):

    def __init__(self, holes, players):
        super().__init__(holes, players)
        # текущий круг
        self.round = 0
        # попадание за круг
        self.flag_hit = False
        # очередь
        self.player_change = deque([i for i in range(len(self.players))])

    def change_hole(self):
        self.round = 0
        self.cur_hole += 1
        self.player_change.rotate(-1)

    def change_round(self):
        self.cur_player = 0
        self.flag_hit = False
        self.round = 0

    def end_of_hole_whithout_success(self):
        for i in range(self.holes):
            if self.score_list[self.cur_hole][i] is None:
                self.score_list[self.cur_hole][i] = 0

    def success_hit(self):
        # если удар успешный, записали очко в таблицу и зафиксировали попадание
        self.score_list[self.cur_hole][self.player_change[self.cur_player]] = 1
        self.flag_hit = True

    def fail_hit(self):
        pass

    def round_analisys(self):
        # если все уже ударили, ход переходит к 1ому и переход на следующую лунку и меняем очерёдность игроков
        if self.cur_player == len(self.players):
            # если есть попадание
            if self.flag_hit:
                self.change_round()
                # у тех кто не забил, ставим 0
                self.end_of_hole_whithout_success()

                self.change_hole()
                if self.cur_hole == self.holes:
                    self._finished = True

            # если никто не забил, начинаем новый круг с 1ого игрока
            else:
                self.cur_player = 0
                self.round += 1

                if self.round == Match.MAX_HIT:
                    for i in range(self.holes):
                        self.score_list[self.cur_hole][i] = 0
                    self.change_hole()

    def get_winners(self):
        return self.get_all_winners(max)