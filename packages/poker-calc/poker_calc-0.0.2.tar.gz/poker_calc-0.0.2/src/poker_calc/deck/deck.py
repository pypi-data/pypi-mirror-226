from ..constants.ranks import RANKS
from ..constants.suites import SUITES
from ..card.card import Card 
from typing import List
from random import shuffle

class Deck:
    def __init__(self) -> None:
        self.cards:list[Card] = []
        self.deck_size = 52
        # Make 13 instances of a card with increment values of one suite * 4 for every suite.
        for suite in SUITES.values():
            value = 2
            for rank,name in RANKS.items():
                card = Card(name, rank, suite, value)
                self.cards.append(card)
                value += 1
    

    def show_all_cards(self) -> None:
        for i in range (len(self.cards)):
            print(self.cards[i].suite, " ",self.cards[i].rank, " " , self.cards[i].value )

    def remove_card(self, card:str):
        if self.verify_card(card) != ValueError:
            for element in self.cards:
                if element.rank == card:
                    return self.cards.pop(self.cards.index(element))

    def add_cards(self, cards) -> None:
        for card in cards:
            if self.verify_card(card) != ValueError:
                self.cards.append(card)

    def remove_cards(self, cards:list) -> List[Card]:
        removed_cards = []
        for card in cards:
            card = self.remove_card(card)
            removed_cards.append(card)
        return removed_cards
    
    def verify_card(self, card:str) -> str:
        if card[:-1] not in RANKS.keys(): # Makes 10s to be 10 (slices away last element) 
            raise ValueError(f"Card: '{card}' not a valid rank! Allowed: {tuple(RANKS.keys())}")
        elif card[-1] not in SUITES.keys(): # Checks if last element is in valid suites
            raise ValueError(f"Card: '{card}' not a valid suite! Allowed: {tuple(SUITES.keys())}")
        elif card not in [card.rank for card in self.cards]: # Checks if for somereason card already moved from the deck
            raise ValueError(f"Card: '{card}' already in use aka out of the deck(dublicate)")
        else:
            return card

    def riffle_shuffel(self) -> None: # TODO: Riffle-shuffel algorithm
        shuffle(self.cards)
        # Tests showed that there is no point of having an proper shuffling algorithm
