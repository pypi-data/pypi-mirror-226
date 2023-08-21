from ..card.card import Card
from typing import Tuple, List

class Player:
    def __init__(self, name:str, cards:List[Card]):
        self._name:str = str(name)
        self._cards:List[Card] = cards   # player cards
        self._hole_cards:List[Card] = [] # Hole cards + community_cards (5 max)
        self._score:int = 0              # Hands strenght
        self.runs:int = 0                # Sim run count
        self.wins:int = 0                # sim run wins 
        self.ties:int = 0                # sim run ties
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def score(self) -> int:
        return self._score

    def update_score(self, new_score:int) -> None:
        if not isinstance(new_score, int):
            raise ValueError("Score must be an type of int")
        self._score = new_score
    
    @property
    def cards(self) -> Tuple:
        cards = tuple([card.rank for card in self._cards])
        return cards
    
    def pretty_cards(self) -> str:
        cards = tuple([str(card.pretty_str()) for card in self._cards])
        return ' '.join(cards)

    def add_cards(self, cards:list) -> None:
        if not isinstance(cards, list):
            raise ValueError("Cards must be an type of list")
        self._cards = cards
    
    def make_hand(self, community_cards:List[Card]) -> None:
        # TODO: I guess make it only relevant cards (5max) as turn and river comes*
        self._hole_cards = self._cards + community_cards
        self.sort()

    def sort(self) -> None:
        # Sorts the hand in acceding order by cards value.
        self._hole_cards.sort(key=lambda x: x.value)

    def __str__(self) -> str:
        odds = round(self.wins/self.runs * 100, 2)
        tie = round(self.ties/self.runs * 100, 2)
        return f"{self.name}: {self.pretty_cards()} \nWin: {odds}%\nTie: {tie}%"  
