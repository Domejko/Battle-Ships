import os
from time import sleep

from src.player import player
from src.battle import battle
from src.tools import is_game_over, LOGO, print_board, play_again, clear_cmd


if __name__ == '__main__':
    play = True

    while play:
        print(LOGO)
        battle.create_opponent()
        player.auto_generate_prompt()

        game_on = True

        while game_on:
            os.system(clear_cmd)
            print(LOGO)
            print_board(player.board, battle.opponent_board)
            if battle.player_attack(player.attack_coordinates()):
                os.system(clear_cmd)
                print(LOGO)
                print_board(player.board, battle.opponent_board)
                battle.player_attack(player.attack_coordinates())
                sleep(1)
            battle.opponent_attack(player.board, player.player_ships)
            game_on = is_game_over(battle.opponent_ships_sunk, battle.player_ships_sunk)
            print('')

        sleep(5)
        play = play_again()
        battle.reset()
        player.reset()
