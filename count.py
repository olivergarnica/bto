import deal

# This is the hi-lo count of the shoe being played
# It will constantly update the running and true count of the shoe
class hiLo():
    def __init__(self, deal.card): 
        self.card = card
        self.count = 0 
        self.trueCount = 0
        # true count is based on the fractional number of decks left.
        self.numCards = 52 * shoeSize # shoe size will be global variable defined in the input

    def counts(self, card): 
        if int(card[0]) <= 6:
            self.count += 1
        
        elif int(card[0]) <= 9:
            self.count += 0

        else:
            self.count -= 1
        
        self.numCards = self.numCards - 1
        self.trueCount = self.count / (self.numCards % 52) 