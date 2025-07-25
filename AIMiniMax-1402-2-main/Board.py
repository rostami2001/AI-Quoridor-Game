from collections import deque
import math


class Board:
    # const
    # Empty_block = 0
    # Empty_Wall = -1
    # walled = 1
    # Player1 = 11
    # Player2 = 22

    def __init__(self, size, player1, player2) -> None:

        self.size = size * 2 - 1

        self.board = [[-1] * self.size for _ in range(self.size)]
        for i in range(0, len(self.board), 2):
            for j in range(0, len(self.board[i]), 2):
                self.board[i][j] = 0
        self.board[player2.row][player2.column] = 22
        self.board[player1.row][player1.column] = 11

        self.player1 = player1
        self.player2 = player2

    def displayboard(self):

        for indexR, r in enumerate(self.board):

            for indexC, c in enumerate(r):
                if c == 0:
                    print("█", end=" ")
                elif c == -1:
                    print(' ', end=" ")
                elif c == 1:
                    if indexR % 2 == 0:
                        print('|', end=" ")
                    else:
                        if indexC % 2 != 0:
                            print('•', end=" ")
                        else:
                            print('\u2014', end=" ")
                else:
                    print(str(c)[0], end=" ")
            print()

    def valid(self, row, col) -> bool:
        """
        Returns true if the given row and col represent a valid location on
        the Quoridor board.
        """
        return row >= 0 and col >= 0 and row < self.size and col < self.size

    def checkForWall(self, row, column):  # for pathToOtherSide
        if row == 2:
            return (1, 0)
        elif row == -2:
            return (-1, 0)
        elif column == -2:
            return (0, -1)
        elif column == 2:
            return (0, 1)

    def pathToOtherSide(self, row, column, goalRow) -> bool:
        """ DFS"""
        stack = [(row, column)]
        visited = set()
        while stack:
            x, y = stack.pop()
            if x == goalRow:
                return True  # Player reached the goal
            if (x, y) in visited:
                continue  # Skip already visited nodes
            visited.add((x, y))

            # Check all adjacent cells
            for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                new_xW, new_yW = self.checkForWall(dx, dy)
                new_xW, new_yW = x + new_xW, y + new_yW
                new_x, new_y = x + dx, y + dy
                if self.valid(new_x, new_y) and self.board[new_xW][new_yW] == -1:
                    stack.append((new_x, new_y))  # Add legal moves to the stack
        return False  # No path found

    def checkForTrap(self):
        p1 = self.pathToOtherSide(self.player1.row, self.player1.column, self.player1.goalRow)
        p2 = self.pathToOtherSide(self.player2.row, self.player2.column, self.player2.goalRow)
        return not (p1 and p2)

    def canPlaceWall(self, row, column, direction: str) -> bool:
        """
        determines if the cordinates are valid for placing wall in desired direction.
        """

        if row % 2 == 0 or column % 2 == 0 or not self.valid(row, column) or self.board[row][column] != -1:
            return False
        else:
            if direction == 'vertical':
                return (self.valid(row + 1, column) and self.valid(row - 1, column) \
                        and self.board[row + 1][column] == -1 and self.board[row - 1][column] == -1)


            elif direction == 'horizontal':
                return (self.valid(row, column + 1) and self.valid(row, column - 1) \
                        and self.board[row][column + 1] == -1 and self.board[row][column - 1] == -1)


            else:
                raise Exception('invalid direction!')

    def addWall(self, row, column, direction: str):
        if self.canPlaceWall(row, column, direction):
            if direction == 'vertical':
                self.board[row][column] = 1
                self.board[row + 1][column] = 1
                self.board[row - 1][column] = 1
            else:
                self.board[row][column] = 1
                self.board[row][column + 1] = 1
                self.board[row][column - 1] = 1

    def go(self, player,
           direction):

        self.board[player.row][player.column] = 0
        cango, jump = self.canGo(player, direction)
        if cango:
            if direction == 'up':
                if jump:
                    player.row -= 4
                else:
                    player.row -= 2

            elif direction == 'down':

                if jump:
                    player.row += 4
                else:
                    player.row += 2

            elif direction == 'right':

                if jump:
                    player.column += 4
                else:
                    player.column += 2

            elif direction == 'left':

                if jump:
                    player.column -= 4
                else:
                    player.column -= 2


            elif direction == 'upRight' or direction == 'rightUp':

                player.row -= 2
                player.column += 2

            elif direction == 'upLeft' or direction == 'leftUp':

                player.row -= 2
                player.column -= 2
            elif direction == 'downRight' or direction == 'rightDown':

                player.row += 2
                player.column += 2
            elif direction == 'downLeft' or direction == 'downLeft''leftDown':

                player.row += 2
                player.column -= 2

        self.board[player.row][player.column] = int(player.name[-1] * 2)

    def canGo(self, player, direction) -> (bool, bool):
        """
        Returns if the player can go to the desired direction or not.
        the second bool determines if the move is jump over another player or it is regular.
        """
        if direction == 'up':
            if self.valid(player.row - 2, player.column) and self.board[player.row - 2][
                player.column] == 0:  # age block khali bood
                return (self.board[player.row - 1][player.column] == -1, False)  ## ham valid bashe ham wall nabashe
            elif self.valid(player.row - 4, player.column) and self.board[player.row - 1][player.column] == -1:  # age player dige bood
                return (self.board[player.row - 3][player.column] == -1, True)
            else:
                return (False, False)
        elif direction == 'down':
            if self.valid(player.row + 2, player.column) and self.board[player.row + 2][
                player.column] == 0:
                return (self.board[player.row + 1][player.column] == -1, False)
            elif self.valid(player.row + 4, player.column)and self.board[player.row + 1][player.column] == -1:
                return (self.board[player.row + 3][player.column] == -1, True)
            else:
                return (False, False)

        elif direction == 'right':
            if self.valid(player.row, player.column + 2) and self.board[player.row][
                player.column + 2] == 0:
                return (self.board[player.row][player.column + 1] == -1, False)
            elif self.valid(player.row, player.column + 4)and self.board[player.row ][player.column+1] == -1:
                return (self.board[player.row][player.column + 3] == -1, True)
            else:
                return (False, False)
        elif direction == 'left':
            if self.valid(player.row, player.column - 2) and self.board[player.row][
                player.column - 2] == 0:
                return (self.board[player.row][player.column - 1] == -1, False)
            elif self.valid(player.row, player.column - 4)and self.board[player.row ][player.column-1] == -1:
                return (self.board[player.row][player.column - 3] == -1, True)
            else:
                return (False, False)
        elif direction == 'upRight':
            if self.valid(player.row - 2, player.column + 2) and self.board[player.row - 1][player.column] == -1 and \
                    self.board[player.row - 2][player.column] != 0 and self.board[player.row - 2][
                player.column + 1] == -1 :
                if self.valid(player.row-3, player.column):
                    return (self.board[player.row-3][player.column ] == 1, False)
                else:
                    return (True, False)
            else:
                return (False, False)

        elif direction == 'upLeft':
            if self.valid(player.row - 2, player.column - 2) and self.board[player.row - 1][player.column] == -1 and \
                    self.board[player.row - 2][player.column] != 0 and self.board[player.row - 2][
                player.column - 1] == -1 :
                if self.valid(player.row - 3, player.column):
                    return (self.board[player.row - 3][player.column] == 1, False)
                else:
                    return (True, False)
            else:
                return (False, False)

        elif direction == 'rightUp':
            if self.valid(player.row - 2, player.column + 2) and self.board[player.row][player.column + 1] == -1 and \
                    self.board[player.row][player.column + 2] != 0 and self.board[player.row - 1][
                player.column + 2] == -1 :
                if self.valid(player.row , player.column+3):
                    return (self.board[player.row ][player.column+3] == 1, False)
                else:
                    return (True, False)
            else:
                return (False, False)
        elif direction == 'rightDown':
            if self.valid(player.row + 2, player.column + 2) and self.board[player.row][player.column + 1] == -1 and \
                    self.board[player.row][player.column + 2] != 0 and self.board[player.row + 1][
                player.column + 2] == -1 :
                if self.valid(player.row, player.column + 3):
                    return (self.board[player.row][player.column + 3] == 1, False)
                else:
                    return (True, False)
            else:
                return (False, False)
        elif direction == 'downRight':
            if self.valid(player.row + 2, player.column + 2) and self.board[player.row + 1][player.column] == -1 and \
                    self.board[player.row + 2][player.column] != 0 and self.board[player.row + 2][
                player.column + 1] == -1:
                if self.valid(player.row + 3, player.column):
                    return (self.board[player.row + 3][player.column] == 1, False)
                else:
                    return (True, False)
            else:
                return (False, False)
        elif direction == 'downLeft':
            if self.valid(player.row + 2, player.column - 2) and self.board[player.row + 1][player.column] == -1 and \
                    self.board[player.row + 2][player.column] != 0 and self.board[player.row + 2][
                player.column - 1] == -1:
                if self.valid(player.row + 3, player.column):
                    return (self.board[player.row + 3][player.column] == 1, False)
                else:
                    return (True, False)

            else:
                return (False, False)
        elif direction == 'leftUp':
            if self.valid(player.row - 2, player.column - 2) and self.board[player.row ][player.column-1] == -1 and \
                    self.board[player.row][player.column - 2] != 0 and self.board[player.row - 1][
                player.column - 2] == -1 :
                if self.valid(player.row , player.column-3):
                    return (self.board[player.row ][player.column-3] == 1, False)
                else:
                    return (True, False)
            else:
                return (False, False)
        elif direction == 'leftDown':
            if self.valid(player.row + 2, player.column - 2) and self.board[player.row ][player.column-1] == -1 and \
                    self.board[player.row][player.column - 2] != 0 and self.board[player.row + 1][
                player.column - 2] == -1 :
                if self.valid(player.row, player.column - 3):
                    return (self.board[player.row][player.column - 3] == 1, False)
                else:
                    return (True, False)
            else:
                return (False, False)
        else:
            raise Exception('inavlid input')

    def shortestPath(self, player):
        """
        Perform Breadth-First Search to find the shortest path from start to target.
        """
        visited = [[False] * 13 for _ in range(13)]
        queue = deque([(player.row, player.column, 0)])
        visited[player.row][player.column] = True

        while queue:
            row, col, distance = queue.popleft()

            if row == player.goalRow:
                return distance

            for dr, dc in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                new_xW, new_yW = self.checkForWall(dr, dc)
                new_xW, new_yW = row + new_xW, col + new_yW
                new_row, new_col = row + dr, col + dc
                if self.valid(new_row, new_col) and not visited[new_row][new_col] and self.board[new_xW][new_yW] == -1:
                    queue.append((new_row, new_col, distance + 1))
                    visited[new_row][new_col] = True

        # If target is not reachable
        return -1

    def distance(self, point1, playerName):
        x1, y1 = point1
        if playerName == 'player 1':
            x2, y2 = self.player2.row, self.player2.column
        else:
            x2, y2 = self.player1.row, self.player1.column
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
