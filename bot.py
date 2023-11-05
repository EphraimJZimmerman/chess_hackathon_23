"""
The Brandeis Quant Club ML/AI Competition (November 2023)

Author: @Ephraim Zimmerman
Email: quants@brandeis.edu
Website: brandeisquantclub.com; quants.devpost.com

Description:

For any technical issues questions or additional assistance please feel free to reach out to
the "on-call" hackathon support team via email at quants@brandeis.edu

Website/GitHub Repository:
You can find the latest updates, documentation, and additional resources for this project on the
official website or GitHub repository: https://github.com/EphraimJZimmerman/chess_hackathon_23

License:
This code is open-source and released under the MIT License. See the LICENSE file for details.
"""

import random
import chess
import time
from collections.abc import Iterator
from contextlib import contextmanager
import test_bot


@contextmanager
def game_manager() -> Iterator[None]:
    """Creates context for game."""

    # DO NOT EDIT. This is used for judging.

    print("===== GAME STARTED =====")
    ping: float = time.perf_counter()
    try:
        yield
    finally:
        pong: float = time.perf_counter()
        total = pong - ping
        print(f"Total game time = {total:.3f} seconds")
    print("===== GAME ENDED =====")


class Bot:
    def __init__(self):
        self.board = chess.Board()

    def check_move_is_legal(self, initial_position, new_position) -> bool:

        """
            To check if, from an initial position, the new position is valid.

            Args:
                initial_position (str): The starting position given chess notation
                new_position (str): The new position given chess notation

            Returns:
                bool: If this move is legal
        """

        return chess.Move.from_uci(initial_position + new_position) in self.board.legal_moves

    def next_move(self) -> str:
        """
            The main call and response loop for playing a game of chess.

            Returns:
                str: The current location and the next move. For example, e3e4.
        """

        # Assume that you are playing an arbitrary game. This function, which is
        # the core "brain" of the bot, should return the next move in any circumstance.

        move = str(random.choice([_ for _ in self.board.legal_moves]))
        print("My move: " + move)
        return move


if __name__ == "__main__":

    chess_bot = Bot()
    with game_manager():

        # Modify this in any way you'd like!
        playing = True

        while playing:
            if chess_bot.board.turn:
                chess_bot.board.push_san(test_bot.get_move(chess_bot.board))
            else:
                chess_bot.board.push_san(chess_bot.next_move())
            print(chess_bot.board, end="\n\n")

            if chess_bot.board.is_game_over():
                if chess_bot.board.is_stalemate():
                    print("Is stalemate")
                elif chess_bot.board.is_insufficient_material():
                    print("Is insufficient material")

                # EX: Outcome(termination=<Termination.CHECKMATE: 1>, winner=True)
                print(chess_bot.board.outcome())
                playing = False
