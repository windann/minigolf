import unittest
from minigolf import Match, HitsMatch, HolesMatch, Player
from collections import deque


class PlayerTestCase(unittest.TestCase):
    def test_init(self):
        p = Player('A')

        self.assertEqual(p.name, 'A')

    def test_str(self):
        p = Player('A')

        self.assertEqual(str(p), 'Игрок: A')


class MatchTestCase(unittest.TestCase):

    def test_init(self):
        players = [Player('A'), Player('B'), Player('C')]
        m = Match(3, players)

        self.assertEqual(m.holes, 3)
        self.assertEqual(m.players, players)
        self.assertEqual(m._finished, False)
        self.assertEqual(m.score_list, [[None, None, None], [None, None, None], [None, None, None]])

    def test_get_table(self):
        players = [Player('A'), Player('B'), Player('C')]
        m = Match(3, players)

        table = m.get_table()
        self.assertEqual(table, [('A', 'B', 'C'), (None, None, None), (None, None, None), (None, None, None)])

    def test_finished(self):
        players = [Player('A'), Player('B'), Player('C')]
        m = Match(3, players)

        self.assertEqual(m.finished, False)


class HitsMatchTestCase(unittest.TestCase):

    def test_init(self):
        pass

    def test_cleaning_players(self):
        pass

    def test_hit(self):
        players = [Player('A'), Player('B'), Player('C')]
        m = HitsMatch(3, players)
        m.hit(True)

        self.assertEqual(m.finished, False)

        with self.assertRaises(RuntimeError):
            m.get_winners()

    def test_change_hole(self):
        players = [Player('A'), Player('B'), Player('C')]
        m = HitsMatch(3, players)
        m.change_hole()
        self.assertEqual(m.hit_list,deque([{'номер': 1,'удар': 0},{'номер': 2,'удар': 0},{'номер': 0,'удар': 0}]))


class HolesMatchTestCase(unittest.TestCase):

    def test_init(self):
        players = [Player('A'), Player('B')]
        m = HolesMatch(4, players)
        m.hit(True)
        self.assertEqual(m.flag_hit, True)
        self.assertEqual(m.round, 0)
        self.assertEqual(m.player_change, deque([0,1]))

    def test_change_hole(self):
        players = [Player('A'), Player('B')]
        m = HolesMatch(4, players)
        m.change_hole()
        self.assertEqual(m.cur_hole,1)
        self.assertEqual(m.player_change,deque([1,0]))

    def test_change_round(self):
        players = [Player('A'), Player('B')]
        m = HolesMatch(4, players)
        m.hit()
        m.hit()
        self.assertEqual(m.round,1)

    def test_hit(self):
        players = [Player('A'), Player('B')]
        m = HolesMatch(2, players)
        for _ in range(10):
            m.hit()
            m.hit()

        self.assertEqual(m.score_list,[[0,0],[None,None]])

    def test_get_winners(self):
        players = [Player('A'), Player('B')]
        m = HolesMatch(2, players)
        m.hit()
        m.hit(True)
        m.hit(True)
        m.hit()
        self.assertEqual(m.get_winners(),[players[1]])