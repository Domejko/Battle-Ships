import pytest
from unittest.mock import patch
from src.opponent_move import check_coordinates, check_direction, initiate_move, move, move_or_go_back


def test_check_coordinates_empty_list():
    assert check_coordinates([9, 1], []) is False


def test_check_coordinates_coord_found():
    assert check_coordinates([9, 1], [[9, 1]]) is True


def test_check_coordinates_coord_not_found():
    assert check_coordinates([9, 1], [[4, 2]]) is False


def test_check_direction_dir_not_none():
    assert check_direction([4, 4], 2) == 2


def test_check_direction_left_boundary():
    for _ in range(10):
        assert check_direction([0, 4], None) != 2


def test_check_direction_right_boundary():
    for _ in range(10):
        assert check_direction([9, 4], None) != 1


def test_check_direction_upper_boundary():
    for _ in range(10):
        assert check_direction([4, 0], None) != 4


def test_check_direction_lower_boundary():
    for _ in range(10):
        assert check_direction([4, 9], None) != 3


def test_check_direction_upper_corners():
    left_corner = [1, 3]
    right_corner = [1, 4]
    for _ in range(10):
        assert check_direction([0, 0], None) in left_corner
        assert check_direction([0, 9], None) in right_corner


def test_check_direction_lower_corners():
    left_corner = [2, 3]
    right_corner = [2, 4]
    for _ in range(10):
        assert check_direction([9, 0], None) in left_corner
        assert check_direction([9, 9], None) in right_corner


@patch('src.opponent_move.move', return_value=[False, None])
def test_initiate_move(mock_move):
    assert initiate_move(mock_move, [[0]], [1, 1], [[]], [], 1) == [False, None]
    mock_move.assert_called_once()


@patch('src.opponent_move.check_coordinates', return_value=True)
def test_move_duplicate_coordinates(mock_check):
    with pytest.raises(IndexError):
        move([[]], [], [], [], 1, None)


def test_move_hit():
    test_board = [[1]]
    test_coord_list = []
    assert move(test_board, [0, 0], test_coord_list, [], 1, None) == [False, None]
    assert test_board[0][0] == 'X'
    assert len(test_coord_list) == 1


def test_move_miss():
    test_board = [[0]]
    test_used_coord = []
    assert move(test_board, [0, 0], [], test_used_coord, 1, None) == [False, None]
    assert test_board[0][0] == '+'
    assert len(test_used_coord) == 1


def test_move_or_go_back():
    test_board = [[1]]
    test_coord_list = []
    test_used_cord = []
    assert move_or_go_back(test_board, [0, 0], test_coord_list, test_used_cord, 1, 2) == [False, None]
    assert test_board[0][0] == 'X'
    assert test_coord_list == [[0, 0, 1]]
    assert test_used_cord == [[0, 0]]


def test_move_or_go_back_change_direction():
    test_board = [[0]]
    test_used_coord = []
    test_coord_list = [[4, 4]]
    assert move_or_go_back(test_board, [0, 0], test_coord_list, test_used_coord, 1, 2) == [False, True]
    assert test_board[0][0] == '+'
    assert test_used_coord == [[0, 0]]
    assert test_coord_list == [[4, 4, 2]]
