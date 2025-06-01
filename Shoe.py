import random
from count import hiLo

# This is a simple shoe class for blackjack
# It will create a shoe with a given number of decks
class Shoe:
    def __init__(self, numDecks = 1):
        self.suits = ["c", "d", "s", "h"]
        self.values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        self.numDecks = numDecks
        self.cards = self.createShoe()
        self.hiLo = hiLo(self.numDecks)

    def createShoe(self):

        cards = []
        suits = ["c", "d", "s", "h"]
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        # Create a shoe
        for i in range(self.numDecks):
            for value in self.values:
                for suit in self.suits:
                    card = str(value) + str(suit)
                    cards.append(card)

        cards = random.sample(cards, len(cards))

        # Checks if the shoe is the right size
        assert len(cards) == 52 * self.numDecks, "The deck is not the right size"
        return cards
    
    def dealOneCard(self):
        dealtCard = self.cards.pop() 
        self.hiLo.counts(dealtCard)
        return dealtCard