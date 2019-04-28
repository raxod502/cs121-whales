import chess
import random
import numpy as np


def minimax(board, eval_fn, max_depth):
    """
    Perform minimax search with alpha/beta pruning through board up
    to a depth of max_depth.

    Take in a board with the current game state, an evaluation function
    called when depth is reached, and a max depth.
    """
    starting_player = board.turn

    return minimax_helper(
        board, eval_fn, max_depth, 0, float("-inf"), float("inf"), starting_player
    )


def minimax_helper(board, eval_fn, max_depth, curr_depth, alpha, beta, starting_player):
    """
    Perform minimax search with alpha/beta pruning through board up
    to a depth of max_depth.

    Take in a board with the current game state, a max depth, a current
    depth, alpha and beta for pruning, an evaluation function called
    when depth is reached, and a starting player.
    """

    curr_agent = board.turn

    multiplier = 1 if starting_player == chess.WHITE else -1

    if board.is_game_over():
        result = board.result()

        score = 0

        # strongly prioritize/deprioritize checkmate boards

        if result == "1-0":
            # white has won
            score = 100
        elif result == "0-1":
            # black has won
            score = -100
        else:
            # game is draw
            # assign a score of 0 here because a tie is better than
            # a black win
            score = 0

        return (multiplier * score, None)

    if curr_depth >= max_depth:
        # if at a leaf node, evaluate board
        return (multiplier * eval_fn(board), None)

    # if it is the starting player's turn, we maximize
    is_maximizing = curr_agent == starting_player
    is_minimizing = not is_maximizing

    legal_actions = list(board.legal_moves)

    best_action = None
    v = 0

    if is_maximizing:
        v = float("-inf")
    else:
        v = float("inf")

    for i in range(len(legal_actions)):
        action = legal_actions[i]

        # simulate the move to pass to children
        successor = board.copy()
        successor.push(action)

        # recurse with same parameters, except one level deeper
        successor_val = minimax_helper(
            successor, eval_fn, max_depth, curr_depth + 1, alpha, beta, starting_player
        )[0]

        if (successor_val > v and is_maximizing) or (
            successor_val < v and is_minimizing
        ):
            best_action = action
            v = successor_val

        # pruning case, stop considering branch
        # return value doesn't matter; we won't be using it
        if (v > beta and is_maximizing) or (v < alpha and is_minimizing):
            return (v, best_action)

        if is_maximizing:
            alpha = max(alpha, v)
        else:
            beta = min(beta, v)

    # return most optimized child along with action to take
    return (v, best_action)


def alt_minimax(board, eval_fn):
    legal_actions = list(board.legal_moves)
    all_boards = [None] * len(legal_actions)
    for i in range(len(legal_actions)):
        all_boards[i] = board.copy()
        all_boards[i].push(legal_actions[i])

    values = eval_fn(all_boards)
    # Get the board that is least advantageous for opponent
    index = np.argmin(values)

    return legal_actions[index]
