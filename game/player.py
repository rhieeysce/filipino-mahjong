from abc import ABC, abstractmethod
from .hand import Hand
from .tile import Tile
from .deck import Deck


class Player(ABC):
    def __init__(self, name: str, deck: Deck):
        self.name = name
        self.hand = Hand()
        self.deck = deck

    def discard_tile(self, tile: Tile) -> bool:
        if self.hand.discard(tile):
            self.deck.discard(tile)
            return True
        return False

    def reset_hand(self):
        self.hand.clear()

    @abstractmethod
    def choose_discard(self) -> Tile:
        ...

    @abstractmethod
    def choose_action(self, chow_tile: Tile | None) -> str:
        # Returns 'bunot' or 'chow'. chow_tile is the claimable discard, or None if not available.
        ...

    @abstractmethod
    def choose_chow_tiles(self, claimed: Tile) -> list[int]:
        # Returns the 2 hand-tile values that complete the sequence with claimed.
        ...

    @abstractmethod
    def choose_out_of_turn(self, discard: Tile) -> str:
        # Returns 'pong', 'kong', 'mahjong', or 'pass'.
        ...
