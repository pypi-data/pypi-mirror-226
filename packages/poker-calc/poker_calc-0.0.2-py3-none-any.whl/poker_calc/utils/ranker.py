from ..card.card import Card
from collections import Counter

def evaluate_hand(hand: list[Card]) -> int:
    """ Assuming that hand list is sorted by the highest rank as the last elemenet
    returns relative hand strenght value from 0-9
    """
    MAX = 5
    if len(hand) == MAX:
        # High card - low card == 4 # if True its a straight
        ranks = [card.get_rank for card in hand]
        dict_ranks = Counter(ranks)
        common_ranks = sorted(list(dict_ranks.values()))

        one_pair = common_ranks[-1] == 2 and common_ranks[-2] == 1
        two_pair = common_ranks[-1] == 2 and common_ranks[-2] == 2
        trips =  max(common_ranks) == 3 and common_ranks[-2] == 1 # aka theere of a kind
        straight = hand[-1].value - hand[0].value == 4 
        wheel = hand[-1].value == 14 and hand[-2].value == 5 # when Ace is the low card straight to 5
        flush = len(set(card.suite for card in hand)) == 1 
        fullhouse =  max(common_ranks) == 3 and common_ranks[-2] == 2
        quads =  max(common_ranks) == 4 # aka four of a kind
        royal_flush =  straight and flush and hand[0].value == 10

        if one_pair: 
            return 1 
        elif two_pair: 
            return 2
        elif trips: 
            return 3
        elif not flush and straight or wheel:
            return 4
        elif not straight and flush:
            return 5
        elif fullhouse:
            return 6
        elif quads:
            return 7
        elif wheel or straight and flush: # Straight flush 
            return 8 
        elif royal_flush:
            return 9
        return 0
    else:
        raise ValueError("Gotta be excatly 5 cards")

