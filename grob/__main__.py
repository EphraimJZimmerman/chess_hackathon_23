from bot import Bot


bot = Bot("r2qkb1r/pp2nppp/3p4/2pNN1B1/2BnP3/3P4/PPP2PPP/R2bK2R w KQkq - 1 0")
print(bot.board, end="\n\n")
next_move = bot.next_move()
print(f"{next_move=}")

bot.board.push_san(next_move)
print(bot.board, end="\n\n")
