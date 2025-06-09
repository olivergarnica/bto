class User:
    def __init__(self, numHands = 1, money = 1000):
        self.numHands = numHands
        self.money = money
        self.hands = {i: Hand(i) for i in range(numHands)}
        self.cookies = 0

    def bet(self, amount, handIndex=0):
        if handIndex < 0 or handIndex >= self.numHands:
            raise IndexError("Invalid hand index")
        
        if amount > self.money:
            raise ValueError("You don't have enough money to make this bet")
            
        self.hands[handIndex].bet = amount 
        return amount
    
    def outcome(self, outcome, handIndex):
        h = self.hands[handIndex]
        b = h.bet
        
        if outcome == "win":
            self.money += b
            print(f"Hand {handIndex + 1} wins! Your new balance is {self.money}.")
        elif outcome == "push":
            # nothig happens, money stays the same
            print(f"Hand {handIndex + 1} pushes! Your balance remains {self.money}.")
        elif outcome == "blackjack":
            self.money += b * (3 / 2)  # 1.5 times the bet, assuming blackjack pays 3:2
            print(f"Hand {handIndex + 1} is a blackjack! Your new balance is {self.money}.")
        elif outcome == "bust":
            self.money -= b
            print(f"Hand {handIndex + 1} busts! Your new balance is {self.money}.")
        elif outcome == "lose":
            self.money -= b

            print(f"Hand {handIndex + 1} loses! Your new balance is {self.money}.")

class Hand():
    def __init__(self, index, initialBet=0):
        self.index = index
        self.cards = []
        self.bet = initialBet 
        self.status = 'active'   
        self.split_count = 0 

    def __str__(self):
        return f"cards={self.cards}, bet=${self.bet}"