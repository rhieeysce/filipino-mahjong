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
        
        
    #returns true if the hand has mahjong
    #does not account for 7 pairs
    #WIP
    def is_mahjong(self):
        
        pairs = self.check_pairs()
        if pairs == 1:
            trips = self.check_trips()
            straights = self.check_straights()
            quads = self.check_quads()
            
            if trips + quads + straights == 5:
                return True
        
        return False
        
     #return the number of quads in the hand
    def check_quads(self):
        ans = 0
        for i in range(10):
            if self._balls[i] == 4:
                ans += 1
            if self._sticks[i] == 4:
                ans += 1
            if self._chars[i] == 4:
                ans += 1
        return ans
            
     
    #returns the number of three of a kinds in the hand
    #counts kang as 2 trips
    #WIP sliding window?
    def check_trips(self):    
        ans = 0
        for i in range(10):
            if self._balls[i] == 3:
                ans += 1
            if self._sticks[i] == 3:
                ans += 1
            if self._chars[i] == 3:
                ans += 1
        return ans
        
        
    #returns the number of pairs in the hand
    #doesnt work!!!!! 11 123 
    def check_pairs(self): 
        ans = 0
        for i in range(10):
            if self._balls[i] == 2:
                ans += 1
            if self._sticks[i] == 2:
                ans += 1
            if self._chars[i] == 2:
                ans += 1
        return ans
        
        
    #returns the number of 3 tile sequences in the hand
    #how to check 1,1,2,2,3,3 for 2 straights?
    #WIP
    def check_straights(self):
        L = 0
        C = 1
        R = 2
        return 0
        
        
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