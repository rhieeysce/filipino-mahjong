from collections import deque
import random

from .tile import Tile, Suit


class Deck:
    def __init__(self):
        self._tiles = []
        self._deck = deque()
        self.reset()
        
    #resets the deck to a full shuffled set of tiles      
    def reset(self):
        self._tiles.clear()
        for suit in Suit:
            for value in range(1, 10):
                for count in range(4):
                    self._tiles.append(Tile(suit, value))
        random.shuffle(self._tiles)
        self._deck = deque(self._tiles)
       
    #pulls a tile from the deck
    def bunot(self):
        if not self._deck:
            raise ValueError("Deck is empty")
        return self._deck.popleft()
       
    #pulls a tile from the flower stack 
    def flower(self):
        if not self._deck:
            raise ValueError("Deck is empty")
        return self._deck.pop()
    
    #returns the number of tiles in the deck
    def __len__(self):
        return len(self._deck)
    
    #prints every tile in the deck
    def __str__(self):
        return '\n'.join(str(tile) for tile in self._deck)