import sys
sys.path.insert(0, '/home/domejko/Python-projects/BattleShips')

import src


battle = src.battle.Battle()
player = src.player.Player()

while True:
    print(src.tools.LOGO)
    print(battle.opponent_board)
    battle.create_opponent()
    src.ship.auto_generate_ships(player.board, player.SHIPS, player.player_ships)

    game_on = True
    while game_on:
        print(src.tools.LOGO)
        src.tools.print_board(player.board, battle.opponent_board)
        if battle.player_attack([0, 0]):
            print(src.tools.LOGO)
            src.tools.print_board(player.board, battle.opponent_board)
            battle.player_attack([0, 0])
        battle.opponent_attack(player.board, player.player_ships)
        game_on = src.tools.is_game_over(battle.opponent_ships_sunk, battle.player_ships_sunk)
        print('')

    battle.reset()
    player.reset()
