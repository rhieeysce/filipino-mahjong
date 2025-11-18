from .hand import Hand
from .tile import Tile, Suit
from .deck import Deck

class GameState:
    def __init__(self):
        self.players = []
        self.deck = Deck()
        