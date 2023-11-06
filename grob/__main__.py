from bot import Bot
from test_bot import get_move
from grob import evaluator
import logging

# logging.basicConfig(level=logging.DEBUG)


grob_bot = Bot()

while not grob_bot.board.is_game_over():
    input()
    move = grob_bot.next_move()
    grob_bot.board.push_san(move)
    print(grob_bot.board.turn, evaluator.evaluate(grob_bot.board))
    print(grob_bot.board, end="\n\n")

    if grob_bot.board.is_game_over():
        break

    input()

    move = get_move(grob_bot.board)
    grob_bot.board.push_san(move)
    print(grob_bot.board.turn, evaluator.evaluate(grob_bot.board))
    print(grob_bot.board, end="\n\n")

