from bot import Bot
from test_bot import get_move
from grob import evaluator
import logging

# logging.basicConfig(level=logging.DEBUG)


grob_bot = Bot()

while not grob_bot.board.is_game_over():
    move = grob_bot.next_move()
    grob_bot.board.push_san(move)

    logging.debug(grob_bot.board.turn)
    logging.debug(-evaluator.evaluate(grob_bot.board))

    if grob_bot.board.is_game_over():
        break

    move = get_move(grob_bot.board)
    grob_bot.board.push_san(move)

    logging.debug(grob_bot.board.turn)
    logging.debug(-evaluator.evaluate(grob_bot.board))

