import random
from .player import Player
from .tile import Tile, Suit
from .deck import Deck


class CPU(Player):
    def __init__(self, name: str, deck: Deck):
        super().__init__(name, deck)

    def choose_discard(self) -> Tile:
        suits = [
            (Suit.BALLS, self.hand._balls),
            (Suit.STICKS, self.hand._sticks),
            (Suit.CHARACTERS, self.hand._chars),
        ]
        tiles = [Tile(suit, v) for suit, arr in suits for v in range(1, 10) if arr[v] > 0]
        return random.choice(tiles)

    def choose_action(self, chow_tile: Tile | None) -> str:
        return 'bunot'

    def choose_chow_tiles(self, claimed: Tile) -> list[int]:
        sequences = self.hand.can_chow(claimed)
        return [v for v in sequences[0] if v != claimed.value]

    def choose_out_of_turn(self, discard: Tile) -> str:
        self.hand.add(discard)
        if self.hand.is_mahjong():
            self.hand.discard(discard)
            return 'mahjong'
        self.hand.discard(discard)
        if self.hand.can_kong(discard):
            return 'kong'
        if self.hand.can_pong(discard):
            return 'pong'
        return 'pass'
