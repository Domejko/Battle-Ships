import os
from time import sleep
from typing import Any

import src.ship
from src.tools import print_single_board, clear_cmd


class Player:
    """
    Description:
        The Player class represents a player in a game. It contains methods for generating ships,
        getting attack coordinates, and providing help instructions.

    Attributes:
        COLUMN_DICT (dict): dictionary mapping character represented columns with a number in order.
        DIRECTION_DICT (dict): dictionary mapping direction with a number representing it.
        SHIPS (list): integer list representing number of ships and there size.
        board (list): list of list representing a 10x10 grid battlefield.
        player_ships (list): list of list where each list contains single initial coordinates of
                                the ship and it's size.

    Methods:
        auto_generate_prompt: Prompts the user whether they want to automatically generate their ships.
        If the input is 'Y', it clears the screen and calls the auto_generate_ships method from the ship module,
        passing in the board, list of ships, and player_ships as arguments. If the input is 'N', it calls the
        manual_generate_ship method. If the input is neither 'Y' nor 'N', it raises a ValueError and displays
        an error message before prompting the user again.

        get_column: Prompts the user to input a column letter (A-J). It checks whether the input is valid,
        and if not, it clears the screen, displays an invalid column error message, waits for 3 seconds,
        and calls the manual_generate_prompt method.

        get_row: Prompts the user to input a row number (1-10). It checks whether the input is valid,
        and if not, it clears the screen, displays an invalid row error message, waits for 3 seconds,
        and calls the manual_generate_prompt method.

        get_direction: Prompts the user to input a direction (up/down/left/right). It checks whether the input
        is valid, and if not, it clears the screen, displays an invalid direction error message, waits for 3 seconds,
        and calls the manual_generate_prompt method.

        manual_generate_prompt: Prints the current state of the board and prompts the user to give starting
        coordinates for their ship and the direction in which it should extend. It provides information about
        the ship generating order and allows the user to type 'help' to see an example. It calls the get_column,
        get_row, and get_direction methods to get the user input and returns them as a tuple.

        help: Displays an example of how to input starting coordinates and direction for generating ships.
        It prints the example board and prompts the user to type 'q' to go back to the manual_generate_prompt method.

        manual_generate_ship: Generates ships manually by iterating over the list of ships. It calls the
        manual_generate_prompt method to get the coordinates and direction from the user. It checks if the
        coordinates have been used before and if the ship can be placed at the given coordinates. If the
        conditions are met, it creates the ship on the board and adds the coordinates to the player_ships list.
        It returns True when all ships have been generated.

        attack_coordinates: Prompts the user to input the coordinates where they want to attack. It checks whether
        the input is valid (a letter from A-J followed by a number from 1-10). If the input is invalid, it displays
        an error message and prompts the user again. Finally, it converts the input into column and row coordinates
        and returns them as a list.
    """
    COLUMN_DICT = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10}
    DIRECTION_DICT = {'UP': 4, 'DOWN': 3, 'LEFT': 2, 'RIGHT': 1}
    SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1]

    board = [[0 for _ in range(10)] for _ in range(10)]
    player_ships = []

    def auto_generate_prompt(self) -> Any:
        while True:
            generate = input('Do you want to automatically generate your ships ? (Y/N): ').upper()

            try:
                if generate in ['Y', 'N'] and generate == 'Y':
                    os.system(clear_cmd)
                    return src.ship.auto_generate_ships(self.board, self.SHIPS, self.player_ships)
                elif generate in ['Y', 'N'] and generate == 'N':
                    return self.manual_generate_ship()
                else:
                    os.system(clear_cmd)
                    raise ValueError
            except ValueError:
                print('Incorrect input. Only Y or N')
                sleep(3)

    def get_column(self) -> str | bool:
        col = input('Column (A-J): ').upper()
        if col not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'HELP']:
            os.system(clear_cmd)
            print('Invalid column! Only character (A-J) or (help). Please try again.')
            sleep(3)
            os.system(clear_cmd)
            return False

        return col

    def get_row(self) -> str | bool:
        row = input('Row (1-10): ')
        if row not in [str(i) for i in range(1, 11)]:
            os.system(clear_cmd)
            print('Invalid row! Only numbers in range (1-10). Please try again.')
            sleep(3)
            os.system(clear_cmd)
            return False

        return row

    def get_direction(self) -> str | bool:
        direction = input('Direction (up/down/left/right): ').upper()
        if direction not in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'HELP']:
            os.system(clear_cmd)
            print('Invalid direction! Only up, down, left and right. Please try again.')
            sleep(3)
            os.system(clear_cmd)
            return False

        return direction

    def manual_generate_prompt(self) -> tuple[str, int, str] | Any:

        print_single_board(self.board)
        print('\n')
        print('Give a starting coordinates for your ship and direction in which it supposed to extent.\n'
              'Ship generating order is as follows, one of size 4, two of size 3, three of size 2 and fife of'
              ' size 1.\n'
              'If you want to see and example type help.\n')

        col = self.get_column()
        if col == 'HELP':
            return self.help()
        elif col is False:
            return False

        row = self.get_row()
        if row is False:
            return False

        direction = self.get_direction()
        if direction is False:
            return False

        return col, int(row), direction

    def help(self) -> None:
        while True:
            os.system(clear_cmd)
            print('Example:\n'
                  '\n'
                  'Column (A-J): B                                    Column (A-J): D\n'
                  'Row (1-10): 5                                      Row (1-10): 2\n'
                  'Direction (up/down/left/right): down               Direction (up/down/left/right): right\n'
                  '\n'          
                  '    A  B  C  D  E  F  G  H  I  J                      A  B  C  D  E  F  G  H  I  J\n'
                  ' 1  -  -  -  -  -  -  -  -  -  -                   1  -  -  -  -  -  -  -  -  -  -\n'
                  ' 2  -  -  -  -  -  -  -  -  -  -                   2  -  -  -  0  0  0  0  -  -  -\n'
                  ' 3  -  -  -  -  -  -  -  -  -  -                   3  -  -  -  -  -  -  -  -  -  -\n'
                  ' 4  -  -  -  -  -  -  -  -  -  -                   4  -  -  -  -  -  -  -  -  -  -\n'
                  ' 5  -  0  -  -  -  -  -  -  -  -                   5  -  -  -  -  -  -  -  -  -  -\n'
                  ' 6  -  0  -  -  -  -  -  -  -  -                   6  -  -  -  -  -  -  -  -  -  -\n'
                  ' 7  -  0  -  -  -  -  -  -  -  -                   7  -  -  -  -  -  -  -  -  -  -\n'
                  ' 8  -  0  -  -  -  -  -  -  -  -                   8  -  -  -  -  -  -  -  -  -  -\n'
                  ' 9  -  -  -  -  -  -  -  -  -  -                   9  -  -  -  -  -  -  -  -  -  -\n'
                  '10  -  -  -  -  -  -  -  -  -  -                  10  -  -  -  -  -  -  -  -  -  -\n')

            q = input('Type q to go back: ').lower()
            if q == 'q':
                os.system(clear_cmd)
                return self.manual_generate_prompt()

    def manual_generate_ship(self) -> bool:
        used_coordinates = []

        for ship in self.SHIPS:
            flag = False

            while not flag:
                os.system(clear_cmd)
                coordinates = False
                while not coordinates:
                    coordinates = self.manual_generate_prompt()
                col = self.COLUMN_DICT[coordinates[0]]
                row = coordinates[1]
                direction = self.DIRECTION_DICT[coordinates[2]]

                if coordinates not in used_coordinates and src.ship.check_position(col - 1, row - 1, direction, ship,
                                                                                   self.board) is True:
                    flag = src.ship.create_ship(self.board, [col, row], ship, direction)
                    temp_list = [col - 1, row - 1, ship]
                    self.player_ships.append(temp_list)
                else:
                    print('Ships can not be placed next to each other or on top of each other. There have to be at'
                          'least 1 free space between them.')
                    sleep(5)

                temp = [col, row]
            used_coordinates.append(temp)

        return True

    def attack_coordinates(self) -> list[int, int]:
        temp_coord = []
        flag = True

        while flag:
            try:
                temp_coord = input('\n\nWhere you want to attack (e.g. B 5): ').upper().split()
                if temp_coord[0] not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
                    print('Invalid input! Only character (A-J) and numbers in range (1-10) separated with space. '
                          'Please try again.')
                elif temp_coord[1] not in [str(i) for i in range(1, 11)]:
                    print('Invalid input! Only character (A-J) and numbers in range (1-10) separated with space. '
                          'Please try again.')
                else:
                    flag = False
            except IndexError:
                print('Invalid input, try again.')
                sleep(2)

        col = self.COLUMN_DICT[temp_coord[0]] - 1
        row = int(temp_coord[1]) - 1

        return [col, row]

    def reset(self):
        self.board = [[0 for _ in range(10)] for _ in range(10)]
        self.player_ships = []


player = Player()
