import logging
import time

import chess

import bot
from grob import evaluator
from tests.grob.random_bot import RandomBot


def evaluation_from_fen(fen: str) -> float:
    board = chess.Board(fen)
    return evaluator.search(board, 2)


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
    # test pawn avoiding
    board = chess.Board("r1bqkbnr/pppp1ppp/2n5/4p3/4P3/3P1N2/PPP2PPP/RNBQKB1R b KQkq - 0 3")
    silly_bishop = chess.Move(chess.square(5, 7), chess.square(0, 2))
    not_silly_bishop = chess.Move(chess.square(5, 7), chess.square(1, 3))
    assert evaluator.guess_move_evaluation(board, silly_bishop) < 0
    assert evaluator.guess_move_evaluation(board, not_silly_bishop) >= 0


def test_ordering_is_more_efficient():
    without_order_number_total = 0
    without_order_time_total = 0
    with_order_number_total = 0
    with_order_time_total = 0

    with open("../data/test_positions.txt", "r") as games:
        for count, line in enumerate(games):
            if count == 10:
                break
            if count % 2 == 1:
                position = chess.Board(line)
                evaluator.reset_debug_vars()
                start = time.perf_counter()
                evaluator.search(position, 3, count_runs=True, guess_move_order=False)
                without_order_number_total += evaluator.debug_search_count
                without_order_time_total += time.perf_counter() - start

                evaluator.reset_debug_vars()
                start = time.perf_counter()
                evaluator.search(position, 3, count_runs=True, guess_move_order=True)
                with_order_number_total += evaluator.debug_search_count
                with_order_time_total += time.perf_counter() - start
    assert with_order_number_total < without_order_number_total
    assert with_order_time_total < without_order_time_total


def test_two_bots(new: bot.Bot, old: bot.Bot, number_games: int = 10) -> tuple[int, int, int]:
    old.board = new.board = chess.Board()
    wins = draws = loses = 0
    news_color = chess.WHITE
    while not new.board.is_game_over():
        if new.board.turn == news_color:
            news_move = new.next_move()
            new.board.push_san(news_move)
        else:
            olds_move = old.next_move()
            new.board.push_san(olds_move)
    if new.board.is_stalemate():
        draws += 1
    elif new.board.is_checkmate():
        if new.board.turn == news_color:
            wins += 1
        else:
            loses += 1
    return wins, draws, loses


def test_grob_beats_random():
    wins, draws, loses = test_two_bots(RandomBot(), bot.Bot(), number_games=1)
    assert wins == 1