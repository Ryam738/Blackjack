import random
import os






blackjack_art = r"""
/$$$$$$$$  /$$                     /$$                               /$$
| $$__  $$| $$                    | $$                              | $$
| $$  \ $$| $$  /$$$$$$   /$$$$$$$| $$   /$$ /$$  /$$$$$$   /$$$$$$$| $$   /$$
| $$$$$$$ | $$ |____  $$ /$$_____/| $$  /$$/|__/ |____  $$ /$$_____/| $$  /$$/
| $$__  $$| $$  /$$$$$$$| $$      | $$$$$$/  /$$  /$$$$$$$| $$      | $$$$$$/
| $$  \ $$| $$ /$$__  $$| $$      | $$_  $$ | $$ /$$__  $$| $$      | $$_  $$
| $$$$$$$/| $$|  $$$$$$$|  $$$$$$$| $$ \  $$| $$|  $$$$$$$|  $$$$$$$| $$ \  $$
|_______/ |__/ \_______/ \_______/|__/  \__/| $$ \_______/ \_______/|__/  \__/
                                      /$$  | $$
                                     |  $$$$$$/
                                      \______/
"""


playing_cards = [
    "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A",
    "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A",
    "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A",
    "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A",
]
deck_of_cards = playing_cards.copy()

dealer_hand: list[str] = []
player_hand: list[str] = []
player_amount = 0
dealer_amount = 0
dealer_bust = False
player_bust = False
ace_unshrinked = 0

def clear_screen():
    # 'nt' represents Windows, everything else is POSIX (Linux/macOS)
    os.system("cls" if os.name == "nt" else "clear")
    print(blackjack_art)

def deal_card(hand: list[str], amount: int, bust: bool) -> tuple[int, bool]:
    global deck_of_cards
    global ace_unshrinked
    if len(deck_of_cards) <= 5:
        deck_of_cards = playing_cards.copy()
    card = random.choice(deck_of_cards)
    hand.append(card)
    deck_of_cards.remove(card)
    if card == "J" or card == "Q" or card == "K":
        amount += 10
    elif card == "A":
        amount += 11
        ace_unshrinked += 1
    else:
        amount += int(card)
    if amount > 21 and ace_unshrinked > 0:
        amount -= 10
        ace_unshrinked -= 1
    if amount > 21:
        bust = True
    return amount, bust

def deal_card_dealer():
    global dealer_amount
    global deck_of_cards
    global ace_unshrinked
    if len(deck_of_cards) <= 5:
        deck_of_cards = playing_cards.copy()
    for i in range(2):
        card = random.choice(deck_of_cards)
        dealer_hand.append(card)
        deck_of_cards.remove(card)
        if card == "J" or card == "Q" or card == "K":
            dealer_amount += 10
        elif card == "A":
            dealer_amount += 11
            ace_unshrinked += 1
        else:
            dealer_amount += int(card)

def deal_card_player():
    global player_amount
    global deck_of_cards
    global ace_unshrinked
    if len(deck_of_cards) <= 5:
        deck_of_cards = playing_cards.copy()
    for i in range(2):
        card = random.choice(deck_of_cards)
        player_hand.append(card)
        deck_of_cards.remove(card)
        if card == "J" or card == "Q" or card == "K":
            player_amount += 10
        elif card == "A":
            player_amount += 11
            ace_unshrinked += 1
        else:
            player_amount += int(card)

def hit():
    global player_amount, player_bust
    player_amount, player_bust = deal_card(player_hand, player_amount, player_bust)

def stand():
    global dealer_amount
    global deck_of_cards
    global dealer_hand
    global dealer_bust
    while dealer_amount < 17:
        dealer_amount, dealer_bust = deal_card(dealer_hand, dealer_amount, dealer_bust)
    print(f"Player's hand: {player_hand} ({player_amount})")
    print(f"Dealer's hand: {dealer_hand} ({dealer_amount})")

def outcome():
    stand()
    if player_bust == True:
        print("Bust! You lose.")
    else:
        if dealer_bust == True:
            print("Dealer busts! You win.")
        elif dealer_amount > player_amount:
            print("Dealer wins!")
        elif dealer_amount == player_amount:
            print("Push.")
        else:
            print("You win!")

def main():
    while True:
        clear_screen()
        print(" ")
        print("Welcome to Blackjack!")
        print(" ")
        command = input("Press 'Enter' to start a new game or 'quit' to exit: ")
        if command == "":
            while True:
                clear_screen()
                global dealer_hand
                global player_hand
                global player_amount
                global dealer_amount
                global dealer_bust
                global player_bust
                dealer_hand = []
                player_hand = []
                player_amount = 0
                dealer_amount = 0
                dealer_bust = False
                player_bust = False
                deal_card_dealer()
                deal_card_player()
                print(" ")
                print(f"Dealer's hand: ['??', {dealer_hand[0]}]")
                print(f"Player's hand: {player_hand} ({player_amount})")
                if player_amount == 21:
                    print(" ")
                    print("Blackjack! You win.")
                    break
                if dealer_amount == 21:
                    print(" ")
                    print("Dealer got Blackjack! Dealer wins.")
                    print(f"Dealer's hand: {dealer_hand} ({dealer_amount})")
                    break

                while True:
                    action = input("Type 'hit' to draw a card or 'stand' to stand: ")
                    if action == "hit":
                        print(" ")
                        hit()
                        if player_bust == True:
                            print(" ")
                            outcome()
                            break
                        else:
                            print(f"Player's hand: {player_hand} ({player_amount})")
                    elif action == "stand":
                        print(" ")
                        outcome()
                        break
                    else:
                        print("Invalid action. Please try again.")
                        print(" ")
                        continue
                print(" ")
                play_again = input("Press 'Enter' to play again or 'quit' for main menu: ")
                if play_again == "quit":
                    break
                else:
                    continue


        elif command == "quit":
            break
        else:
            print("Invalid command. Please try again.")
            print(" ")
            continue

main()
