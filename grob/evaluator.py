import chess

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3.1,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}


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


def next_move(board: chess.Board) -> chess.Move:
    ...
