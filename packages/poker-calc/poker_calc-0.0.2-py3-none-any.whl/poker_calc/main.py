from poker_calc.pokergame.pokergame import TexasHoldem
from  poker_calc.interfaces.argparser import argparser
import time

def interactive():
    while True:
        print("-----------------------")
        print("TexasHoldem Odds Calculator")
        print("Here cards are in format As Kd rather than AsKd :)")
        p1_input = input("Your cards: ").strip()
        p1_cards = p1_input.split()
        
        p2_input = input("Player2 cards: ").strip()
        p2_cards = p2_input.split()

        b_input = input("Board cards (3-7cards): ").strip()
        board = b_input.split()
        try:
            start = time.time()
            game = TexasHoldem()
            game.add_player("You", *p1_cards)
            game.add_player("Player2", *p2_cards)
            game.add_board(*board)
            game.run(10000)
            game.result()
            print(f"Time elapsed:  {round(time.time() - start, 3)} sec \n")
            break
        except Exception as e:
            print(e)

def main(): 
    players_cards, board, interactive_mode, iterations, parser  = argparser() 

    if interactive_mode == True:
        interactive()
    elif players_cards != []:
        try:
            print("-----------------------")
            print("TexasHoldem Odds Calculator")
            game = TexasHoldem()
            for i, p_cards in enumerate(players_cards):
                game.add_player(f"Player{i+1}", *p_cards)

            game.add_board(*board)
            start = time.time()
            game.run(iterations)
            game.result()
            print(f"Time Elapsed: {round(time.time() - start, 3)} sec \n")
        except ValueError as err:
            print(err)
    else:
        parser.print_help() # if no args are present then it prints help message

if __name__ == "__main__":
    main()
