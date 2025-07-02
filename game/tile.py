from __future__ import annotations
from enum import Enum

class Suit(Enum):
    STICKS = "Sticks"
    BALLS = "Balls"
    CHARACTERS = "Characters"
    FLOWERS = "Flowers"
    
class Tile():
    def __init__(self, suit: Suit, value: int):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        return f"{self.value} {self.suit.value}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tile):
            return NotImplemented
        return self.suit == other.suit and self.value == other.value
    