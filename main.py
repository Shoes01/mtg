import json
import pprint

from deck_v2 import Deck

import pilot

pp = pprint.PrettyPrinter(indent=4)


# LOAD THE CARD DATABASE.


file = open("data/Deck.json", "r", encoding="utf8")
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
    cards.extend([CARDS[key],] * value)

deck = Deck(cards)


# SIMULATOR.

print("Begin simulation.\n")

deck.new_hand()
pilot.play(deck)
deck.next_turn()
pilot.play(deck)
deck.next_turn()
pilot.play(deck)
deck.next_turn()
pilot.play(deck)
deck.next_turn()
pilot.play(deck)
deck.next_turn()
pilot.play(deck)
deck.next_turn()
pilot.play(deck)
deck.next_turn()
pilot.play(deck)

print("\nSimulation complete.")