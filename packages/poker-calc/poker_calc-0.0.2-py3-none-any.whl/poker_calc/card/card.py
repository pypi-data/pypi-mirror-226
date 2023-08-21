from ..constants.suites import PRETTY

class Card:
    def __init__(self, name:str, rank:str, suite:str, value:int) -> None:
        self._name:str = name
        self._rank:str = rank
        self._suite:str = suite
        self._value:int = value
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def rank(self) -> str:
        #Make formated rank string like: As (Ace of Spades)
        rank = self._rank+self._suite[0].lower() 
        return rank

    @property 
    def get_rank(self) -> str:
        return self._rank

    @property
    def suite(self) -> str:
        return self._suite

    @property
    def value(self) -> int:
        return self._value
    
    def pretty_str(self) -> str:
        pretty = PRETTY.get(self.suite[0].lower())
        rank_suite = ""
        if pretty is not None:
           rank_suite = self.get_rank + pretty 
        return rank_suite

    def __str__(self) -> str:
        return self.rank

    def __repr__(self) -> str:
        return self.__str__()

