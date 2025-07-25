import copy
from Action import doAction
from Board import Board
from Player import Player
from utility import utility

class AI:
    MIN_VALUE = -1000000
    MAX_VALUE = 1000000

    def choose_action(self, board, player, opponent, max_depth):
        best_action = self.doMiniMax(
            copy.deepcopy(board),
            copy.copy(player),
            copy.copy(opponent),
            max_depth,
        )
        return best_action

    def deepCopy(self, player, opponent, board):
        player_copy = copy.deepcopy(player)
        opponent_copy = copy.deepcopy(opponent)
        next_board = copy.deepcopy(board)
        next_board.player1 = player_copy
        next_board.player2 = opponent_copy
        return player_copy, opponent_copy, next_board

    def successors(self, board: Board, player: Player, opponent: Player, reverse=False):
        if reverse:
            actions = opponent.getValidActions(board)
        else:
            actions = player.getValidActions(board)
        result = []
        for action in actions:
            player_copy, opponent_copy, next_board = self.deepCopy(player, opponent, board)
            if reverse:
                doAction(action, opponent_copy, next_board)
            else:
                doAction(action, player_copy, next_board)
            result.append({'board': next_board, 'player': player_copy, 'opponent': opponent_copy, 'action': action})
        return result

    def doMiniMax(self, board: Board, player: Player, opponent: Player, depth):
        if player.name == 'player 1':
            value, action = self.max(board, player, opponent, depth)
        else:
            value, action = self.min(board, player, opponent, depth)

        return action


    def max(self, board, player, opponent, depth):
        if depth == 0 or player.terminal_test():
            return utility(board, player, opponent), None

        max_value = float('-inf')
        best_action = None

        for successor in self.successors(board, player, opponent):
            new_board = successor['board']
            action = successor['action']

            value = self.min(new_board, player, opponent, depth - 1)[0]

            if value > max_value:
                max_value = value
                best_action = action

        return max_value, best_action

    def min(self, board, player, opponent, depth):
        if depth == 0 or opponent.terminal_test():
            return utility(board, player, opponent), None

        min_value = float('inf')
        best_action = None

        for successor in self.successors(board, player, opponent, reverse=True):
            new_board = successor['board']
            action = successor['action']

            value = self.max(new_board, player, opponent, depth - 1)[0]

            if value < min_value:
                min_value = value
                best_action = action

        return min_value, best_action