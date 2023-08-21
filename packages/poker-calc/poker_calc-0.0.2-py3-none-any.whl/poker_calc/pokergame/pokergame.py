from typing import Iterable, List, Tuple, Dict
from ..player.player import Player
from ..card.card import Card
from ..deck.deck import Deck
from phevaluator import evaluate_cards as evaluate_hand

class TexasHoldem:
    def __init__(self) -> None:
        self.deck = Deck() 
        self._players:Dict[str, Player] = {} 
        self.community_cards: List[Card] = [] 
   
    @property
    def c_cards_str(self) -> List[str]:
        c_cards = [str(card.rank) for card in self.community_cards]
        return c_cards
    
    @property
    def pretty_c_cards(self) -> str:
        cards = tuple([str(card.pretty_str()) for card in self.community_cards]) 
        return ' '.join(cards) 

    @property
    def c_cards(self) -> Tuple[str]:
        return tuple(self.c_cards_str)

    @property
    def players(self) -> Iterable[Player]:
        return self._players.values()

    @property
    def players_list(self) -> List[Player]:
        return list(self.players)


    def get_player(self, player_name:str) -> Player:
        player = self._players.get(player_name)
        if player is None:
            raise ValueError("Player doesnt exist")
        else:
            return player 
    
    def add_player(self, player_name:str, *cards:str) -> str: 
        if not len(self.players_list) < 9:
            raise ValueError("Max players are 9")

        if not len(cards) == 2:
            raise ValueError(f"Player should have excatly 2 cards provided: {len(cards)}")
        p_cards = self.deck.remove_cards(list(cards))
        self._players[player_name] = Player(player_name, p_cards)
        return f"{player_name} joined the table"

    def add_board(self, *cards:str) -> None:
        if not 3 <= len(cards) <= 5 and not len(cards) == 0:
            raise ValueError(f"PreFlop odds no board, otherwise board must be between 3-7 cards provided: {len(cards)}cards")
        self.community_cards = self.deck.remove_cards(list(cards))

    def draw_board(self) -> str:
        board = self.pretty_c_cards
        if len(board) == 0:
            board = "Pre-Flop"
        return f"Board: {board}"

    def draw(self, index:int) -> Card: 
        return self.deck.cards[index]
    
    def draw_sim(self, index:int) -> str: 
        return str(self.draw(index))

    def evaluate_hands(self, *cards:Tuple[str]) -> None:
        for player in self._players.values():
            hand = player.cards + self.c_cards + cards
            result = evaluate_hand(*hand)
            player.update_score(result) 

    def __sim_winner_counter__(self) -> None:
        best_hand = min(player.score for player in self.players_list) 
        winners = [player for player in self.players_list if player.score == best_hand]
        if len(winners) == 1: # checks if there is only one winner
            winners[0].wins += 1
        else:
            for winner in winners: # Else its tie
                winner.ties += 1
    
    def run(self, iterations:int) -> None:
        for _ in range(iterations):
            self.deck.riffle_shuffel()
            needed_cards = []
            for i in range(5-len(self.community_cards)):
                needed_cards.append(self.draw_sim(1+i))
            self.evaluate_hands(*tuple(needed_cards)) 
            self.__sim_winner_counter__()
        
        for player in self.players_list:
            player.runs = iterations

    def result(self) -> None:
        print("-----------------------")
        print(self.draw_board())
        print("-----------------------")
        for player in self.players_list:
            print(player)
            print("-----------------------")
