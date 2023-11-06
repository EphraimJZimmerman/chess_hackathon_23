import chess
import logging

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3.1,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}

INF = float("inf")


debug_count = 0


def material_balance(board: chess.Board) -> float:
    """

    Args:
        board:

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

    Args:
        board:

    Returns: board evaluation

    """
    balance = material_balance(board)
    return balance

@profile
def guess_move_evaluation(board: chess.Board, move: chess.Move) -> int:
    """

    Args:
        board:
        move:

    Returns: guesses the evaluation of a move for move ordering

    """
    guess = 0
    move_piece = board.piece_at(move.from_square)
    move_piece_type = None if move_piece is None else move_piece.piece_type
    capture_piece = board.piece_at(move.to_square)
    capture_piece_type = None if capture_piece is None else capture_piece.piece_type

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
    return sorted(moves, key=lambda m: guess_move_evaluation(board, m), reverse=True)


def search(board: chess.Board, depth: int, alpha: float = -INF, beta: float = INF,
           count_runs: bool = False, guess_move_order: bool = True) -> float:
    if count_runs:
        global debug_count
        debug_count += 1

    if depth == 0:
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
        evaluation = -search(board, depth - 1, -beta, -alpha, count_runs=count_runs, guess_move_order=guess_move_order)
        board.pop()
        if evaluation != 0:
            logging.debug(f"Eval for {move}: {evaluation}")
        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)
    return alpha


@profile
def next_move(board: chess.Board, depth: int) -> chess.Move:
    moves = list(board.legal_moves)
    order_moves(board, moves)
    best_eval = -INF
    best_move = None
    for move in moves:
        board.push(move)
        
        if (curr_eval := -search(board, 3)) > best_eval:
            best_eval = curr_eval
            best_move = move
        board.pop()
    return best_move
