import random
from time import sleep

from src.ship import auto_generate_ships, check_if_ship_destroyed
from src.opponent_move import check_coordinates, move, initiate_move, move_or_go_back
from src.tools import COLUMN_DICT


class Battle:
    """
    Description:
        The Battle class represents a battle between the player and the opponent in a game.
        It contains various methods to carry out the battle and creates a player opponent.

    Attributes:
        SHIPS (list): integer list representing number of ships and there size.

        opponent_board (list): list of list representing a 10x10 grid battlefield.

        opponent_ships (list): list of list where each list contains single initial coordinates of
                                the ship and it's size.

        used_coordinates (list): list of attack coordinates already used by opponent.

        sinking_opponent_ship (list): list of coordinates representing the opponent's ship that is currently being sunk.

        sinking_player_ship (list): list of coordinates representing the player's ship that is currently being sunk.

        player_ships_sunk (list): integer representing the number of player's ships that have been sunk.

        opponent_ships_sunk (list): integer representing the number of opponent's ships that have been sunk.

        end (bool): boolean indicating if the current ship sinking sequence has ended.

    Methods:
        create_opponent: Generates the opponent's ships randomly on the opponent's board.

        opponent_attack: Initiates the opponent's attack on the player's board. The method determines
        the type of attack based on the state of the sinking_player_ship list. If attack was successful
        it lets opponent attack again. After every successful attack checks dose the ship have been sunk.

        player_attack: Initiates the player's attack on the opponent's board. The method updates the
        opponent's board and checks if a ship has been sunk. If attack was successful it lets player
        attack again. After every successful attack checks dose the ship have been sunk.
    """

    SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1]

    opponent_board = [[0 for _ in range(10)] for _ in range(10)]
    opponent_ships = []

    used_coordinates = []

    sinking_opponent_ship = []
    sinking_player_ship = []

    player_ships_sunk = 0
    opponent_ships_sunk = 0

    end = False

    def create_opponent(self) -> None:
        auto_generate_ships(self.opponent_board, self.SHIPS, self.opponent_ships)

    def opponent_attack(self, player_board: list[list], player_ships: list[list]) -> None:
        if len(self.sinking_player_ship) == 1:
            sleep(1)
            if not self.end:
                initiate_move(move, player_board, self.sinking_player_ship[0], self.used_coordinates,
                              self.sinking_player_ship)
            else:
                initiate_move(move, player_board, self.sinking_player_ship[0], self.used_coordinates,
                              self.sinking_player_ship, self.sinking_player_ship[0][2])
                self.end = False

            if check_if_ship_destroyed(player_ships, self.sinking_player_ship, self.sinking_player_ship,
                                       self.used_coordinates):
                self.player_ships_sunk += 1
                self.sinking_player_ship.clear()
                print('\nEnemy have sunk your ship')
                sleep(3)

        elif len(self.sinking_player_ship) > 1:
            sleep(1)
            direction = self.sinking_player_ship[-1][2]

            if not self.end:
                temp = initiate_move(move_or_go_back, player_board, self.sinking_player_ship[-1],
                                     self.used_coordinates, self.sinking_player_ship, direction)
                self.end = temp[1]
            else:
                initiate_move(move, player_board, self.sinking_player_ship[0], self.used_coordinates,
                              self.sinking_player_ship, self.sinking_player_ship[0][2])
                self.end = False

            if check_if_ship_destroyed(player_ships, self.sinking_player_ship, self.sinking_player_ship,
                                       self.used_coordinates):
                self.player_ships_sunk += 1
                self.sinking_player_ship.clear()
                print('\nEnemy have sunk your ship')
                sleep(3)

        elif len(self.sinking_player_ship) == 0:
            sleep(1)
            coordinates = [random.randint(0, 9), random.randint(0, 9)]

            while check_coordinates(coordinates, self.used_coordinates):
                coordinates = [random.randint(0, 9), random.randint(0, 9)]
            self.used_coordinates.append(coordinates)

            if player_board[coordinates[0]][coordinates[1]] == 1:
                player_board[coordinates[0]][coordinates[1]] = 'X'
                self.sinking_player_ship.append(coordinates)
                print(f'\nEnemy have hit your ship at {COLUMN_DICT[coordinates[0]], coordinates[1] + 1}')
                sleep(3)

                if check_if_ship_destroyed(player_ships, [coordinates], self.sinking_player_ship,
                                           self.used_coordinates):
                    self.player_ships_sunk += 1
                    self.sinking_player_ship.clear()
                    print('\nEnemy have sunk your ship')
                    sleep(3)
                else:
                    initiate_move(move, player_board, coordinates, self.used_coordinates, self.sinking_player_ship)

                    if check_if_ship_destroyed(player_ships, self.sinking_player_ship, self.sinking_player_ship,
                                               self.used_coordinates):
                        self.player_ships_sunk += 1
                        self.sinking_player_ship.clear()
                        print('\nEnemy have sunk your ship')
                        sleep(3)
            else:
                if (player_board[coordinates[0]][coordinates[1]] == 0 and
                        player_board[coordinates[0]][coordinates[1]] != 'X'):
                    player_board[coordinates[0]][coordinates[1]] = '+'

    def player_attack(self, coordinates: list) -> bool:
        if self.opponent_board[coordinates[0]][coordinates[1]] == 1:
            self.opponent_board[coordinates[0]][coordinates[1]] = 'X'
            self.sinking_opponent_ship.append(coordinates)
            if check_if_ship_destroyed(self.opponent_ships, self.sinking_opponent_ship, self.sinking_opponent_ship,
                                       None):
                self.sinking_opponent_ship.clear()
                self.opponent_ships_sunk += 1
                print('\n Hit and sunk !\n')
                sleep(2)
                return False
            if len(self.sinking_opponent_ship) <= 1:
                print('\n Direct Hit! Take one more shoot.\n')
                sleep(2)
                return True
        else:
            self.opponent_board[coordinates[0]][coordinates[1]] = '+'
            print('\nMiss\n')
            sleep(2)
            return False

    def reset(self):
        self.opponent_board = [[0 for _ in range(10)] for _ in range(10)]
        self.opponent_ships = []

        self.used_coordinates = []

        self.sinking_opponent_ship = []
        self.sinking_player_ship = []

        self.player_ships_sunk = 0
        self.opponent_ships_sunk = 0

        self.end = False


battle = Battle()
