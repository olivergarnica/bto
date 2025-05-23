import random

# This is a simple shoe class for blackjack
# It will create a shoe with a given number of decks
def shoe(numDecks = 1):
    cards = []
    suits = ["c", "d", "s", "h"]
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']

    # Create a shoe
    for i in range(numDecks):
        for value in  values:
            for suit in suits:
                card = str(value) + str(suit)
                cards.append(card)

    cards = random.sample(cards, len(cards))

    # Checks if the shoe is the right size
    assert len(cards) == 52 * numDecks, "The deck is not the right size"

    return cards

print(shoe(1))