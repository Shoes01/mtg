import random
import json
import pprint

from deck import Deck

pp = pprint.PrettyPrinter(indent=4)


# LOAD THE CARD DATABASE.


file = open("data/Deck.json", "r")
CARDS = json.load(file)


# LOAD THE DECK.


deck_txt = open("data/deck.txt", "r", newline='')
cards_dict = {}

for line in deck_txt.readlines():
    line.rstrip()
    pieces = line.split()

    value = int(pieces[0])
    key = ""
    for n in range(1, len(pieces)):
        key += pieces[n] + " "
    
    cards_dict[key.rstrip()] = value
    

# ASSEMBLE MTG DECK.


cards = []

for key, value in cards_dict.items():
    cards.extend([key,] * value)

deck = Deck(cards)


# DRAW 7 CARDS


deck.new_hand()
print(f"Hand is: {deck.hand}.")


# Analyse the hand.


types = []
for card in deck.hand:
    types.extend(CARDS[card]["types"])

print(types)

# Fun sim.

sim_it = 0
sim_results = []
while sim_it < 1000:
    sim_it += 1

    deck.new_hand()

    cmcs = []
    for card in deck.hand:
        cmcs.append(CARDS[card]["convertedManaCost"])

    one_drop_count = cmcs.count(1.0)
    #two_drop_count = cmcs.count(2.0)

    sim_results.append(one_drop_count)

print(f"The average number of 1+2 drop cards in hand is: {sum(sim_results)/len(sim_results)}.")

