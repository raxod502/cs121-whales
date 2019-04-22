import chess
import random
import numpy as np


def minimax(
    board,
    eval_fn,
    max_depth=2,
    curr_depth=0,
    alpha=float("-inf"),
    beta=float("inf"),
    starting_player=None,
):
    """
    Perform minimax search with alpha/beta pruning through board up
    to a depth of max_depth.

    Take in a board with the current game state, a max depth in
    plies, a current depth, alpha and beta for pruning, an evaluation
    function called when depth is reached, and a starting player.

    Note: use defaults for curr_depth, alpha, beta, and
    starting_player.
    """

    if starting_player is None:
        # if given the default value, determine based on board
        starting_player = board.turn

    if curr_depth >= max_depth or board.is_game_over():
        # if at a leaf node, evaluate board
        multiplier = 1 if starting_player == chess.WHITE else -1
        return (multiplier * eval_fn(board), None)

    curr_agent = board.turn

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
        successor_val = minimax(
            successor,
            eval_fn,
            max_depth,
            curr_depth + 1,
            alpha,
            beta,
            starting_player=starting_player,
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
