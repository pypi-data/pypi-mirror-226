import argparse 


class ArgParser:
    def __init__(self) -> None:
        self._iterations = 20000 
        self.parser = argparse.ArgumentParser(description="""
                    TexasHoldem Odds Calculator!
    Calculates odds/probality of winning with Monte Carlo Simulation 
    Default iterations are set to 20'000 middle ground between speed and quality.
    By providing no board it will calculate preflop odds,
    by providing 3 cards it will run simulation of turn and river
    by providing board with 5 cards it will evaluate winner or a tie.
    Example usage: poker_calc -p 4s5s -p 6dTh -b AsKc2s --nolife
    Will run simulation 500'000 times!!!
                                         """, formatter_class=argparse.RawTextHelpFormatter)
        
        self.parser.add_argument('-p', '--player',  nargs='+', action='append', help='player cards in format: AsKd', metavar="")
        self.parser.add_argument('-b', '--board', help='Board cards either None(preflop) or 3-5(flop)', metavar="")
        self.parser.add_argument('--fast', action='store_const', const=5000, help='5000 iterations Monte Carlo simulation')
        self.parser.add_argument('--slow', action='store_const', const=100000, help='100000 iterations Monte Carlo simulation')
        self.parser.add_argument('--nolife', action='store_const', const=500000, help='500000 iterations Monte Carlo simulation')
        self.parser.add_argument('--interactive', action='store_true',help='Terminal interface version')
    
    def get_args(self):
        args = self.parser.parse_args()
        return args 
    
    @property
    def iterations(self):
        args = self.get_args()
        iterations = self._iterations
        
        if args.fast != None:
            iterations = args.fast

        if args.slow != None:
            iterations = args.slow

        if args.nolife != None:
            iterations = args.nolife
        return iterations

    @iterations.setter
    def iterations(self, iterations):
        self._iterations = iterations
    
    @property
    def player_cards(self) -> list[tuple]:
        args = self.get_args()
        cards = [] 
        if args.player != None:
            for card in args.player: # args.player is an nested list
                cards.extend(card)

        p_cards = [] # a list of player cards as tuple
        if cards != []:
            for i, card in enumerate(cards):
                if len(cards[i]) != 4: # cards = ['As4d'] so this check if there is 2 cards rank+suite
                    raise ValueError(f"Player should have exactly 2 cards, but got : -p {cards[i]}")
                p_cards += [(card[:2], card[2:])] # Then here its made into tuple of p_cards
        return p_cards

    @property
    def board_cards(self) -> tuple:
        args = self.get_args()
        board = ()
        if args.board != None:
            if len(args.board) == 10: # Didnt want to mess the Base code, but basicly if all 5 community cards are passed in then it runs sim once.
                self.iterations = 1
            board = tuple([args.board[i:i+2] for i in range(0, len(args.board), 2)])
        return board

def argparser():
    parser = argparse.ArgumentParser(description="""
                TexasHoldem Odds Calculator!
Calculates odds/probality of winning with Monte Carlo Simulation 
Default iterations are set to 20'000 middle ground between speed and quality.
By providing no board it will calculate preflop odds,
by providing 3 cards it will run simulation of turn and river
by providing board with 5 cards it will evaluate winner or a tie.
Example usage: poker_calc -p 4s5s -p 6dTh -b AsKc2s --nolife
Will run simulation 500'000 times!!!
                                     """, formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('-p', '--player',  nargs='+', action='append', help='player cards in format: AsKd', metavar="")
    parser.add_argument('-b', '--board', help='Board cards either None(preflop) or 3-5(flop)', metavar="")
    parser.add_argument('--fast', action='store_const', const=5000, help='5000 iterations Monte Carlo simulation')
    parser.add_argument('--slow', action='store_const', const=100000, help='100000 iterations Monte Carlo simulation')
    parser.add_argument('--nolife', action='store_const', const=500000, help='500000 iterations Monte Carlo simulation')
    parser.add_argument('--interactive', action='store_true',help='Terminal interface version')

    args = parser.parse_args()
    
    iterations = 20000 # Default simulation value
    if args.fast != None:
        iterations = args.fast

    if args.slow != None:
        iterations = args.slow

    if args.nolife != None:
        iterations = args.nolife

    cards = [] 
    if args.player != None:
        for card in args.player: # args.player is an nested list
            cards.extend(card)

    p_cards = [] # a list of player cards as tuple
    if cards != []:
        try:
            for i, card in enumerate(cards):
                if len(cards[i]) != 4: # cards = ['As4d'] so this check if there is 2 cards rank+suite
                    raise ValueError(f"Player should have exactly 2 cards, but got : -p {cards[i]}")
                p_cards += [(card[:2], card[2:])] # Then here its made into tuple of p_cards
        except ValueError as err:
            print(err)

    board = ()
    if args.board != None:
        if len(args.board) == 10: # Didnt want to mess the Base code, but basicly if all 5 community cards are passed in then it runs sim once.
            iterations = 1
        board = tuple([args.board[i:i+2] for i in range(0, len(args.board), 2)])

    return p_cards, board, args.interactive, iterations, parser
