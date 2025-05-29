class User:
    def __init__(self, numHands = 1, money = 1000):
        self.numHands = numHands
        self.money = money
        self.hands = {i: [] for i in range(numHands)}
        self.bets = {i: 0 for i in range(numHands)}
        self.status = 'active'
    
    def bet(self, bet, handIndex=0):
        if handIndex < 0 or handIndex >= self.numHands:
            raise IndexError("Invalid hand index")
        
        if bet > self.money:
            raise ValueError("You don't have enough money to make this bet")
        self.money -= bet
        self.bets[handIndex] += bet
        return bet
    
    def outcome(self, outcome, bet):
        if outcome == "win":
            self.money += bet * 2
        elif outcome == "push":
            self.money += bet
        elif outcome == "blackjack":
            self.money += bet * (6 / 5)
        elif outcome == "bust":
            self.money -= bet
        elif outcome == "lose":
            self.money -= bet
        
        