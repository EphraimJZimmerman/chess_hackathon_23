from bot import Bot
from test_bot import get_move
from grob import evaluator
import logging

from tests.grob.random_bot import RandomBot

# logging.basicConfig(level=logging.DEBUG)

grob_bot = Bot(depth=5, debug=True)
random_bot = RandomBot()
random_bot.board = grob_bot.board

while not grob_bot.board.is_game_over():
    evaluator.reset_debug_vars()
    move = grob_bot.next_move()
    grob_bot.board.push_san(move)
    print(f"move: {move}, count: {evaluator.debug_search_count}, depth: {evaluator.debug_search_depth}")

    logging.debug(grob_bot.board.turn)
    logging.debug(-evaluator.evaluate(grob_bot.board))

    if grob_bot.board.is_game_over():
        break

    move = random_bot.next_move()
    grob_bot.board.push_san(move)

    logging.debug(grob_bot.board.turn)
    logging.debug(-evaluator.evaluate(grob_bot.board))

    if grob_bot.board.is_game_over():
        break

