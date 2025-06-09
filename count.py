# This is the hi-lo count of the shoe being played
# It will constantly update the running and true count of the shoe
class hiLo:
    def __init__(self, shoeSize):
        self.count = 0
        self.trueCount = 0
        self.numCards = 52 * shoeSize
        self.shoeSize = shoeSize

    def counts(self, card):
        v = card[0]
        if v in ('2','3','4','5','6'):
            self.count += 1
        elif v in ('7','8','9'):
            pass
        else:
            self.count -= 1

        self.numCards -= 1

        decksRemaining = self.numCards / 52
        if decksRemaining > 0.5:
            raw = self.count / decksRemaining
            if raw > 0:
                self.trueCount = int(raw + 0.5)
            else:
                self.trueCount = int(raw - 0.5)
        else:
            # Near end of shoe, just use running count
            self.trueCount = self.count

