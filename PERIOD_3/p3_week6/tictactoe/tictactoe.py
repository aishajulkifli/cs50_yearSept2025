"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():            # -> list
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):  #> str
    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == "X":
                x_count += 1
            elif cell == "O":
                o_count += 1

    if x_count == o_count:
        return "X"
    else:
        return "O"


def actions(board):
    moves = set()       # set to store available moves

    for i in range(3):          # loop through rows
        for j in range(3):      # loop through columns
            if board[i][j] is None: # if cell is empty, add its coordinates to the set of moves
                moves.add((i, j))

    return moves


def result(board, action):              #> list
    if action not in actions(board):    # if the action is not valid (not in the set of available moves), raise an exception
        raise Exception("Invalid move")

    # Copy board (important!)
    new_board = [row.copy() for row in board]   # create a new board by copying each row of the original board. This is important to avoid modifying the original board when we apply the action.

    i, j = action                               # unpack the action into row and column indices
    new_board[i][j] = player(board)

    return new_board


def winner(board):      # > str or None
    lines = []          # list to store all possible winning lines (rows, columns, diagonals)

    # Rows
    lines.extend(board) # add all rows of the board to the list of lines

    # Columns
    for j in range(3):
        lines.append([board[0][j], board[1][j], board[2][j]])   # add each column of the board to the list of lines by creating a new list for each column that contains the elements from that column across all rows. For example, for the first column (j=0), we create a list [board[0][0], board[1][0], board[2][0]] and add it to the lines list. We repeat this process for the second and third columns (j=1 and j=2).

    # Diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])       # add the first diagonal (top-left to bottom-right) to the list of lines by creating a new list that contains the elements from that diagonal: [board[0][0], board[1][1], board[2][2]]. We then add this list to the lines list.
    lines.append([board[0][2], board[1][1], board[2][0]])       # add the second diagonal (top-right to bottom-left) to the list of lines by creating a new list that contains the elements from that diagonal: [board[0][2], board[1][1], board[2][0]]. We then add this list to the lines list.

    for line in lines:
        if line[0] is not None and line.count(line[0]) == 3:    # check if the first cell of the line is not empty and if all three cells in the line are the same (i.e., they all contain the same player's symbol). If both conditions are true, it means that player has won, and we return the symbol of that player (line[0]).
            return line[0]

    return None


def terminal(board):                    # > bool
    # If someone won → game over
    if winner(board) is not None:       # check if there is a winner by calling the winner function. If the winner function returns a non-None value, it means that there is a winner and the game is over, so we
        return True

    # If any empty cell → game not over
    for row in board:                   # loop through each row of the board
        if None in row:                 # check if there is an empty cell (None) in the current row. If there is an empty cell, it means that the game is not over yet, so we return False.
            return False

    # Otherwise → no empty cells → game over
    return True


def utility(board):             # > int
    w = winner(board)           # call the winner function to determine if there is a winner on the board. The winner function will return "X" if player X has won, "O" if player O has won, or None if there is no winner.

    if w == "X":
        return 1                # If player X has won, the utility value is 1, indicating a favorable outcome for player X.
    elif w == "O":
        return -1               # If player O has won, the utility value is -1, indicating an unfavorable outcome for player X (and a favorable outcome for player O).
    else:
        return 0                # If there is no winner (i.e., a tie or the game is still ongoing), the utility value is 0, indicating a neutral outcome for both players.


def minimax(board):             # minimax function that returns the optimal action for the current player on the board. The minimax algorithm is a decision-making algorithm used in game theory and artificial intelligence to determine the best move for a player, assuming that the opponent also plays optimally.
    if terminal(board):
        return None

    turn = player(board)

    # If it's X → maximize
    if turn == "X":
        best_value = float("-inf")      # -inf represents negative infinity, which is the smallest possible value. We initialize best_value to negative infinity because we want to find the maximum value, and any value we encounter will be greater than negative infinity.
        best_move = None                # variable to store the best move found so far. We initialize it to None because we haven't found any moves yet.

        for action in actions(board):   # loop through all possible actions (moves) available on the board by calling the actions function. The actions function returns a set of all valid moves that can be made on the current board state.
            value = min_value(result(board, action))    # for each action, we calculate the value of that action by calling the min_value function on the result of applying that action to the board. The result function takes the current board and an action, and returns a new board state that results from applying that action. The min_value function is a recursive function that evaluates the value of a board state from the perspective of the minimizing player (in this case, player O). It will return a value that represents how favorable that board state is for player O.
            if value > best_value:
                best_value = value
                best_move = action

        return best_move

    # If it's O → minimize
    else:
        best_value = float("inf")       # inf represents positive infinity, which is the largest possible value. We initialize best_value to positive infinity because we want to find the minimum value, and any value we encounter will be less than positive infinity.
        best_move = None

        for action in actions(board):
            value = max_value(result(board, action))        # for each action, we calculate the value of that action by calling the max_value function on the result of applying that action to the board. The max_value function is a recursive function that evaluates the value of a board state from the perspective of the maximizing player (in this case, player X). It will return a value that represents how favorable that board state is for player X.
            if value < best_value:
                best_value = value
                best_move = action

        return best_move

def max_value(board):
    if terminal(board):         # check if the board state is terminal (i.e., the game is over) by calling the terminal function. If the terminal function returns True, it means that the game is over and we can evaluate the utility of that board state.
        return utility(board)   # utility function is called to evaluate the utility of the terminal board state. The utility function will return a value that represents how favorable that board state is for player X (1 for a win, -1 for a loss, and 0 for a tie or ongoing game).

    v = float("-inf")           # initialize v to negative infinity because we want to find the maximum value, and any value we encounter will be greater than negative infinity.

    for action in actions(board):
        v = max(v, min_value(result(board, action)))    # loop through all possible actions (moves) available on the board by calling the actions function. For each action, we calculate the value of that action by calling the min_value function on the result of applying that action to the board. The min_value function will return a value that represents how favorable that board state is for player O (the minimizing player). We then take the maximum of v and this value to update v with the best value found so far.

    return v


def min_value(board):
    if terminal(board):     # check if the board state is terminal (i.e., the game is over) by calling the terminal function. If the terminal function returns True, it means that the game is over and we can evaluate the utility of that board state.
        return utility(board)

    v = float("inf")        # initialize v to positive infinity because we want to find the minimum value, and any value we encounter will be less than positive infinity.

    for action in actions(board):
        v = min(v, max_value(result(board, action)))    # loop through all possible actions (moves) available on the board by calling the actions function. For each action, we calculate the value of that action by calling the max_value function on the result of applying that action to the board. The max_value function will return a value that represents how favorable that board state is for player X (the maximizing player). We then take the minimum of v and this value to update v with the best value found so far.

    return v
