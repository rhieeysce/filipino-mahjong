from collections import deque
import random

from .tile import Tile, Suit


class Deck:
    def __init__(self):
        self._tiles = []
        self.allTiles()
        self._deck = deque()
        self._discarded = []
        
        
    def allTiles(self):
        for suit in Suit:
            for value in range(1, 10):
                for count in range(4):
                    self._tiles.append(Tile(suit, value))
        
    #resets the deck to a full shuffled set of tiles      
    def reset(self):
        random.shuffle(self._tiles)
        self._deck = deque(self._tiles)
       
    #pulls a tile from the deck
    def bunot(self):
        if not self._deck:
            self.reshuffleDiscarded()
        return self._deck.popleft()
       
    #pulls a tile from the flower stack 
    def flower(self):
        if not self._deck:
            self.reshuffleDiscarded()
        return self._deck.pop()
    
    def discard(self, tile: Tile):
        self._discarded.append(tile)
    
    #ONLY called when the deck is empty
    #reshuffles the discarded tiles back into the deck
    #raises ValueError if there are no discarded tiles
    def reshuffleDiscarded(self):
        if not self._discarded:
            raise ValueError("No discarded tiles to reshuffle")
        random.shuffle(self._discarded)
        self._deck = deque(self._discarded)
        self._discarded = []
        
    
    #returns the number of tiles in the deck
    def __len__(self):
        return len(self._deck)
    
    #prints every tile in the deck
    def __str__(self):
        return '\n'.join(str(tile) for tile in self._deck)