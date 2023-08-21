from ..pokergame.pokergame import TexasHoldem
from .argparser import ArgParser


def cli():
    args = ArgParser()
    game = TexasHoldem()
    for i, p_cards in enumerate(args.player_cards):
        game.add_player(f"Player{i}", *p_cards)
    game.add_board(*args.board_cards)
    game.run(args.iterations)
    game.result()
