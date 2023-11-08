from itertools import chain

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
                        debug_counts: bool = False) -> tuple[float, chess.Move | None]:
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
        return beta, None
    alpha = max(alpha, evaluation)

    # unclear if this is the most efficient way of generating these moves, could also use board.gives_check
    capture_moves = board.generate_legal_moves(chess.BB_ALL, board.occupied_co[not board.turn])
    important_moves = capture_moves
    if search_checks:
        king = board.king(not board.turn)
        # mask logic followed according to board.attacks_mask()
        pawn_check_moves = board.generate_legal_moves(
            board.pieces_mask(chess.PAWN, board.turn), chess.BB_PAWN_ATTACKS[not board.turn][king])
        rook_checks_mask = (chess.BB_RANK_ATTACKS[king][chess.BB_RANK_MASKS[king] & board.occupied] |
                            chess.BB_FILE_ATTACKS[king][chess.BB_FILE_MASKS[king] & board.occupied])
        rook_check_moves = board.generate_legal_moves(
            board.pieces_mask(chess.ROOK, board.turn), rook_checks_mask)
        knight_check_moves = board.generate_legal_moves(
            board.pieces_mask(chess.KNIGHT, board.turn), chess.BB_KNIGHT_ATTACKS[king])
        bishop_checks_mask = chess.BB_DIAG_ATTACKS[king][chess.BB_DIAG_MASKS[king] & board.occupied]
        bishop_check_moves = board.generate_legal_moves(
            board.pieces_mask(chess.BISHOP, board.turn), bishop_checks_mask)
        queen_check_moves = board.generate_legal_moves(
            board.pieces_mask(chess.QUEEN, board.turn), rook_checks_mask | bishop_checks_mask)
        important_moves = chain(capture_moves, pawn_check_moves, rook_check_moves,
                                knight_check_moves, bishop_check_moves, queen_check_moves)

    important_moves = sorted(important_moves, key=lambda m: guess_move_evaluation(board, m), reverse=True)

    best_move = None
    for move in important_moves:
        board.push(move)
        evaluation = -search_all_captures(board, -beta, -alpha, levels_deep=levels_deep + 1,
                                          search_checks=search_checks, debug_counts=debug_counts)[0]
        board.pop()
        if evaluation >= beta:
            return beta, None
        if evaluation > alpha:  # must not be >=
            alpha = evaluation
            best_move = move
    return alpha, best_move


def search(board: chess.Board, depth: int, alpha: float = -INF, beta: float = INF, levels_deep: int = 0,
           guess_move_order: bool = True, search_captures: bool = True, search_checks: bool = True,
           debug_counts: bool = False) -> tuple[float, chess.Move | None]:
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
    Returns: the evaluation of the current position, along with the best move if the depth has not been reached
    """
    if debug_counts:
        global debug_search_count
        global debug_search_depth
        debug_search_count += 1
        debug_search_depth = max(debug_search_depth, levels_deep)

    if depth == 0:
        if search_captures:
            return search_all_captures(board, alpha, beta, levels_deep=levels_deep,
                                       search_checks=search_checks, debug_counts=debug_counts)
        else:
            return evaluate(board), None

    moves = board.legal_moves
    if moves.count() == 0:
        if board.is_checkmate():
            return -INF, None  # current player has lost
        else:
            return 0, None  # game is a draw

    if guess_move_order:
        moves = order_moves(board, moves)
    best_move = None
    for move in moves:
        board.push(move)
        evaluation = -search(board, depth - 1, -beta, -alpha, levels_deep=levels_deep + 1,
                             guess_move_order=guess_move_order, search_captures=search_captures,
                             search_checks=search_checks, debug_counts=debug_counts)[0]
        board.pop()
        if evaluation != 0:
            logging.debug(f"Eval for {move}: {evaluation}")
        if evaluation >= beta != INF:
            return beta, None
        if evaluation > alpha:
            alpha = evaluation
            best_move = move
    return alpha, best_move
