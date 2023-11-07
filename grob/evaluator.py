import chess
import logging

from line_profiler import profile

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3.1,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}

INF = float("inf")


debug_search_count = 0
debug_search_depth = 0


def reset_debug_vars():
    global debug_search_count
    global debug_search_depth
    debug_search_count = 0
    debug_search_depth = 0


def material_balance(board: chess.Board) -> float:
    """
    Returns: the piece material balance of the board
    """
    white_value = black_value = 0
    for piece_type in piece_values:
        white_value += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        black_value += len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    balance = white_value - black_value
    if board.turn == chess.BLACK:
        return -balance
    else:
        return balance


def evaluate(board: chess.Board) -> float:
    """
    Returns: board evaluation
    """
    balance = material_balance(board)
    return balance


@profile
def guess_move_evaluation(board: chess.Board, move: chess.Move) -> int:
    """
    Returns: guesses the evaluation of a move for move ordering
    """
    guess = 0
    move_piece_type = board.piece_type_at(move.from_square)
    capture_piece_type = board.piece_type_at(move.to_square)

    # prioritize easy captures
    if capture_piece_type is not None and move_piece_type is not None:
        guess += 10 * piece_values[capture_piece_type] - piece_values[move_piece_type]

    # prioritize promotions
    if move.promotion is not None:
        guess += piece_values[move.promotion]

    # prioritize avoiding pawns
    opposite_color = not board.turn
    attacking_pawns = board.attackers_mask(opposite_color, move.to_square) & \
        board.pieces_mask(chess.PAWN, opposite_color)
    if attacking_pawns != 0 and move_piece_type is not None:
        guess -= piece_values[move_piece_type]

    return guess


def order_moves(board: chess.Board, moves: chess.LegalMoveGenerator) -> list[chess.Move]:
    """
    Returns: sorts a list of moves in place according to guess_move_evaluation
    """
    return sorted(moves, key=lambda m: guess_move_evaluation(board, m), reverse=True)


def search_all_captures(board: chess.Board, alpha: float, beta: float, levels_deep: int = 0, search_checks: bool = True,
                        debug_counts: bool = False) -> float:
    """
    Returns: an alpha-beta evaluation that only considers capture moves (and check moves)
    """
    if debug_counts:
        global debug_search_count
        global debug_search_depth
        debug_search_count += 1
        debug_search_depth = max(debug_search_depth, levels_deep)

    evaluation = evaluate(board)
    if evaluation >= beta:
        return beta
    alpha = max(alpha, evaluation)

    capture_moves = board.generate_legal_moves(chess.BB_ALL, board.occupied_co[not board.turn])
    if search_checks:
        ...
    sorted(capture_moves, key=lambda m: guess_move_evaluation(board, m), reverse=True)  # since it's not a generator

    for move in capture_moves:
        board.push(move)
        evaluation = -search_all_captures(board, -beta, -alpha, levels_deep=levels_deep + 1, search_checks=search_checks, debug_counts=debug_counts)
        board.pop()
        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)
    return alpha


def search(board: chess.Board, depth: int, alpha: float = -INF, beta: float = INF, levels_deep: int = 0,
           guess_move_order: bool = True, search_captures: bool = True, search_checks: bool = True,
           debug_counts: bool = False) -> float:
    """
    Args:
        board:
        depth: depth to run a full search on
        alpha: see alpha-beta pruning
        beta: see alpha-beta pruning
        levels_deep: how many levels deep the current function call is
        guess_move_order: whether to sort moves according to an initial guess evaluation
        search_captures: whether to search all captures after depth limit is reached
        search_checks: whether to search all checks after depth limit is reached
        debug_counts: whether to update global count variables
    Returns: a position evaluation
    """
    if debug_counts:
        global debug_search_count
        global debug_search_depth
        debug_search_count += 1
        debug_search_depth = max(debug_search_depth, levels_deep)

    if depth == 0:
        if search_captures:
            return search_all_captures(board, alpha, beta, levels_deep=levels_deep + 1,
                                       search_checks=search_checks, debug_counts=debug_counts)
        else:
            return evaluate(board)

    moves = board.legal_moves
    if moves.count() == 0:
        if board.is_checkmate():
            return -INF  # current player has lost
        else:
            return 0  # game is a draw

    if guess_move_order:
        order_moves(board, moves)
    for move in moves:
        board.push(move)
        evaluation = -search(board, depth - 1, -beta, -alpha, levels_deep=levels_deep + 1,
                             guess_move_order=guess_move_order, search_captures=search_captures, search_checks=search_checks,
                             debug_counts=debug_counts)
        board.pop()
        if evaluation != 0:
            logging.debug(f"Eval for {move}: {evaluation}")
        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)
    return alpha


@profile
def next_move(board: chess.Board, depth: int) -> chess.Move:
    """
    Returns: finds the next best move
    """
    moves = board.legal_moves
    order_moves(board, moves)
    best_eval = -INF
    best_move = None
    for move in moves:
        board.push(move)
        if (curr_eval := -search(board, depth=depth)) > best_eval:
            best_eval = curr_eval
            best_move = move
        board.pop()
    return best_move
