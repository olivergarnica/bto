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
        # self.money -= bet
        self.bets[handIndex] += bet
        return bet
    
    def outcome(self, outcome, bet, handNum):
        if outcome == "win":
            self.money += bet
            print(f"Hand {handNum + 1} wins! Your new balance is {self.money}.")
        elif outcome == "push":
            # nothig happens, money stays the same
            print(f"Hand {handNum + 1} pushes! Your balance remains {self.money}.")
        elif outcome == "blackjack":
            self.money += bet * (3 / 2)  # 1.5 times the bet, assuming blackjack pays 3:2
            print(f"Hand {handNum + 1} is a blackjack! Your new balance is {self.money}.")
        elif outcome == "bust":
            self.money -= bet
            print(f"Hand {handNum + 1} busts! Your new balance is {self.money}.")
        elif outcome == "lose":
            self.money -= bet

            print(f"Hand {handNum} loses! Your new balance is {self.money}.")
