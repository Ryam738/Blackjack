import random
import os
import sys





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
dealer_ace_unshrinked = 0
player_ace_unshrinked = 0

def clear_screen():
    # 'nt' represents Windows, everything else is POSIX (Linux/macOS)
    os.system("cls" if os.name == "nt" else "clear")
    print(blackjack_art)

def deal_card(hand: list[str], amount: int, bust: bool, ace_unshrinked: int):
    global deck_of_cards
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
    return amount, bust, ace_unshrinked

def deal_card_dealer():
    global dealer_amount
    global deck_of_cards
    global dealer_ace_unshrinked
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
            dealer_ace_unshrinked += 1
        else:
            dealer_amount += int(card)
    if dealer_amount > 21 and dealer_ace_unshrinked > 0:
        dealer_amount -= 10
        dealer_ace_unshrinked -= 1

def screen(bool: bool):
    clear_screen()
    if bool == True:
        print(f"Dealer's hand: ['??', {dealer_hand[0]}]")
    else:
        print(f"Dealer's hand: {dealer_hand} ({dealer_amount})")
    print(f"Player's hand: {player_hand} ({player_amount})")
    print(" ")

def deal_card_player():
    global player_amount
    global deck_of_cards
    global player_ace_unshrinked
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
            player_ace_unshrinked += 1
        else:
            player_amount += int(card)
        if player_amount > 21 and player_ace_unshrinked > 0:
            player_amount -= 10
            player_ace_unshrinked -= 1

def hit():
    global player_amount, player_bust, player_ace_unshrinked
    player_amount, player_bust, player_ace_unshrinked = deal_card(
        player_hand, player_amount, player_bust, player_ace_unshrinked
    )

def stand():
    global dealer_amount
    global deck_of_cards
    global dealer_hand
    global dealer_bust
    global dealer_ace_unshrinked
    while dealer_amount < 17:
        dealer_amount, dealer_bust, dealer_ace_unshrinked = deal_card(dealer_hand, dealer_amount, dealer_bust, dealer_ace_unshrinked)

def outcome():
    if player_bust == True:
        return("Bust! You lose.")
    else:
        stand()
        if dealer_bust == True:
            return "Dealer busts! You win."
        elif dealer_amount > player_amount:
            return "Dealer wins!"
        elif dealer_amount == player_amount:
            return "Push."
        else:
            return "You win!"

def main():
    while True:
        clear_screen()
        print(" ")
        print("Welcome to Blackjack!")
        print(" ")
        command = input("Press 'Enter' to start a new game or 'quit' to exit: ")
        if command == "":
            while True:  # outer loop
                global dealer_hand, player_hand, dealer_ace_unshrinked, player_ace_unshrinked
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
                dealer_ace_unshrinked = 0
                player_ace_unshrinked = 0
                deal_card_dealer()
                deal_card_player()
                if player_amount == 21:
                    screen(False)
                    print("Blackjack! You win.")
                if dealer_amount == 21:
                    screen(False)
                    print("Dealer got Blackjack! Dealer wins.")
                screen(True)
                while True: #inner loop
                    if len(player_hand) == 2 and player_amount == 21 or len(dealer_hand) == 2 and dealer_amount == 21:
                        screen(False)
                        if player_amount == 21:
                            if dealer_amount == 21:
                                print("Push!")
                            else:
                                print("You got Blackjack! You win.")
                        else:
                            print("Dealer got Blackjack! Dealer wins.")
                        break
                    print(" ")
                    action = input("Type 'hit' to draw a card or 'stand' to stand: ")
                    if action == "hit":
                        hit()
                        if player_bust == True:
                            result = outcome()
                            screen(False)
                            print(result)
                            break
                        screen(True)
                    elif action == "stand":
                        result = outcome()
                        screen(False)
                        print(result)
                        break
                    elif action == "quit":
                        os.system("cls" if os.name == "nt" else "clear")
                        sys.exit()
                    else:
                        print("Invalid action. Please try again.")
                        print(" ")
                        continue #end of inner loop
                print(" ")
                play_again = input("Press 'Enter' to play again or 'quit' to quit: ")
                if play_again == "quit":
                    os.system("cls" if os.name == "nt" else "clear")
                    sys.exit()
                else:
                    continue


        elif command == "quit":
            os.system("cls" if os.name == "nt" else "clear")
            break
        else:
            print("Invalid command. Please try again.")
            print(" ")
            continue

main()
