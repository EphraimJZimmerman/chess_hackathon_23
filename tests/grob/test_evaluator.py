import time

import chess

import bot
from grob import evaluator
from tests.random_bot import RandomBot


def evaluation_from_fen(fen: str) -> float:
    board = chess.Board(fen)
    return evaluator.search(board, 2)[0]


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
                evaluator.search(position, 3, debug_counts=True, guess_move_order=False)
                without_order_number_total += evaluator.debug_search_count
                without_order_time_total += time.perf_counter() - start

                evaluator.reset_debug_vars()
                start = time.perf_counter()
                evaluator.search(position, 3, debug_counts=True, guess_move_order=True)
                with_order_number_total += evaluator.debug_search_count
                with_order_time_total += time.perf_counter() - start
    assert with_order_number_total < without_order_number_total
    assert with_order_time_total < without_order_time_total


def test_check_all_captures():
    board = chess.Board("r4rk1/1p2npb1/pqn1p2p/1B1pPbp1/Q2P4/1PN1BN2/P4PPP/2R1K2R b K - 0 14")
    evaluator.search(board, 0, search_captures=False, search_checks=False, debug_counts=True)
    depth_without_captures = evaluator.debug_search_depth
    count_without_captures = evaluator.debug_search_count

    evaluator.reset_debug_vars()
    evaluator.search(board, 0, search_captures=True, search_checks=False, debug_counts=True)
    depth_with_captures = evaluator.debug_search_depth
    count_with_captures = evaluator.debug_search_count

    assert(depth_with_captures > depth_without_captures)

    board = chess.Board("8/8/8/8/1k6/8/2P2B2/2NR3K w - - 0 1")
    evaluator.reset_debug_vars()
    evaluator.search(board, 0, search_captures=True, search_checks=True, debug_counts=True)
    assert(evaluator.debug_search_depth > 0)


def test_endgame_skill():
    grob = bot.Bot(depth=4)
    wins, draws, losses = play_two_bots(grob, RandomBot(), 1, fen="8/8/4R3/5K2/8/2k5/8/8 w - - 0 1")
    assert wins == 1


def play_two_bots(new: bot.Bot, old: bot.Bot, number_games: int = 1, fen: str =chess.STARTING_FEN) -> tuple[int, int, int]:
    old.board = new.board = chess.Board(fen=fen)
    wins = draws = losses = 0
    for i in range(number_games):
        news_color = chess.WHITE if i % 2 == 0 else chess.BLACK
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
                losses += 1
            else:
                wins += 1
    return wins, draws, losses


def test_grob_beats_random():
    wins, draws, losses = play_two_bots(bot.Bot(), RandomBot(), number_games=1)
    assert wins == 1
