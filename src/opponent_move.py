from random import randint, choice
from time import sleep
from typing import Callable

from src.tools import COLUMN_DICT


def check_coordinates(coordinates: list, used_coordinates: list[list]) -> bool:
    """
    Description:
        The function check_coordinates takes in two parameters: coordinates, which is a list of
        coordinates to be checked, and coordinates_list, which is a list of lists containing other coordinates.
        It returns a boolean value indicating whether the given coordinates are present in the coordinates_list.
        If the coordinates_list is empty, the function returns False.

    :param coordinates: List of coordinates to check.
    :param used_coordinates: List of list containing coordinates that already have been used.
    :return: boolean
    """
    if len(used_coordinates) == 0:
        return False
    else:
        for cor in used_coordinates:
            if coordinates == cor:
                return True
        return False


def check_direction(ship_coord: list, direction: int | None) -> int:
    """
    Description:
        The function check_direction takes in two parameters: ship_coord, which is a list representing
        the current ship coordinates, and direction, which is an integer representing the current attack direction.
        If the direction is None and the ship's coordinates are not at the edges of the board,
        a random integer between 1 and 4 is generated as the next_move_direction. If the direction
        is None and the ship's coordinates are at the leftmost edge of the board, the next_move_direction
        is randomly chosen from 1, 3, or 4. Similar logic is applied for other edges of the board.
        If the direction is not None, it is assigned as the next_move_direction. The function returns
        the next_move_direction.

    :param ship_coord: List of attack coordinates.
    :param direction: Integer representing direction of attack.
    :return: integer
    """
    if direction is None:
        if ship_coord[0] == 9 and ship_coord[1] == 9:
            direction = choice([2, 4])
        elif ship_coord[0] == 0 and ship_coord[1] == 0:
            direction = choice([1, 3])
        elif ship_coord[0] == 9 and ship_coord[1] == 0:
            direction = choice([2, 3])
        elif ship_coord[0] == 0 and ship_coord[1] == 9:
            direction = choice([1, 4])
        elif ship_coord[1] == 0:
            direction = choice([1, 2, 3])
        elif ship_coord[1] == 9:
            direction = choice([1, 2, 4])
        elif ship_coord[0] == 0:
            direction = choice([1, 3, 4])
        elif ship_coord[0] == 9:
            direction = choice([2, 3, 4])
        else:
            direction = randint(1, 4)

    return direction


def initiate_move(func: Callable, board: list[list], ship_coord: list, used_coord_list: list[list],
                  ship_coord_list: list, direction: int = None) -> list[bool, bool | None]:
    """
    Description:
        The function initiate_move takes in multiple parameters including a func which is a
        Callable object representing the move function, a board list, ship_coord list, used_coord_list list,
        ship_coord_list list, and an optional direction integer parameter. It initializes a flag
        list with the values [True, None]. The function enters a while loop with the condition flag[0]
        until the flag[0] is False. Inside the loop, it calls the check_direction function to get the
        next_move_direction. It then uses the next_move_direction to call the func function with
        appropriate parameters. The func function modifies the flag list. If an IndexError occurs,
        the loop continues. The function returns the flag list.

    :param func: Callable function move or move_or_go_back
    :param board: List of list representing a 10x10 grid battlefield.
    :param ship_coord: List containing sinking ship coordinates.
    :param used_coord_list: List of lists containing already used coordinates.
    :param ship_coord_list: List or list containing coordinates of sinking ship.
    :param direction: Integer representing direction of the attack.
    :return: boolean
    """
    flag = [True, None]

    while flag[0]:
        next_move_direction = check_direction(ship_coord, direction)
        try:
            match next_move_direction:
                case 1:
                    flag = func(board, [ship_coord[0] + 1, ship_coord[1]], ship_coord_list, used_coord_list,
                                next_move_direction, 2)
                case 2:
                    flag = func(board, [ship_coord[0] - 1, ship_coord[1]], ship_coord_list, used_coord_list,
                                next_move_direction, 1)
                case 3:
                    flag = func(board, [ship_coord[0], ship_coord[1] + 1], ship_coord_list, used_coord_list,
                                next_move_direction, 4)
                case 4:
                    flag = func(board, [ship_coord[0], ship_coord[1] - 1], ship_coord_list, used_coord_list,
                                next_move_direction, 3)
        except IndexError:
            continue
    return flag


