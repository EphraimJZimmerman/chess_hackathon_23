"""
python -m cProfile -m grob
"""


import cProfile

from bot import Bot

grob = Bot()

cProfile.run("grob.next_move(depth=2)")
