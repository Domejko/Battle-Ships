import unittest
from unittest.mock import patch, Mock

import src.ship
from src.player import Player


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    def tearDown(self):
        del self.player

    @patch('builtins.input', return_value='y')
    def test_auto_generate_prompt_return_true(self, mock_input):
        src.ship.auto_generate_ships = Mock()
        self.player.auto_generate_prompt()
        src.ship.auto_generate_ships.assert_called_once()

    @patch('builtins.input', return_value='n')
    def test_auto_generate_prompt_return_false(self, mock_input):
        self.player.manual_generate_ship = Mock()
        self.player.auto_generate_prompt()
        self.player.manual_generate_ship.assert_called_once()

    @patch('builtins.input', return_value='h')
    def test_print_error_message_on_invalid_input(self, mock_input):
        self.player.auto_generate_prompt = Mock()
        self.player.auto_generate_prompt()
        self.player.auto_generate_prompt.assert_called_once()

    @patch('builtins.input', return_value='foo')
    def test_get_column_invalid_input(self, mock_input):
        self.player.manual_generate_prompt = Mock()
        result = self.player.get_column()
        assert result is False

    @patch('builtins.input', return_value='a')
    def test_get_column_valid_input(self, mock_input):
        result = self.player.get_column()
        assert result == 'A'

    @patch('builtins.input', return_value='bar')
    def test_get_row_invalid_input(self, mock_input):
        self.player.manual_generate_prompt = Mock()
        result = self.player.get_row()
        assert result is False

    @patch('builtins.input', return_value='1')
    def test_get_row_valid_input(self, mock_input):
        result = self.player.get_row()
        assert result == '1'

    @patch('builtins.input', side_effect='baz')
    def test_get_direction_invalid_input(self, mock_input):
        self.player.manual_generate_prompt = Mock()
        result = self.player.get_direction()
        assert result is False

    @patch('builtins.input', return_value='right')
    def test_get_direction_valid_input(self, mock_input):
        result = self.player.get_direction()
        assert result == 'RIGHT'

    @patch('builtins.input', side_effect=['help', 1, 'up'])
    def test_manual_generate_prompt_help(self, mock_input):
        self.player.help = Mock()
        self.player.manual_generate_prompt()
        self.player.help.assert_called_once()

    @patch('builtins.input', return_value='Q')
    def test_help_quit(self, mock_input):
        self.player.manual_generate_prompt = Mock()
        self.player.help()
        self.player.manual_generate_prompt.assert_called_once()

    @patch('src.player.Player.player_ships', return_value=[1 for _ in range(10)])
    @patch('src.ship.create_ship', return_value=True)
    @patch('src.player.Player.manual_generate_prompt', return_value=('C', 1, 'DOWN'))
    def test_manual_generate_ship(self, mock_ships, mock_create, mock_prompt):
        self.player.manual_generate_ship()
        mock_create.assert_called()
        self.assertTrue(self.player.manual_generate_ship)

    @patch('builtins.input', side_effect=['B 5'])
    def test_attack_coordinates(self, mock_input):
        self.assertEqual(self.player.attack_coordinates(), [1, 4])
