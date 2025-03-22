import random

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
          '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def deal_one(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'A':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

class Chips:
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            bet = int(input(f"You have ${chips.total}. How much would you like to bet? "))
        except ValueError:
            print("Invalid input. Please enter an integer.")
        else:
            if bet > chips.total:
                print("Bet cannot exceed your total chips!")
            else:
                chips.bet = bet
                break

def hit(deck, hand):
    hand.add_card(deck.deal_one())

def show_some(player, dealer):
    print("\nDealer's Hand:")
    print("<hidden card>", dealer.cards[1])
    print("\nPlayer's Hand:")
    print(player)
    print(f"Value: {player.value}")

def show_all(player, dealer):
    print("\nDealer's Hand:")
    print(dealer)
    print(f"Value: {dealer.value}")
    print("\nPlayer's Hand:")
    print(player)
    print(f"Value: {player.value}")

def player_busts(chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(chips):
    print("Dealer busts! Player wins!")
    chips.win_bet()

def dealer_wins(chips):
    print("Dealer wins!")
    chips.lose_bet()

def push():
    print("It's a push! Tie game.")

def play_game():
    print("Welcome to Blackjack!")
    chips = Chips()

    while True:
        deck = Deck()
        player_hand = Hand()
        dealer_hand = Hand()

        for _ in range(2):
            player_hand.add_card(deck.deal_one())
            dealer_hand.add_card(deck.deal_one())

        take_bet(chips)
        show_some(player_hand, dealer_hand)

        while True:
            move = input("Would you like to Hit or Stand? (h/s): ").lower()
            if move == 'h':
                hit(deck, player_hand)
                show_some(player_hand, dealer_hand)
                if player_hand.value > 21:
                    player_busts(chips)
                    break
            elif move == 's':
                print("Player stands. Dealer is playing...")
                break
            else:
                print("Invalid input. Enter 'h' or 's'.")

        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                dealer_busts(chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(chips)
            else:
                push()

        print(f"\nPlayer's total chips are now: ${chips.total}")

        again = input("Would you like to play another hand? (y/n): ").lower()
        if again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    play_game()
