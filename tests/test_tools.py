import sys
from io import StringIO

from src.tools import increment, is_game_over


def test_increment():
    assert increment(2, 2) == 1
    assert increment(2, 1) == 3


def test_is_game_over_player_won():
    captured_output = StringIO()
    sys.stdout = captured_output
    assert is_game_over(11, 0) is False
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue() == '\nCONGRATULATIONS YOU HAVE WON !\n\n'


def test_is_game_over_player_lost():
    captured_output = StringIO()
    sys.stdout = captured_output
    assert is_game_over(0, 11) is False
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue() == '\nGAME OVER, YOU HAVE LOST.\n\n'


def test_is_game_over_game_not_over():
    assert is_game_over(1, 1) is True
