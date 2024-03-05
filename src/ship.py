from random import randint
import contextlib

from src.tools import increment


def check_position_free(col: int, row: int, direction: int, ship_size: int, board: list[list]) -> bool:
    """
    Description:
        This function checks if a ship can be placed on the board starting from the given column
        and row coordinates. It takes into account the ship's size and checks for any neighboring
        ships. It returns True if the ship can be placed in the given position, otherwise False.

    :param col: Integer representing a column on the board.
    :param row: Integer representing a row on the board.
    :param direction: Integer representing a direction in which ship will be extended.
    :param ship_size: Integer representing a size of the ship.
    :param board: List of list representing a 10x10 grid battlefield.
    :return: boolean
    """
    x = col
    y = row
    for _ in range(ship_size):
        try:
            if board[x][y] == 1:
                return False
        except IndexError:
            pass
        try:
            if board[x][y + 1] == 1:
                return False
        except IndexError:
            pass
        try:
            if board[x][y - 1] == 1:
                return False
        except IndexError:
            pass
        try:
            if board[x - 1][y] == 1:
                return False
        except IndexError:
            pass
        try:
            if board[x + 1][y] == 1:
                return False
        except IndexError:
            pass
        try:
            if board[x - 1][y + 1] == 1:
                return False
        except IndexError:
            pass
        try:
            if board[x + 1][y + 1] == 1:
                return False
        except IndexError:
            pass
        try:
            if board[x - 1][y - 1] == 1:
                return False
        except IndexError:
            pass
        try:
            if board[x + 1][y - 1] == 1:
                return False
        except IndexError:
            pass

        if direction in [1, 2]:
            x = increment(x, direction)
        elif direction in [3, 4]:
            y = increment(y, direction)

    return True


def check_position(col: int, row: int, direction: int, ship_size: int, board: list[list]) -> bool:
    """
    Description:
        This function checks if a ship can be placed on the board at the given row and column
        coordinates in the given direction. It checks for sufficient space and calls either
        check_vertical or check_horizontal based on the direction. It returns True if the ship
        can be placed in the given position, otherwise False.

    :param row: Integer representing a row on the board.
    :param col: Integer representing a column on the board.
    :param direction: Integer representing a direction in which ship will be extended.
    :param ship_size: Integer representing a size of the ship.
    :param board: List of list representing a 10x10 grid battlefield.
    :return: boolean
    """
    row_space_left = 10 - (row + 1)
    col_space_left = 10 - (col + 1)

    if direction == 1 and col_space_left >= ship_size:
        if not check_position_free(col, row, direction, ship_size, board):
            return False
    elif direction == 2 and col >= ship_size:
        if not check_position_free(col, row, direction, ship_size, board):
            return False
    elif direction == 3 and row_space_left >= ship_size:
        if not check_position_free(col, row, direction, ship_size, board):
            return False
    elif direction == 4 and row >= ship_size:
        if not check_position_free(col, row, direction, ship_size, board):
            return False
    else:
        return False

    return True


def create_ship(board: list[list], coordinates: list, ship_size: int, direction: int) -> bool:
    """
    Description:
        This function creates a ship on the board starting from the given coordinates. It
        updates the board with 1s representing the ship's position. It also updates the
        row or column position based on the given direction. It returns True if the ship
        creation is successful, otherwise False.

    :param board: List of list representing a 10x10 grid battlefield.
    :param coordinates: List of coordinates where ship is supposed to be placed.
    :param ship_size: Integer representing a size of the ship.
    :param direction: Integer representing a direction in which ship will be extended.
    :return: boolean
    """
    col_pos = coordinates[0] - 1
    row_pos = coordinates[1] - 1

    for _ in range(ship_size):
        board[col_pos][row_pos] = 1
        if direction in [1, 2]:
            col_pos = increment(col_pos, direction)
        else:
            row_pos = increment(row_pos, direction)

    return True


def auto_generate_ships(board: list[list], ships: list, ship_list: list) -> None:
    """
    Description:
        This function automatically generates ships on the board using random coordinates
        and directions. It ensures that ships are not placed on top of each other or outside
        the bounds of the board. It updates the board and the ship list with the generated ships.

    :param board: List of list representing a 10x10 grid battlefield.
    :param ships: Integer list representing number of ships and there size.
    :param ship_list: List of list where each list contains single initial coordinates of
                    the ship and it's size.
    :return: None
    """
    used_coordinates = []
    coordinates = []

    for ship in ships:
        flag = False

        while not flag:
            coordinates = [randint(1, 10), randint(1, 10)]
            direction = randint(1, 4)
            if coordinates not in used_coordinates and check_position(coordinates[0] - 1, coordinates[1] - 1,
                                                                      direction, ship, board) is True:
                flag = create_ship(board, coordinates, ship, direction)
                temp_list = [coordinates[0] - 1, coordinates[1] - 1, ship]
                ship_list.append(temp_list)

        used_coordinates.append(coordinates)


def check_if_ship_destroyed(ships_list: list[list], coordinates: list[list], sinking_ship: list[list],
                            used_coordinates: list[list] | None) -> bool:
    """
    Description:
        This function checks if a ship has been destroyed based on the current hits on its coordinates.
        It iterates through the ship list and coordinate list to find matching ships. If the number
        of hits on a ship's coordinates matches its size, the ship is considered destroyed. It returns
        True if the ship has been destroyed, otherwise False.

    :param used_coordinates: List of lists containing already used coordinates.
    :param ships_list: List of list where each list contains single initial coordinates of
                    the ship and it's size.
    :param coordinates: List of lists containing attack coordinates in a given turn.
    :param sinking_ship: List of lists coordinates representing ship that is currently being sunk.
    :return: boolean
    """
    for ship in ships_list:
        for coord in coordinates:
            if len(coord) == 2:
                if coord == ship[:2]:
                    if ship[2] == len(sinking_ship):
                        destroyed_ship_outline_coords(sinking_ship, used_coordinates)
                        return True
            elif len(coord) == 3:
                if coord[:2] == ship[:2]:
                    if ship[2] == len(sinking_ship):
                        destroyed_ship_outline_coords(sinking_ship, used_coordinates)
                        return True
    return False


def destroyed_ship_outline_coords(sinking_ship: list[list], used_coordinates: list[list] | None) -> None:
    """
    Description:
        The function append to the list of already used coordinates, coordinates around already
        destroyed ship.

    :param sinking_ship: List of lists coordinates representing ship that is currently being sunk.
    :param used_coordinates: List of lists containing already used coordinates.
    """
    if used_coordinates is not None:
        for coord in sinking_ship:
            used_coordinates.append([coord[0] + 1, coord[1]])
            used_coordinates.append([coord[0] - 1, coord[1]])
            used_coordinates.append([coord[0], coord[1] + 1])
            used_coordinates.append([coord[0], coord[1] - 1])
            used_coordinates.append([coord[0] - 1, coord[1] - 1])
            used_coordinates.append([coord[0] + 1, coord[1] - 1])
            used_coordinates.append([coord[0] + 1, coord[1] + 1])
            used_coordinates.append([coord[0] - 1, coord[1] + 1])



