
class User:
    def __init__(self, numHands = 1, money = 1000):
        self.numHands = numHands
        self.money = money
        self.hands = []
    
    def bet(self, bet):
        if bet > self.money:
            raise ValueError("You don't have enough money to make this bet")
        self.money -= bet
        return bet


