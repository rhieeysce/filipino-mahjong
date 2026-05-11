from .deck import Deck
from .tile import Tile, Suit
from .player import Player
from .human import Human
from .cpu import CPU


class _GameOver(Exception):
    def __init__(self, winner: Player):
        self.winner = winner


class GameState:
    def __init__(self, human_name: str = "Player"):
        self.deck = Deck()
        self.deck.reset()
        self.players: list[Player] = [
            Human(human_name, self.deck),
            CPU("CPU 1", self.deck),
            CPU("CPU 2", self.deck),
            CPU("CPU 3", self.deck),
        ]
        self.current_idx: int = 0
        self.last_discard: Tile | None = None
        self.last_discard_player_idx: int | None = None
        self._deal()

    def _deal(self):
        for player in self.players:
            for _ in range(16):
                tile = self._draw_and_handle_secret(player)
                player.hand.add(tile)

    def _draw_and_handle_secret(self, player: Player) -> Tile:
        drawn = self.deck.bunot()
        while drawn.suit == Suit.FLOWERS:
            drawn = self.deck.flower()

        while player.hand.would_complete_secret(drawn):
            player.hand.add(drawn)
            player.hand.lock_secret(drawn.suit, drawn.value)
            print(f"\n{player.name}: Secret Kong!")
            drawn = self.deck.flower()
            while drawn.suit == Suit.FLOWERS:
                drawn = self.deck.flower()

        return drawn

    def _execute_chow(self, player: Player, claimed: Tile):
        other_values = player.choose_chow_tiles(claimed)
        player.hand.add(claimed)
        tiles = [claimed] + [Tile(claimed.suit, v) for v in other_values]
        player.hand.lock_claimed_made(tiles)
        print(f"\n{player.name} reveals Chow: {[str(t) for t in tiles]}")
        self.last_discard = None

    def _resolve_claims(self, discard: Tile, discarder_idx: int) -> int | None:
        priority = {'mahjong': 3, 'kong': 2, 'pong': 1}
        claims = []

        for i in range(1, 4):
            other_idx = (discarder_idx + i) % 4
            other = self.players[other_idx]
            action = other.choose_out_of_turn(discard)
            if action != 'pass':
                claims.append((i, other_idx, other, action))

        if not claims:
            return None

        dist, claimer_idx, claimer, action = min(claims, key=lambda c: (-priority[c[3]], c[0]))

        claimer.hand.add(discard)

        if action == 'mahjong':
            raise _GameOver(claimer)

        n_tiles = 4 if action == 'kong' else 3
        made = [Tile(discard.suit, discard.value)] * n_tiles
        claimer.hand.lock_claimed_made(made)
        label = 'Kong' if action == 'kong' else 'Pong'
        print(f"\n{claimer.name} reveals {label}: {[str(t) for t in made]}")

        if action == 'kong':
            bonus = self.deck.flower()
            while bonus.suit == Suit.FLOWERS:
                bonus = self.deck.flower()
            claimer.hand.add(bonus)
            if claimer.hand.is_mahjong():
                raise _GameOver(claimer)

        new_discard = claimer.choose_discard()
        claimer.hand.discard(new_discard)
        self.deck.discard(new_discard)
        print(f"\n{claimer.name} discards: {new_discard}")
        self.last_discard = new_discard
        self.last_discard_player_idx = claimer_idx

        sub = self._resolve_claims(new_discard, claimer_idx)
        return sub if sub is not None else claimer_idx

    def _take_turn(self):
        current = self.players[self.current_idx]

        can_chow = (
            self.last_discard is not None
            and self.last_discard_player_idx == (self.current_idx - 1) % 4
            and bool(current.hand.can_chow(self.last_discard))
        )
        action = current.choose_action(self.last_discard if can_chow else None)

        if action == 'chow':
            self._execute_chow(current, self.last_discard)
        else:
            tile = self._draw_and_handle_secret(current)
            current.hand.add(tile)
            if isinstance(current, Human):
                print(f"\n  >> You drew: {tile} <<")

        if current.hand.is_mahjong():
            raise _GameOver(current)

        discard = current.choose_discard()
        current.hand.discard(discard)
        self.deck.discard(discard)
        print(f"\n{current.name} discards: {discard}")
        self.last_discard = discard
        self.last_discard_player_idx = self.current_idx

        claimer_idx = self._resolve_claims(discard, self.current_idx)
        self.current_idx = ((claimer_idx + 1) % 4) if claimer_idx is not None else ((self.current_idx + 1) % 4)

    def play(self) -> None:
        try:
            while True:
                self._take_turn()
        except _GameOver as e:
            print(f"\n{e.winner.name} wins! Mahjong!")
