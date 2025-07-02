from .deck import Deck
from .tile import Tile, Suit

class Hand:
    def __init__(self):
        self._balls = []
        self._sticks = []
        self._chars = []
        
    #takes in a tile and adds it to the appropriate suit list
    def add(self, tile: Tile):
        if tile.suit == Suit.BALLS:
            self._balls.append(tile)
        elif tile.suit == Suit.STICKS:
            self._sticks.append(tile)
        elif tile.suit == Suit.CHARACTERS:
            self._chars.append(tile)
        else:
            raise ValueError("Invalid tile suit")
    
    #takes in a tile and discards it from the hand
    def discard(self, tile:Tile):
        if tile.suit == Suit.BALLS:
            self._balls.remove(tile)
        elif tile.suit == Suit.STICKS:
            self._sticks.remove(tile)
        elif tile.suit == Suit.CHARACTERS:
            self._chars.remove(tile)
        else:
            raise ValueError("Invalid tile suit")
        
    #organizes the hand within each suit
    def organize(self):
        self._balls.sort(key=lambda tile: tile.value)
        self._sticks.sort(key=lambda tile: tile.value)
        self._chars.sort(key=lambda tile: tile.value)
        
    #clears the hand
    def clear(self):
        self._balls.clear()
        self._sticks.clear()
        self._chars.clear()
        
    #returns the number of tiles in the hand
    def __len__(self):
        return len(self._balls) + len(self._sticks) + len(self._chars)
    
    #prints the hand
    def __str__(self):
        return (f"Balls: {', '.join(tile.value for tile in self._balls)}\n" +
                f"Sticks: {', '.join(tile.value for tile in self._sticks)}\n" +
                f"Characters: {', '.join(tile.value for tile in self._chars)}")
    