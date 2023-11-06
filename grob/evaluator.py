import chess

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3.1,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}

INF = float("inf")


def material_balance(board: chess.Board) -> float:
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
    balance = material_balance(board)
    return balance


def search(board: chess.Board, depth: int, alpha: float, beta: float) -> float:
    if depth == 0:
        return evaluate(board)

    moves = board.legal_moves
    if moves.count() == 0:
        if board.is_checkmate():
            return -INF  # current player has lost
        else:
            return 0     # game is a draw

    for move in moves:
        board.push(move)
        evaluation = -search(board, depth - 1, -beta, -alpha)
        board.pop()
        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)
    return alpha


def next_move(board: chess.Board) -> chess.Move:
    best_eval = -INF
    best_move = None
    for move in board.legal_moves:
        board.push(move)
        if (curr_eval := search(board, 3, -INF, INF)) > best_eval:
            best_eval = curr_eval
            best_move = move
        board.pop()
    return best_move
