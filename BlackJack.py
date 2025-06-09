from Shoe import Shoe
from User import User, Hand
import random

class BlackJack():
    def __init__(self, numDecks = 1):
        self.numDecks = numDecks
        self.shoe = Shoe(numDecks)
        self.nextHandID = 0
    
    def game(self):
        # Dont change
        numDecks = int(input("How many decks do you want to play with? (1 to 8) "))
        if numDecks < 1 or numDecks > 8:
            raise ValueError("You can only play with 1 to 8 decks")
        self.shoe = Shoe(numDecks)
        
        # Dont change
        while True:
            try:
                money = int(input("How much money do you want to start with? "))
                if 10 <= money <= 10000:
                    break
                else:
                    print("Don't kid yourself of you $$$. Enter a number between 10 and 10000")
            except ValueError:
                print("Enter a valid number")

        # Dont change            
        hitOnSoft = self.gameStyle()            

        print("########BLACKJACK########")

        self.user = User(money=money)

        while (True):
            while (len(self.shoe.cards) > 32):
                number = 25
                self.countChecker(number)

                numHands = int(input("How many hands do you want to play? (1 to 4) "))
                if numHands < 1 or numHands > 4:
                    raise ValueError("You can only play with 1 to 4 hands")

                self.user.numHands = numHands                
                self.user.hands = {i: Hand(i) for i in range(numHands)}
                self.nextHandID = numHands 
                
                for i in range(numHands):
                    bet = int(input(f"How much do you want to bet for hand {i + 1}? "))
                    self.user.bet(bet, i)
                
                dealersCards = {numHands : []}
                self.dealCards(numHands, dealersCards)
                dealerHandValue = self.valueHand(dealersCards[numHands])
             

                dealerBJ = False
                # for i in range(numHands):
                for i in sorted(self.user.hands):
                    hand = self.user.hands[i]
                    playerHandVal = self.valueHand(self.user.hands[i].cards)
                    
                    # Hand and Dealer get blackjack
                    if playerHandVal == 21 and dealerHandValue == 21: 
                        print(f"Hand {i + 1} and the dealer have blackjack and push")
                        self.user.outcome("push", i)
                        hand.status = "blackjack" 
                        dealerBJ = True

                    # Hand doesn't and dealer does
                    elif playerHandVal != 21 and dealerHandValue == 21:
                        print(f"The dealer has blackjack and hand {i + 1} doesn't")
                        self.user.outcome("lose", i)
                        hand.status = "blackjack" 
                        dealerBJ = True

                    # Hand does and dealer doesn't
                    elif playerHandVal == 21 and dealerHandValue != 21:
                        print(f"Hand {i + 1} has blackjack and the dealer doesn't!")
                        self.user.outcome("blackjack", i)
                        hand.status = "blackjack"

                # Only play the game if the dealer did not get blackja
                if not dealerBJ:
                    self.playAllHands()

                    print("Dealer's turn...")
                    self.dealerLogic(dealersCards[numHands], hitOnSoft)
                    dealerHandValue = self.valueHand(dealersCards[numHands])

                    for i, hand in self.user.hands.items():
                        if hand.status in ('bust', 'blackjack'):
                            continue
                        handValue = self.valueHand(self.user.hands[i].cards)

                        if dealerHandValue > 21 or handValue > dealerHandValue:
                            self.user.outcome("win", i)
                        elif handValue == dealerHandValue:
                            self.user.outcome("push", i)
                        else:
                            self.user.outcome("lose", i)
                else:
                    pass                            
                
                if self.user.money <= 0:
                    print("OUT OF MONEY BYE BYE")
                    break
                print(f"current cash: ${self.user.money}")
                print("New round starting...\n")

            playAgain = input("Oh no! Out of cards. Do you want to play another shoe? (y/n) ").strip().lower()
            if playAgain == "n":
                print("Thanks for playing!")
                break
            elif playAgain == "y":
                self.game()
            elif playAgain != "y":
                print("Invalid input. Please enter 'y' or 'n'.")
                continue
                
    # See if i should change back the return statements to break statements
    def playHand(self, handIndex):
        hand = self.user.hands[handIndex]
        number = random.randint(1, 100)

        while True:
            action = input(f"Hand {handIndex + 1}: Do you want to hit, stand, double down, or split? ").lower()
            if action == "hit":
                self.hit(handIndex)
                handValue = self.valueHand(self.user.hands[handIndex].cards)
                if handValue > 21:
                    print(f"Hand {handIndex + 1} busts!")
                    return "bust"
            elif action == "stand":
                print(f"Hand {handIndex + 1} stands.")
                return "stand"
            elif action == "double down":
                self.doubleDown(handIndex)
                handValue = self.valueHand(self.user.hands[handIndex].cards)
                print(f"Hand {handIndex + 1} ends after double down.")
                if handValue > 21:
                    print(f"Hand {handIndex + 1} busts!")
                return "double down"
            elif action == "split":
                if hand.split_count >= 3:
                    print("You can only split up to 3 times.")
                    continue
                return "split"
            else:
                print("Invalid action. Please choose hit, stand, double down, or split.")


    def dealerLogic(self, dealersCards, hitOnSoft):
        value = self.valueHand(dealersCards)

        if hitOnSoft == True:

            while value < 17 or (value == 17 and 'A' in [card[0] for card in dealersCards]):

                dealersCards.append(self.shoe.dealOneCard())
                value = self.valueHand(dealersCards)
        else:

            while value < 17:

                dealersCards.append(self.shoe.dealOneCard())
                value = self.valueHand(dealersCards)

        
        print(f"Dealer's final hand: {dealersCards} | Hand value: {self.valueHand(dealersCards)}")

    def hit(self, handIndex):
        card = self.shoe.dealOneCard()
        self.user.hands[handIndex].cards.append(card)
        print(f"Hand: {self.user.hands[handIndex]}")
        

    def doubleDown(self, handIndex):
        card = self.shoe.dealOneCard()
        hand = self.user.hands[handIndex]
        hand.cards.append(card)
        original = hand.bet
        hand.bet += original
        print(f"Bet doubled to ${hand.bet}")
        print(f"Hand after DD: {self.user.hands[handIndex]}")
        hand.status = "done"

        return "double down"

    def split(self, handIndex):
        hand = self.user.hands[handIndex]
        
        assert len(hand.cards) == 2, "You can only split if you have two cards" 

        card1 = hand.cards[0]
        card2 = hand.cards[1]

        def getCardVal(card):
            if card[0] in ['J', 'Q', 'K'] or (card[0] == '1' and card[1] == '0'):
                return 10
            elif card[0] == 'A':
                return 11
            else:
                return int(card[0])
        
        if getCardVal(card1) != getCardVal(card2):
            print("You can only split cards with the same value!")
            return None 

        if hand.split_count >= 3:
            print("You can only split a hand up to 3 times.")
            return None
        
        hand.split_count +=1

        # Create a new hand index
        new_index = self.nextHandID
        self.nextHandID += 1

        # Create new hand from one of the original cards
        new_hand = Hand(index=new_index, initialBet=hand.bet)
        new_hand.cards.append(hand.cards.pop(1))  # Remove one card from original hand
        new_hand.split_count = hand.split_count

        # Deal one card to each hand
        hand.cards.append(self.shoe.dealOneCard())
        new_hand.cards.append(self.shoe.dealOneCard())

        # Register the new hand
        self.user.hands[new_index] = new_hand
        new_hand.status = 'active'

        print(f"Split hand {handIndex + 1} into:")
        print(f"  - Hand {handIndex + 1}: {hand.cards}")
        print(f"  - Hand {new_index + 1}: {new_hand.cards}")
        return new_index
    
    def valueHand(self, hand):
        handValue = 0
        ace_count = 0

        for card in hand:
            if card[0] in ['J', 'Q', 'K'] or (card[0] == '1' and card[1] == '0'):
                handValue += 10
            elif card[0] == 'A':
                handValue += 11
                ace_count += 1
            else:
                handValue += int(card[0])

        while handValue > 21 and ace_count:
            handValue -= 10
            ace_count -= 1

        return handValue

    def dealCards(self, numHands, dealersCards):
               
        for i in range(2):
            for j in range(numHands+1):
                    card = self.shoe.dealOneCard()
                    if j != numHands:
                        self.user.hands[j].cards.append(card)
                    else:
                        dealersCards[j].append(card)

        print("Your Hands:")
        for i in range(numHands):
            print(f"    Hand {i + 1}: {self.user.hands[i]}")
        
        print("Dealer Hand: " + dealersCards[numHands][0] + ", " + "(DCard)")
    
    def gameStyle(self):
        while True:
            choice = input("Should the dealer hit on soft 17? (y/n): ").strip().lower()
            if choice == "y":
                return True
            elif choice == "n":
                return False
            else:
                print("Invalid input. Please enter 'y' or 'n'.")


    def playAllHands(self):
        queue = list(self.user.hands.keys())
        while queue:
            idx = queue.pop(0)
            hand = self.user.hands[idx]
            print(f"Hand {idx + 1}: {hand}")
            if hand.status != "active":
                continue

            result = self.playHand(idx)

            if result == "bust":
                # Immediate outcome in the player phase:
                hand.status = "bust"
                self.user.outcome("bust", idx)

            elif result == "double down":
                # Deal one card happened inside playHand/doubleDown()
                hand.status = "done"

            elif result == "split":
                new_idx = self.split(idx)
                if new_idx is None:
                    print("Split failed, try again")
                    queue.insert(0, idx)      # replay parent 
                else:
                    queue.insert(0, idx)     # replay parent
                    queue.insert(0, new_idx) # play new hand
                

            elif result == "stand":
                hand.status = "done"


    def countChecker(self, number):
        n1 = random.randint(0, 100)
        n2 = random.randint(0, 100)
        lower, upper = sorted([n1, n2])
        runningCount = self.shoe.hiLo.count
        trueCount = self.shoe.hiLo.trueCount

        if number in range(lower, upper):
            try:
                rCount = int(input("WHAT IS THE RUNNING COUNT? "))
                if rCount != runningCount:
                    print(f"No. I thought you knew how to count. I am uber disappointed in you. I don't even know what to say...\nRunning Count: {runningCount}")
                    
                else:
                    self.user.cookies += 2
                    print(f"Good job. +2 cookies for you. Cookie Count: {self.user.cookies}")
            except ValueError:
                print("That's not even a number...")

            try:
                tCount = int(input("WHAT IS THE TRUE COUNT OR LOSE ALL COOKIES? "))
                if tCount != trueCount:
                    self.user.cookies = 0
                    print(f"*sigh*... wrong :( I am sorry...\n\ndealer = 'cookie monster'\nif dealer == 'cookie monster':\n   self.user.cookies = 0\nUser Cookies: {self.user.cookies}\n") 
                else:
                    self.user.cookies += 72
                    print(f"I am proud of you.\nYou get 1000 * 1001 cookies. Karatsuba is happy.\n   User Cookies: {self.user.cookies}\n")
            except ValueError:
                print("No cookies for bad input.")
        else:   
            print(f"\n### WArning!! know The Count. He Observes Underneath. Try Fleeing Or Run. He Is Merciless...\nUser Cookies: {self.user.cookies}\n")


            
game1 = BlackJack()
game1.game()
