"""
Credit to Sebastian Lague for the quick script
"""

import chess.pgn
import random
import math

pgn = open("data/lichess_db_standard_rated_2016-04.pgn")
positions = []

for i in range(150000):
    game = chess.pgn.read_game(pgn)
    moves = game.mainline_moves()
    board = game.board()

    plyToPlay = math.floor(16 + 20 * random.random()) & ~1

    numPlyPlayed = 0
    for move in moves:
        board.push(move)
        numPlyPlayed += 1
        if numPlyPlayed == plyToPlay:
            fen = board.fen()

    numPiecesInPos = sum(fen.lower().count(char) for char in "rnbq")
    if numPlyPlayed > plyToPlay + 20 * 2 and numPiecesInPos >= 10:
        positions.append(game.headers['Opening'])
        positions.append(fen)

with open("output.txt", "w") as file:
    for string in positions:
        file.write(string + "\n")