def move(board: list, ship_coord: list, ship_coord_list: list, used_coord_list: list[list], direction: int, _: None) \
        -> list[bool, None]:
    """
    Description:
        The move function takes in board, ship_coord, ship_coord_list, used_coord_list,
        direction, and a _ parameter (which is ignored). It checks if the ship_coord is
        present in the used_coord_list using the check_coordinates function. If it is present,
        an IndexError is raised. If the value at the ship_coord on the board is 1, it is
        replaced with 'X', ship_coord_list is updated with the ship's current position and
        direction, and the function returns [False, None]. If the value at the ship_coord
        on the board is not 'X', it is replaced with '+'. The ship_coord is appended to the
        used_coord_list and the function returns [False, None].

    :param board: List of list representing a 10x10 grid battlefield.
    :param ship_coord: List containing sinking ship coordinates.
    :param ship_coord_list: List or list containing coordinates of sinking ship.
    :param used_coord_list: List of lists containing already used coordinates.
    :param direction: Integer representing direction of the attack.
    :param _: Empty parameter not used in this function.
    :return: List of bool and None
    """
    if check_coordinates([ship_coord[0], ship_coord[1]], used_coord_list):
        raise IndexError
    elif board[ship_coord[0]][ship_coord[1]] == 1:
        board[ship_coord[0]][ship_coord[1]] = 'X'
        ship_coord_list.append([ship_coord[0], ship_coord[1], direction])
        print(f'\nEnemy have hit your ship at {COLUMN_DICT[ship_coord[0]], ship_coord[1] + 1}')
        sleep(3)

        return [False, None]
    else:
        if board[ship_coord[0]][ship_coord[1]] != 'X':
            board[ship_coord[0]][ship_coord[1]] = '+'
    used_coord_list.append([ship_coord[0], ship_coord[1]])

    return [False, None]


def move_or_go_back(board: list, ship_coord: list, ship_coord_list: list, used_coord_list: list[list], direction: int,
                    turn_around: int) -> list[bool] | list[bool, None]:
    """
    Description:
        The move_or_go_back function takes in several parameters similar to the move function
        along with an additional turn_around parameter. If the value at the ship_coord on the
        board is 1, it is replaced with 'X', ship_coord_list is updated with the ship's current
        position and direction, and the ship_coord is appended to the used_coord_list. If the
        value is not 1, the turn_around value is appended to the ship_coord_list which is changing
        the direction of next attack. If the value at the ship_coord on the board is not 'X',
        it is replaced with '+'. The ship_coord is appended to the used_coord_list and the
        function returns [False, True]. If the conditions are not met, the function returns [False, None].

    :param board: List of list representing a 10x10 grid battlefield.
    :param ship_coord: List containing sinking ship coordinates.
    :param ship_coord_list: List or list containing coordinates of sinking ship.
    :param used_coord_list: List of lists containing already used coordinates.
    :param direction: Integer representing direction of the attack.
    :param turn_around: Integer representing opposite direction of the attack from the current one.
    :return: List of bool and None or bool and bool
    """
    if ship_coord[0] == 10:
        ship_coord[0] -= 1
    elif ship_coord[0] == -1:
        ship_coord[0] += 1
    elif ship_coord[1] == 10:
        ship_coord[1] -= 1
    elif ship_coord[1] == -1:
        ship_coord[1] += 1

    if board[ship_coord[0]][ship_coord[1]] == 1:
        board[ship_coord[0]][ship_coord[1]] = 'X'
        ship_coord_list.append([ship_coord[0], ship_coord[1], direction])
        used_coord_list.append([ship_coord[0], ship_coord[1]])
        print(f'\nEnemy have hit your ship at {COLUMN_DICT[ship_coord[0]], ship_coord[1] + 1}')
        sleep(3)
    else:
        ship_coord_list[0].append(turn_around)
        if board[ship_coord[0]][ship_coord[1]] != 'X':
            board[ship_coord[0]][ship_coord[1]] = '+'
        used_coord_list.append([ship_coord[0], ship_coord[1]])
        return [False, True]

    return [False, None]
