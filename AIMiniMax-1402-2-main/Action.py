import Player


class Action:
    def __init__(self, row, column, direction):
        self.row = row
        self.column = column
        self.direction = direction


def doAction(action: Action, player: Player, board):
    if action.direction == "up":
        player.doGo(board, 'up')
    elif action.direction == "down":
        player.doGo(board, 'down')
    elif action.direction == "right":
        player.doGo(board, 'right')
    elif action.direction == "left":
        player.doGo(board, 'left')

    elif action.direction == "upRight" or action.direction == "rightUp":
        player.doGo(board, 'upRight')
    elif action.direction == "upLeft" or action.direction == "leftUp":
        player.doGo(board, 'leftUp')
    elif action.direction == "downRight" or action.direction == 'rightDown':
        player.doGo(board, 'downRight')
    elif action.direction == "downLeft" or action.direction == 'leftDown':
        player.doGo(board, 'downLeft')

    elif action.direction == "horizontal":
        player.doBuild(board, action.row, action.column, 'horizontal')
    elif action.direction == "vertical":
        player.doBuild(board, action.row, action.column, 'vertical')
