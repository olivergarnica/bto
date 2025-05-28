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
        
        numHands = int(input("How many hands do you want to play? (1 to 4) "))
        if numHands < 1 or numHands > 4:
            raise ValueError("You can only play with 1 to 4 hands")

        self.user = User(numHands, money=1000)
        
        done = False


        while (done == False):
            while (len(self.shoe.cards) > 20):  # Change the 20 to an int that changes based on parameters
                handValues = {i: [] for i in range(numHands + 1)} 
                for i in range(numHands):
                    bet = int(input(f"How much do you want to bet for hand {i + 1}? "))
                    self.user.bet(bet, i)
                
                dealersCards = {numHands : []}
                self.dealCards(numHands, dealersCards)
                dealerHandValue = self.valueHand(dealersCards[numHands])

                for i in range(numHands):
                    handValue = self.valueHand(self.user.hands[i])
                    handValues[i] = handValue
    

    
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
                card = self.shoe.dealOneCard()
                self.user.hands[handIndex].append(card)
                print(f"New card dealt to hand {handIndex + 1}: {card}")
                print(f"Hand {handIndex + 1} split into two hands.")
                self.playHand(handIndex)
                self.playHand(int(handIndex) + 0.1)  # Play the new hand created by the split
                break
            else:
                print("Invalid action. Please choose hit, stand, double down, or split.")


    def hit(self, handIndex):
        card = self.shoe.dealOneCard()
        self.user.hands[handIndex].append(card)
        

    def doubleDown(self, handIndex):
        card = self.shoe.dealOneCard()
        self.user.hands[handIndex].append(card)
        bet = self.user.bet(self.user.bets[handIndex], handIndex)
        
    def split(self, handIndex):
        assert len(self.user.hands[handIndex]) == 2, "You can only split if you have two cards"

        self.user.hands = sorted(self.user.hands())
        tempHand = self.user.hands[handIndex]
        self.user.hands[handIndex] = [tempHand[0]]
        self.user.hands[int(handIndex)+0.1] = [tempHand[1]]
        self.user.bets[int(handIndex)+0.1] = self.user.bets[handIndex]
        

    def valueHand(self, hand):
        cardValue = 0

        for i in hand:
            if i[0] in ['J', 'Q', 'K']:
                cardValue = 10
            elif i[0] == 'A':
                cardValue = 11 if cardValue + 11 <= 21 else 1
            else:
                cardValue = int(i[0])
            
            handValue += cardValue
        
        for i in hand:
            if i[0] == 'A' and handValue > 21:
                handValue -= 10

        print (f"Hand value: {handValue}")
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
        
        print("Dealer Hand: " + dealersCards[numHands][0] + " DCard")
    
            
game1 = BlackJack()
game1.game()


        

