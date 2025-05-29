from Shoe import Shoe
from User import User


class BlackJack():
    def __init__(self, numDecks = 1):
        self.numDecks = numDecks
        self.shoe = Shoe(numDecks)
    

    def game(self):
        numDecks = int(input("How many decks do you want to play with? (1 to 8) "))
        if numDecks < 1 or numDecks > 8:
            raise ValueError("You can only play with 1 to 8 decks")
        
        money = int(input("How much money do you want to start with? (100 to 10000) "))

        while True:
            hitOnSoft = input("Do you want the dealer to hit on a soft 17? (y/n)").strip().lower()
            if hitOnSoft in ("n", "y"):
                if hitOnSoft == "y":
                    hitOnSoft = True
                else:
                    hitOnSoft = False
                break
            print("Invalid input. Please enter 'hard' or 'soft'.")


        while (True):
            while (len(self.shoe.cards) > 20):  # Change the 20 to an int that changes based on parameters

                numHands = int(input("How many hands do you want to play? (1 to 4) "))
                if numHands < 1 or numHands > 4:
                    raise ValueError("You can only play with 1 to 4 hands")

                self.user = User(numHands, money)

                # handValues = {i: [] for i in range(numHands + 1)} 
                
                for i in range(numHands):
                    bet = int(input(f"How much do you want to bet for hand {i + 1}? "))
                    self.user.bet(bet, i)
                    # money -= bet
                
                dealersCards = {numHands : []}
                self.dealCards(numHands, dealersCards)
                dealerHandValue = self.valueHand(dealersCards[numHands])

                for i in range(numHands):
                    self.playHand(i)

                print("Dealer's turn...")
                self.dealerLogic(dealersCards[numHands], hitOnSoft)
                
                dealerHandValue = self.valueHand(dealersCards[numHands])
                for i in range(numHands):
                    handValue = self.valueHand(self.user.hands[i])

                    if handValue > 21:
                        # player busts
                        self.user.outcome("bust", self.user.bets[i])
                    elif dealerHandValue > 21:
                        # player wins
                        self.user.outcome("win", self.user.bets[i])
                    elif handValue > dealerHandValue:
                        # player wins
                        self.user.outcome("win", self.user.bets[i])
                    elif handValue == dealerHandValue:
                        # push 
                        self.user.outcome("push", self.user.bets[i])
                    elif handValue < dealerHandValue:
                        # player loses because dealer has higher hand
                        self.user.outcome("lose", self.user.bets[i])
                        

                

                print("New round starting...")

            break
                

    def playHand(self, handIndex):
        numSplits = 0
        while True:
            action = input(f"Hand {handIndex + 1}: Do you want to hit, stand, double down, or split? ").lower()
            if action == "hit":
                self.hit(handIndex)
                handValue = self.valueHand(self.user.hands[handIndex])
                if handValue > 21:
                    print(f"Hand {handIndex + 1} busts!")
                    break
            elif action == "stand":
                print(f"Hand {handIndex + 1} stands.")
                break
            elif action == "double down":
                self.doubleDown(handIndex)
                handValue = self.valueHand(self.user.hands[handIndex])
                if handValue > 21:
                    print(f"Hand {handIndex + 1} busts!")
                    break
            elif action == "split":
                numSplits += 1
                if numSplits > 3:
                    print("You can only split up to 3 times.")
                    break
                self.split(handIndex)
                print(f"Hand {handIndex + 1} split into two hands.")
                self.playHand(handIndex)
                self.playHand(int(handIndex) + 0.1)  # Play the new hand created by the split
                break
            else:
                print("Invalid action. Please choose hit, stand, double down, or split.")


    def dealerLogic(self, dealersCards, hitOnSoft):
        value = self.valueHand(dealersCards)

        # debug output
        print(f"Current shoe: {self.shoe.cards}")

        if hitOnSoft == True:

            # debug output
            print(f"Dealer hits on soft 17.")


            while value < 17 or (value == 17 and 'A' in [card[0] for card in dealersCards]):

                # debug output
                print(f"dealt card: {self.shoe.cards[0]}")

                dealersCards.append(self.shoe.dealOneCard())
                value = self.valueHand(dealersCards)
        else:

            # debug output
            print(f"Dealer does not hit on soft 17.")

            while value < 17:

                # debug output
                print(f"dealt card: {self.shoe.cards[0]}")

                dealersCards.append(self.shoe.dealOneCard())
                value = self.valueHand(dealersCards)

        
        print(f"Dealer's final hand: {dealersCards} | Hand value: {self.valueHand(dealersCards)}")

    def hit(self, handIndex):
        card = self.shoe.dealOneCard()
        self.user.hands[handIndex].append(card)
        

    def doubleDown(self, handIndex):
        card = self.shoe.dealOneCard()
        self.user.hands[handIndex].append(card)
        self.user.bet(self.user.bets[handIndex], handIndex)
        
    def split(self, handIndex):
        assert len(self.user.hands[handIndex]) == 2, "You can only split if you have two cards"  

        tempCard = self.user.hands[handIndex][1]
        self.user.hands[handIndex].pop(1)
        self.user.hands[int(handIndex)+0.1] = [tempCard]

        self.user.bets[int(handIndex)+0.1] = self.user.bets[handIndex]
        self.user.hands[handIndex].append(self.shoe.dealOneCard())
        self.user.hands[int(handIndex)+0.1].append(self.shoe.dealOneCard())

        self.user.hands = { k: self.user.hands[k] for k in sorted(self.user.hands) }
        self.user.bets = { k: self.user.bets[k] for k in sorted(self.user.bets) }

    def valueHand(self, hand):
        cardValue = 0
        handValue = 0

        for i in hand:
            if i[0] in ['J', 'Q', 'K']:
                cardValue = 10
            elif i[0] == 'A':
                cardValue = 11 if cardValue + 11 <= 21 else 1
            elif i[0] == '1' and i[1] == '0':
                cardValue = 10
            else:
                cardValue = int(i[0])
            
            handValue += cardValue
        
        for i in hand:
            if i[0] == 'A' and handValue > 21:
                handValue -= 10

        print (f"Cards: {hand[0]}, {hand[1]} | Hand value: {handValue}")
        return handValue
        
    
    def dealCards(self, numHands, dealersCards):
               
        for i in range(2):
            for j in range(numHands+1):
                    card = self.shoe.dealOneCard()
                    if j != numHands:
                        self.user.hands[j].append(card)
                    else:
                        dealersCards[j].append(card)

        print("Your Hands:")
        for i in range(numHands):
            print(f"    Hand {i + 1}: {self.user.hands[i]}")
        
        print("Dealer Hand: " + dealersCards[numHands][0] + ", " + dealersCards[numHands][1] + "(DCard)")
    
            
game1 = BlackJack()
game1.game()


        

