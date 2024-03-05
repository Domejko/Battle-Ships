from unittest.mock import patch

from src.ship import (check_position_free, check_position, create_ship, auto_generate_ships,
                      check_if_ship_destroyed)


def create_test_board():
    empty = [[0 for _ in range(10)] for _ in range(10)]
    full = [[1 for _ in range(10)] for _ in range(10)]

    return empty, full


def test_check_position_free_pos_taken():
    _, board = create_test_board()
    assert check_position_free(4, 4, 2, 3, board) is False


def test_check_position_free_pos_free():
    board, _ = create_test_board()
    assert check_position_free(4, 4, 2, 3, board) is True


def test_check_position_free_corner_taken():
    temp = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    board = [[0 for _ in range(10)] for _ in range(9)]
    board.append(temp)
    assert check_position_free(9, 1, 2, 1, board) is False


@patch('src.ship.check_position_free', return_value=False)
def test_check_position_pos_taken(mock):
    assert check_position(4, 4, 2, 3, [[]]) is False
    assert check_position(4, 4, 4, 3, [[]]) is False


@patch('src.ship.check_position_free', return_value=True)
def test_check_position_pos_free(mock):
    assert check_position(4, 4, 2, 3, [[]]) is True


def test_create_ship():
    board, _ = create_test_board()
    assert create_ship(board, [4, 4], 3, 3) is True
    assert board[3][3] == 1
    assert board[3][4] == 1
    assert board[3][5] == 1


def test_auto_generate_ships():
    board, _ = create_test_board()
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1]
    test_ships_list = []
    auto_generate_ships(board, ships, test_ships_list)

    assert len(test_ships_list) == 11


@patch('src.ship.destroyed_ship_outline_coords', return_value=True)
def test_check_if_ship_destroyed_ship_destroyed(mock):
    ships_list = [[4, 4, 1]]
    coordinates = [[4, 4]]
    used_coord = []

    assert check_if_ship_destroyed(ships_list, coordinates, [[]], used_coord) is True


def test_check_if_ship_destroyed_ship_not_destroyed():
    ships_list = [[4, 4, 3]]
    coordinates = [[4, 4]]
    used_coord = []

    assert check_if_ship_destroyed(ships_list, coordinates, [[]], used_coord) is False
