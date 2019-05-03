import chess
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

    # Multiply by -1 in the case that the root minimax call was Black
    # because the evaluation function returns more positive values to
    # represent a high probability of White winning; for Black we must
    # flip that.
    multiplier = 1 if starting_player == chess.WHITE else -1

    if board.is_game_over():
        result = board.result()

        score = 0

        # Strongly prioritize/deprioritize checkmate boards.

        if result == "1-0":
            # This is the case where White has won.
            score = 100
        elif result == "0-1":
            # This is the case where Black has won.
            score = -100
        else:
            # This is the case where the game is a draw. Here, assign
            # a score of 0 because a tie is better than a black win.
            score = 0

        return (multiplier * score, None)

    if curr_depth >= max_depth:
        # If at a leaf node, evaluate the board.
        return (multiplier * eval_fn(board), None)

    # If it is the starting player's turn, maximize.
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

        # Simulate the move to pass to children.
        successor = board.copy()
        successor.push(action)

        # Recurse with same parameters, except one level deeper.
        successor_val = minimax_helper(
            successor, eval_fn, max_depth, curr_depth + 1, alpha, beta, starting_player
        )[0]

        if (successor_val > v and is_maximizing) or (
            successor_val < v and is_minimizing
        ):
            best_action = action
            v = successor_val

        # Here is the pruning case, stop considering branch. The move
        # chosen doesn't matter here; it will not be used.
        if (v > beta and is_maximizing) or (v < alpha and is_minimizing):
            return (v, best_action)

        # Update parameters for pruning.
        if is_maximizing:
            alpha = max(alpha, v)
        else:
            beta = min(beta, v)

    # Return most optimized child's value along with action to take.
    return (v, best_action)


def greedy_minimax(board, eval_fn):
    """
    Greedily select best board based solely on evaluation function.
    """

    legal_actions = list(board.legal_moves)
    all_boards = [None] * len(legal_actions)

    for i in range(len(legal_actions)):
        all_boards[i] = board.copy()
        all_boards[i].push(legal_actions[i])

    values = eval_fn(all_boards)

    # Select move that is least advantageous for opponent.
    index = np.argmin(values)

    return legal_actions[index]
