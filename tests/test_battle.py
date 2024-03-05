from unittest import TestCase
from unittest.mock import patch

from src.battle import Battle


class TestBattle(TestCase):

    def setUp(self):
        self.battle = Battle()
        self.battle.opponent_board = [[0 for _ in range(10)] for _ in range(10)]
        self.battle.opponent_ships = []
        self.battle.used_coordinates = []
        self.battle.sinking_opponent_ship = []
        self.battle.sinking_player_ship = []
        self.battle.player_ships_sunk = 0
        self.battle.opponent_ships_sunk = 0
        self.battle.end = False

    def test_create_opponent(self):
        self.battle.create_opponent()
        self.assertEqual(len(self.battle.opponent_ships), 11)

    def test_opponent_attack_sinking_player_ship_len_2(self):
        player_board = [[1 for _ in range(10)] for _ in range(10)]
        player_ships = [[5, 5, 2], [4, 5, 2], [6, 5, 2], [5, 4, 2], [5, 6, 2]]

        self.battle.sinking_player_ship.append([5, 5, 1])
        self.battle.opponent_attack(player_board, player_ships)

        self.assertEqual(len(self.battle.sinking_player_ship), 0)
        self.assertEqual(self.battle.player_ships_sunk, 1)

    @patch('random.randint', side_effect=[9, 1])
    def test_opponent_attack_sinking_player_ship_len_1(self, mock_randint):
        player_board = [[0 for _ in range(10)] for _ in range(9)]
        player_board.append([0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        player_ships = [[9, 1, 1]]

        self.battle.opponent_attack(player_board, player_ships)

        self.assertEqual(len(self.battle.sinking_player_ship), 0)
        self.assertEqual(self.battle.player_ships_sunk, 1)

    def test_opponent_attack_sinking_player_ship_len_3(self):
        player_board = [[0 for _ in range(10)] for _ in range(9)]
        player_board.append([0, 1, 1, 1, 0, 0, 0, 0, 0, 0])
        player_ships = [[9, 1, 3], [9, 2, 3], [9, 3, 3]]

        self.battle.sinking_player_ship = [[9, 1, 3], [9, 2, 3]]
        self.battle.opponent_attack(player_board, player_ships)

        self.assertEqual(len(self.battle.sinking_player_ship), 0)
        self.assertEqual(self.battle.player_ships_sunk, 1)
        self.assertEqual(player_board[9][3], 'X')

    @patch('random.randint', side_effect=[0, 0])
    def test_opponent_attack_miss(self, mock_randint):
        player_board = [[0, 1]]
        player_ships = []

        self.battle.opponent_attack(player_board, player_ships)

        self.assertEqual(player_board[0][0], '+')

    @patch('random.randint', side_effect=[9, 1])
    @patch('src.opponent_move.check_direction', return_value=3)
    def test_opponent_attack_second_attack(self, mock_random, mock_direction):
        player_board = [[0 for _ in range(10)] for _ in range(9)]
        player_board.append([0, 1, 1, 1, 0, 0, 0, 0, 0, 0])
        player_ships = [[9, 1, 2], [9, 2, 2]]

        self.battle.opponent_attack(player_board, player_ships)

        self.assertEqual(len(self.battle.sinking_player_ship), 0)
        self.assertEqual(self.battle.player_ships_sunk, 1)
        self.assertEqual(player_board[9][1], 'X')

    def test_player_attack_hit_and_sunk(self):
        temp_board = [[0 for _ in range(10)] for _ in range(9)]
        temp_board.append([0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        self.battle.opponent_ships = [[9, 1, 1]]
        self.battle.opponent_board = temp_board

        response = self.battle.player_attack([9, 1])

        self.assertFalse(response)
        self.assertEqual(self.battle.opponent_ships_sunk, 1)
        self.assertEqual(self.battle.sinking_opponent_ship, [])

    def test_player_attack_hit_and_second_attack(self):
        temp_board = [[0 for _ in range(10)] for _ in range(9)]
        temp_board.append([0, 1, 1, 0, 0, 0, 0, 0, 0, 0])
        self.battle.opponent_ships = [[9, 1, 2]]
        self.battle.opponent_board = temp_board

        response = self.battle.player_attack([9, 1])

        self.assertTrue(response)
        self.assertEqual(len(self.battle.sinking_opponent_ship), 1)

    def test_player_attack_miss(self):
        response = self.battle.player_attack([9, 1])

        self.assertFalse(response)
        self.assertEqual(self.battle.opponent_board[9][1], '+')

