from Board import Board
from Player import Player
import numpy as np

def utility(board: Board, player: Player, opponent: Player):
    value = 0
    if player.terminal_test():
        value = 1000
    elif opponent.terminal_test():
        value = -1000
    else:
        player_shortest_path = board.shortestPath(player)
        opponent_shortest_path = board.shortestPath(opponent)
        value = 0.5 * (player_shortest_path - opponent_shortest_path)
    return value