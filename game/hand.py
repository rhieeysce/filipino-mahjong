from .deck import Deck
from .tile import Tile, Suit

class Hand:
    def __init__(self):
        self._balls = [0] * 10
        self._sticks = [0] * 10
        self._chars = [0] * 10
        
    #takes in a tile and adds it to the appropriate suit list
    def add(self, tile: Tile):
        if tile.suit == Suit.BALLS:
            self._balls[tile.value] += 1
        elif tile.suit == Suit.STICKS:
            self._sticks[tile.value] += 1
        elif tile.suit == Suit.CHARACTERS:
            self._chars[tile.value] += 1
        else:
            raise ValueError("Invalid tile suit")
    
    #takes in a tile and discards it from the hand
    #returns 1 if successful, 0 if not found
    def discard(self, tile:Tile):
        if tile.suit == Suit.BALLS and self._balls[tile.value] > 0:
            self._balls[tile.value] -= 1
            return 1
        elif tile.suit == Suit.STICKS and self._sticks[tile.value] > 0:
            self._sticks[tile.value] -= 1
            return 1
        elif tile.suit == Suit.CHARACTERS and self._chars[tile.value] > 0:
            self._chars[tile.value] -= 1
            return 1
        else:
            return 0  # Tile not found in hand
                
    #clears the hand
    def clear(self):
        self._balls = [0] * 10
        self._sticks = [0] * 10
        self._chars = [0] * 10
        
        
    # returns True if the hand is a valid Mahjong hand
    # for every possible pair, remove the pair and check if the remaining tiles can form sets
    # Note: This is a simplified version and may not cover all Mahjong rules
    # remove the pair, remove the triplets and quads, and check if the rest can be split into sequences of 3
    def is_mahjong(self):
        
        def checkMades(suit):
            clone = suit.copy()
            # remove all triplets
            for i in range(1, 10):
                if clone[i] >= 3:
                    clone[i] -= 3
            for i in range(3, 10):
                if clone[i] >= 1 and clone[i-1] >= 1 and clone[i-2] >= 1:
                    clone[i] -= 1
                    clone[i-1] -= 1
                    clone[i-2] -= 1
            return sum(clone) == 0
        
        # remove every pair in balls suit
        # check if the rest can be split into trips and sequences of 3
        if sum(self._balls) % 3 == 2 and sum(self._sticks) % 3 == 0 and sum(self._chars) % 3 == 0:
            # remove pairs from balls
            for i in range(1, 10):
                if self._balls[i] >= 2:
                    self._balls[i] -= 2
                    if checkMades(self._balls) and checkMades(self._sticks) and checkMades(self._chars):
                        self._balls[i] += 2
                        return True
                    self._balls[i] += 2
                    
            return False
          
          
        # remove every pair in sticks suit
        # check if the rest can be split into trips and sequences of 3  
        elif sum(self._balls) % 3 == 0 and sum(self._sticks) % 3 == 2 and sum(self._chars) % 3 == 0:
            for i in range(1, 10):
                if self._sticks[i] >= 2:
                    self._sticks[i] -= 2
                    if checkMades(self._balls) and checkMades(self._sticks) and checkMades(self._chars):
                        self._sticks[i] += 2
                        return True
                    self._sticks[i] += 2
            return False
        
        # remove every pair in characters suit
        # check if the rest can be split into trips and sequences of 3
        elif sum(self._balls) % 3 == 0 and sum(self._sticks) % 3 == 0 and sum(self._chars) % 3 == 2:
            for i in range(1, 10):
                if self._chars[i] >= 2:
                    self._chars[i] -= 2
                    if checkMades(self._balls) and checkMades(self._sticks) and checkMades(self._chars):
                        self._chars[i] += 2
                        return True
                    self._chars[i] += 2
            return False

        return False
            
    
            
        
        
    #returns the number of tiles in the hand
    def __len__(self):
        return sum(self._balls) + sum(self._sticks) + sum(self._chars)
    
    #prints the hand
    def __str__(self):
        hand_str = []
        suits = {
            "Balls": self._balls,
            "Sticks": self._sticks,
            "Characters": self._chars
        }
        
        for suit_name, suit_list in suits.items():
            tiles = []
            for value, count in enumerate(suit_list):
                if count > 0:
                    tiles.extend([str(value)] * count)
            if tiles:
                hand_str.append(f"{suit_name}: {' '.join(tiles)}")
                
        return "\n".join(hand_str) if hand_str else "Empty hand"