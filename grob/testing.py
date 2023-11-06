import chess

from grob import evaluator


def evaluation_from_fen(fen: str) -> float:
    board = chess.Board(fen)
    return evaluator.search(board, 2, -evaluator.INF, evaluator.INF)


def test_obvious_black_win():
    obvious_black_win = "rnbqkb1r/ppp1pppp/5n2/3p4/2QP4/8/PPP1PPPP/RNB1KBNR b KQkq - 0 1"
    assert evaluation_from_fen(obvious_black_win) > 5


def test_obvious_black_lose():
    obvious_black_lose = "8/1R6/8/8/8/8/2K5/k7 b - - 0 1"
    assert evaluation_from_fen(obvious_black_lose) < 10


def test_guess_move_evaluation():
    board = chess.Board("r1bqkbnr/pppp1ppp/2n5/4p3/3PP3/5N2/PPP2PPP/RNBQKB1R b KQkq d3 0 3")
    knight_takes = chess.Move(chess.square(2, 5), chess.square(3, 3))
    pawn_takes = chess.Move(chess.square(4, 4), chess.square(3, 3))
    none_takes = chess.Move(chess.square(3, 6), chess.square(3, 4))
    # prioritizes the correct captures
    assert evaluator.guess_move_evaluation(board, pawn_takes) > evaluator.guess_move_evaluation(board, knight_takes)
    assert evaluator.guess_move_evaluation(board, knight_takes) > evaluator.guess_move_evaluation(board, none_takes)