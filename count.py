# This is the hi-lo count of the shoe being played
# It will constantly update the running and true count of the shoe
class hiLo():
    def __init__(self, shoeSize): 
        self.count = 0 
        self.trueCount = 0
        # true count is based on the fractional number of decks left.
        self.numCards = 52 * shoeSize # shoe size will be global variable defined in the input

    def counts(self, card):
        # Running count logic
        value = card[0]
        if value in ['2', '3', '4', '5', '6']:
            self.count += 1
        elif value in ['7', '8', '9']:
            pass
        else:
            self.count -= 1

        # True count logic
        self.numCards -= 1
        decksRemaining = self.numCards / 52
        if decksRemaining >= 1:
            self.trueCount = self.count / decksRemaining
        elif decksRemaining < 1 and decksRemaining > 0:
            self.trueCount = self.count
        else:
            self.trueCount = self.count
