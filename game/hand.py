from .tile import Tile, Suit


def _can_decompose(counts: list) -> bool:
    for i in range(1, 10):
        if counts[i] > 0:
            if counts[i] >= 4:
                counts[i] -= 4
                if _can_decompose(counts):
                    counts[i] += 4
                    return True
                counts[i] += 4
            if counts[i] >= 3:
                counts[i] -= 3
                if _can_decompose(counts):
                    counts[i] += 3
                    return True
                counts[i] += 3
            if i + 2 <= 9 and counts[i+1] >= 1 and counts[i+2] >= 1:
                counts[i] -= 1
                counts[i+1] -= 1
                counts[i+2] -= 1
                if _can_decompose(counts):
                    counts[i] += 1
                    counts[i+1] += 1
                    counts[i+2] += 1
                    return True
                counts[i] += 1
                counts[i+1] += 1
                counts[i+2] += 1
            return False
    return True


class Hand:
    def __init__(self):
        self._balls = [0] * 10
        self._sticks = [0] * 10
        self._chars = [0] * 10
        self._locked_mades: list[list[Tile]] = []  # revealed (chow/pong/kong claims)
        self._secret_mades: list[list[Tile]] = []  # concealed (self-drawn kongs)

    def _suit_array(self, suit: Suit) -> list:
        if suit == Suit.BALLS:
            return self._balls
        elif suit == Suit.STICKS:
            return self._sticks
        elif suit == Suit.CHARACTERS:
            return self._chars
        raise ValueError(f"Invalid suit: {suit}")

    def add(self, tile: Tile):
        self._suit_array(tile.suit)[tile.value] += 1

    def discard(self, tile: Tile) -> int:
        if tile.suit == Suit.FLOWERS:
            return 0
        arr = self._suit_array(tile.suit)
        if arr[tile.value] > 0:
            arr[tile.value] -= 1
            return 1
        return 0

    def has_tile(self, tile: Tile) -> bool:
        if tile.suit == Suit.FLOWERS:
            return False
        return self._suit_array(tile.suit)[tile.value] > 0

    def count_tile(self, tile: Tile) -> int:
        if tile.suit == Suit.FLOWERS:
            return 0
        return self._suit_array(tile.suit)[tile.value]

    def can_chow(self, tile: Tile) -> list[list[int]]:
        if tile.suit == Suit.FLOWERS:
            return []
        arr = self._suit_array(tile.suit)
        v = tile.value
        result = []
        for start in range(max(1, v - 2), min(7, v) + 1):
            seq = [start, start + 1, start + 2]
            others = [x for x in seq if x != v]
            if all(arr[x] > 0 for x in others):
                result.append(seq)
        return result

    def can_pong(self, tile: Tile) -> bool:
        return self.count_tile(tile) >= 2

    def can_kong(self, tile: Tile) -> bool:
        return self.count_tile(tile) >= 3

    def would_complete_secret(self, tile: Tile) -> bool:
        return self.count_tile(tile) == 3

    def lock_claimed_made(self, tiles: list[Tile]):
        for tile in tiles:
            self.discard(tile)
        self._locked_mades.append(list(tiles))

    def lock_secret(self, suit: Suit, value: int):
        self._suit_array(suit)[value] -= 4
        self._secret_mades.append([Tile(suit, value)] * 4)

    def clear(self):
        self._balls = [0] * 10
        self._sticks = [0] * 10
        self._chars = [0] * 10
        self._locked_mades = []
        self._secret_mades = []

    def is_mahjong(self) -> bool:
        suits = [self._balls, self._sticks, self._chars]
        n_locked = len(self._locked_mades) + len(self._secret_mades)
        free_total = sum(sum(s[1:]) for s in suits)

        # Condition 1: one pair + remaining tiles as mades (locked mades pre-counted)
        for suit in suits:
            for value in range(1, 10):
                if suit[value] >= 2:
                    suit[value] -= 2
                    if all(_can_decompose(s[:]) for s in suits):
                        suit[value] += 2
                        return True
                    suit[value] += 2

        # Condition 2: seven pairs + one made
        if n_locked >= 1:
            # Locked made serves as the "1 made"; free tiles must be exactly 7 pairs
            if free_total == 14 and all(s[v] % 2 == 0 for s in suits for v in range(1, 10)):
                return True
        else:
            for suit in suits:
                for value in range(1, 10):
                    if suit[value] >= 3:
                        suit[value] -= 3
                        if all(s[v] % 2 == 0 for s in suits for v in range(1, 10)):
                            suit[value] += 3
                            return True
                        suit[value] += 3
                    if value + 2 <= 9 and suit[value] >= 1 and suit[value+1] >= 1 and suit[value+2] >= 1:
                        suit[value] -= 1
                        suit[value+1] -= 1
                        suit[value+2] -= 1
                        if all(s[v] % 2 == 0 for s in suits for v in range(1, 10)):
                            suit[value] += 1
                            suit[value+1] += 1
                            suit[value+2] += 1
                            return True
                        suit[value] += 1
                        suit[value+1] += 1
                        suit[value+2] += 1

        return False

    def __len__(self) -> int:
        free = sum(self._balls) + sum(self._sticks) + sum(self._chars)
        locked = sum(len(m) for m in self._locked_mades) + sum(len(m) for m in self._secret_mades)
        return free + locked

    def __str__(self) -> str:
        hand_str = []
        suits = {"Balls": self._balls, "Sticks": self._sticks, "Characters": self._chars}
        for suit_name, suit_list in suits.items():
            tiles = []
            for value, count in enumerate(suit_list):
                if count > 0:
                    tiles.extend([str(value)] * count)
            if tiles:
                hand_str.append(f"{suit_name}: {' '.join(tiles)}")
        for made in self._locked_mades:
            hand_str.append(f"[Locked: {', '.join(str(t) for t in made)}]")
        for _ in self._secret_mades:
            hand_str.append("[Secret Kong]")
        return "\n".join(hand_str) if hand_str else "Empty hand"
