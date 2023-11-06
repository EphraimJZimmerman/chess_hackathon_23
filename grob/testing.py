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
