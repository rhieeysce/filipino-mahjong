from game.tile import Suit, Tile
from game.deck import Deck
from game.hand import Hand



def main():
    game_deck = Deck()
    player_hand = Hand()
    
    print(game_deck)
    print(player_hand)

if __name__ == "__main__":
    main()