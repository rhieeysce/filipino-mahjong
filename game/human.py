from .player import Player
from .tile import Tile, Suit
from .deck import Deck

_SUIT_CODES = {'b': Suit.BALLS, 's': Suit.STICKS, 'c': Suit.CHARACTERS}


class Human(Player):
    def __init__(self, name: str, deck: Deck):
        super().__init__(name, deck)

    def choose_discard(self) -> Tile:
        print(f"\nYour hand:\n{self.hand}")
        while True:
            raw = input("Discard (suit value — b/s/c 1-9, e.g. 'b 5'): ").strip().lower().split()
            if len(raw) != 2 or raw[0] not in _SUIT_CODES or not raw[1].isdigit():
                print("Invalid input.")
                continue
            value = int(raw[1])
            if not (1 <= value <= 9):
                print("Value must be 1-9.")
                continue
            tile = Tile(_SUIT_CODES[raw[0]], value)
            if self.hand.has_tile(tile):
                return tile
            print("Tile not in hand.")

    def choose_action(self, chow_tile: Tile | None) -> str:
        if chow_tile is None:
            return 'bunot'
        print(f"\nYour turn. {chow_tile} is available to chow.")
        while True:
            choice = input("Action (bunot/chow): ").strip().lower()
            if choice in ('bunot', 'chow'):
                return choice
            print("Enter 'bunot' or 'chow'.")

    def choose_chow_tiles(self, claimed: Tile) -> list[int]:
        sequences = self.hand.can_chow(claimed)
        if len(sequences) == 1:
            others = [v for v in sequences[0] if v != claimed.value]
            print(f"Chow: {sequences[0]}")
            return others
        print("Available chow sequences:")
        for i, seq in enumerate(sequences):
            print(f"  {i + 1}: {seq}")
        while True:
            raw = input("Choose sequence number: ").strip()
            if raw.isdigit():
                idx = int(raw) - 1
                if 0 <= idx < len(sequences):
                    return [v for v in sequences[idx] if v != claimed.value]
            print("Invalid choice.")

    def choose_out_of_turn(self, discard: Tile) -> str:
        options = []
        if self.hand.can_kong(discard):
            options.append('kong')
        if self.hand.can_pong(discard):
            options.append('pong')
        self.hand.add(discard)
        if self.hand.is_mahjong():
            options.append('mahjong')
        self.hand.discard(discard)
        if not options:
            return 'pass'
        print(f"\n{self.name}: {discard} discarded. Options: {', '.join(options)}")
        while True:
            choice = input("Action (or pass): ").strip().lower()
            if choice == 'pass' or choice in options:
                return choice
            print(f"Choose from: {', '.join(options + ['pass'])}")
