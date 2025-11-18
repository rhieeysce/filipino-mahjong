from .hand import Hand
from .tile import Tile, Suit
from .deck import Deck


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.deck = Deck()
    
    def draw_tile(self):
        tile = self.deck.bunot()
        while tile.suit == Suit.FLOWERS:
            tile = self.deck.flower()
        self.hand.add(tile)
        return tile
    
    def discard_tile(self, tile: Tile):
        if self.hand.discard(tile):
            self.deck.discard(tile)
            return True
        return False
    
    def reset_hand(self):
        self.hand.clear()


