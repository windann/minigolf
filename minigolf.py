from collections import deque

class Player:
    def __init__(self,name):
        self._name = name
    def __str__(self):
        return 'Игрок: {}'.format(self._name)
    @property
    def name(self):
        return self._name


class Match:
    def __init__(self, holes, players):
        self.holes = holes
        self.players = [player for player in players]

        self._finished = False
        self.score_list = [[None for _ in range(len(self.players))] for _ in range(self.holes)]

        # текущий игрок
        self.cur_player = 0
        # текущая лунка
        self.cur_hole = 0

    @property
    def finished(self):
        return self._finished

    def get_table(self):
        table = [tuple(elem) for elem in self.score_list]
        table.insert(0, tuple(player.name for player in self.players))
        return table


class HitsMatch(Match):
    def __init__(self,holes,players):
        super().__init__(holes,players)
        self.hit_list = [{'номер': i, 'удар': 0 } for i in range(len(self.players))]
        # список игроков попавших в лунку за круг
        self.success_list = []

    def change_hole(self):
        self.cur_hole += 1

        if self.cur_hole == self.holes:
            self._finished = True
            return None

        self.hit_list = deque([{'номер': i, 'удар': 0} for i in range(len(self.players))])
        self.hit_list.rotate(-self.cur_hole)


    def cleaning_players(self):
        for i in self.success_list[::-1]:
            del self.hit_list[i]

        self.success_list = []

    def hit(self, success=False):
        if self.finished:
            raise RuntimeError
        else:
            if success:
                if self.hit_list[self.cur_player]['удар'] == 0:
                    self.score_list[self.cur_hole][self.hit_list[self.cur_player]['номер']] = 1
                # если игрок попал не с первого раза
                else:
                    self.score_list[self.cur_hole][self.hit_list[self.cur_player]['номер']] = self.hit_list[self.cur_player]['удар'] + 1
                self.success_list.append(self.cur_player)
            else:
                self.hit_list[self.cur_player]['удар'] += 1
                # если он и на 9 раз не попал
                if self.hit_list[self.cur_player]['удар'] == 9:
                    self.score_list[self.cur_hole][self.hit_list[self.cur_player]['номер']] = 10
                    self.success_list.append(self.cur_player)

            self.cur_player += 1

            if self.cur_player == len(self.hit_list):

                if self.success_list:
                    self.cleaning_players()

                    if not self.hit_list:
                        self.change_hole()

                self.cur_player = 0

    def get_winners(self):
        if self.finished:
            final_score = {i: sum([row[i] for row in self.score_list]) for i in range(len(self.score_list))}
            return [self.players[player] for player, score in final_score.items() if score == min(final_score.values())]
        else:
            raise RuntimeError


class HolesMatch(Match):
    def __init__(self,holes,players):
        super().__init__(holes,players)
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

    def hit(self, success=False):
        if self.finished:
            raise RuntimeError
        else:
            if success:
                # если удар успешный, записали очко в таблицу и зафиксировали попадание
                self.score_list[self.cur_hole][self.player_change[self.cur_player]] = 1
                self.flag_hit = True

            # в конце удара переходим к следующему игроку
            self.cur_player += 1

            # если все уже ударили, ход переходит к 1ому и переход на следующую лунку и меняем очерёдность игроков
            if self.cur_player == len(self.players):
                # если есть попадание
                if self.flag_hit:
                    self.change_round()
                    # у тех кто не забил, ставим 0
                    for i in range(self.holes):
                        if self.score_list[self.cur_hole][i] is None:
                            self.score_list[self.cur_hole][i] = 0

                    self.change_hole()
                    if self.cur_hole == self.holes:
                        self._finished = True

                # если никто не забил, начинаем новый круг с 1ого игрока
                else:
                    self.cur_player = 0
                    self.round += 1
                    # если это уже 10ый круг, то всем ставим 0 очков и переход на следующую лунку
                    if self.round == 10:
                        for i in range(self.holes):
                            self.score_list[self.cur_hole][i] = 0
                        self.change_hole()

            if self.cur_hole == self.holes and self.cur_player == len(self.players):
                self._finished = True

    def get_winners(self):
        if self.finished:
            final_score = {i: sum([row[i] for row in self.score_list]) for i in range(len(self.score_list))}
            return [self.players[player] for player, score in final_score.items() if score == max(final_score.values())]
        else:
            raise RuntimeError