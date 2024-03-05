import os


COLUMN_DICT = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}

LOGO = ("   ___       __  __  __      ______   _\n"
        "  / _ )___ _/ /_/ /_/ /__   / __/ /  (_)__  ___                    #   #  (|)\n"
        " / _  / _ `/ __/ __/ / -_) _\ \/ _ \/ / _ \(_-<                ___| |_| |__|__\n"
        "/____/\_,_/\__/\__/_/\__/ /___/_//_/_/ .__/___/            _  |____________|  _\n"
        "                                    /_/             _=====| | |            | | |==== _\n"
        "                                            =======| |.---------------------------. | |====\n"
        "                                 <--------------------'   .  .  .  .  .  .  .  .   '--------------/\n"
        "                                   \                                                             / \n"
        "                                    \___________________________________________________________/ \n")


def increment(number: int, direction: int) -> int:
    """
    Description:
        If the direction parameter is either 4 or 2, the number is incremented
        by 1 and the updated number is returned. If the direction parameter is either 3 or 1,
        the number is decremented by 1 and the updated number is returned.
    :param number: an integer representing either column or row on the board.
    :param direction: an integer representing a direction on the board.
    :return: integer
    """
    if direction in [4, 2]:
        number -= 1
        return number
    elif direction in [3, 1]:
        number += 1
        return number


def is_game_over(ships_sunk_player: int, ships_sunk_opponent: int) -> bool:
    """
    Description:
        If the ships_sunk_player is equal to 11, the function displays a message indicating
        that the player has won and returns False. If the ships_sunk_opponent is equal to 11,
        the function displays a message indicating that the player has lost and returns False.
        Otherwise, it returns True.
    :param ships_sunk_player: Integer representing number of ships sunk by player.
    :param ships_sunk_opponent: Integer representing number of ships sunk by opponent.
    :return: boolean
    """
    if ships_sunk_player == 11:
        os.system(clear_cmd)
        print('\nCONGRATULATIONS YOU HAVE WON !\n')
        return False
    elif ships_sunk_opponent == 11:
        os.system(clear_cmd)
        print('\nGAME OVER, YOU HAVE LOST.\n')
        return False
    return True


def print_board(board: list[list], opponent_board: list[list]) -> None:
    """
    Description:
        The function prints out the visual representation of the board and opponent_board.
        It iterates through the rows of the board and prints the corresponding cells. The cells
        are printed as 'O' (if it has a value of 1), 'X' (if it has value 'X'), '+' (if it has value '+'),
        or '-' (if it has any other value). The function prints both the player's board and the
        opponent's board side by side.
    :param board: List of lists representing a player board with his ships locations.
    :param opponent_board: List of lists representing opponents board where visible are coordinates
                            where player have attacked and ships that he have sunk.
    :return: None
    """
    for n in range(10):
        flag = True
        flag_1 = True
        print('')
        if n == 0:
            print('    A  B  C  D  E  F  G  H  I  J        A  B  C  D  E  F  G  H  I  J')
        for col in board:
            if flag is True and n != 9:
                print(f'{n + 1}   ', end='')
                flag = False
            elif flag is True:
                print(f'{n + 1}  ', end='')
                flag = False
            if col[n] == 1:
                print('O  ', end='')
            elif col[n] == 'X':
                print('\033[93mX  \033[0m', end='')
            elif col[n] == '+':
                print('\033[96m+  \033[0m', end='')
            else:
                print('-  ', end='')
        for col_1 in opponent_board:
            if flag_1 is True and n != 9:
                print(f'  {n + 1}   ', end='')
                flag_1 = False
            elif flag_1 is True:
                print(f'  {n + 1}  ', end='')
                flag_1 = False
            if col_1[n] == 'X':
                print('\033[93mX  \033[0m', end='')
            elif col_1[n] == '+':
                print('\033[96m+  \033[0m', end='')
            else:
                print('-  ', end='')


def print_single_board(board: list[list]) -> None:
    """
    Description:
        The function prints out the visual representation of the board during manual creation of
        the ships by player. It iterates through the rows of the board and prints the corresponding
        cells. The cells are printed as 'O' (if it has a value of 1), 'X' (if it has value 'X'),
        '+' (if it has value '+'), or '-' (if it has any other value).
    :param board: List of lists representing a player board with his ships locations.
    :return: None
    """
    for n in range(10):
        flag = True
        print('')
        if n == 0:
            print('    A  B  C  D  E  F  G  H  I  J')
        for col in board:
            if flag is True and n != 9:
                print(f' {n + 1}  ', end='')
                flag = False
            elif flag is True:
                print(f'{n + 1}  ', end='')
                flag = False
            if col[n] == 1:
                print('O  ', end='')
            elif col[n] == 'X':
                print('X  ', end='')
            elif col[n] == '+':
                print('+  ', end='')
            else:
                print('-  ', end='')


def play_again() -> bool:
    resp = input('Do you want to play again (y/n): ').upper()
    if resp == 'Y':
        return True
    else:
        return False


def check_os():
    if os.name == 'posix':
        return 'clear'
    elif os.name == 'nt':
        return 'cls'


clear_cmd = check_os()
