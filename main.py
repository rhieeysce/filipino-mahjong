from game.tile import Suit, Tile
from game.deck import Deck
from game.hand import Hand



def main():
    hand_test = Hand()
    hand_test.add(Tile(Suit.BALLS, 1))
    hand_test.add(Tile(Suit.BALLS, 1))
    hand_test.add(Tile(Suit.BALLS, 1))
    hand_test.add(Tile(Suit.BALLS, 1))
    hand_test.add(Tile(Suit.BALLS, 2))
    hand_test.add(Tile(Suit.BALLS, 2))
    hand_test.add(Tile(Suit.BALLS, 3))
    hand_test.add(Tile(Suit.BALLS, 3))
    hand_test.add(Tile(Suit.BALLS, 3))
    hand_test.add(Tile(Suit.BALLS, 4))
    hand_test.add(Tile(Suit.BALLS, 4))
    hand_test.add(Tile(Suit.BALLS, 4))
    hand_test.add(Tile(Suit.BALLS, 5))
    hand_test.add(Tile(Suit.BALLS, 5))
    hand_test.add(Tile(Suit.BALLS, 5))
    hand_test.add(Tile(Suit.BALLS, 6))
    hand_test.add(Tile(Suit.BALLS, 6))
    hand_test.add(Tile(Suit.BALLS, 6))



    print(hand_test)
    print(len(hand_test))

if __name__ == "__main__":
    main()