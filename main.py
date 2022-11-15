import random
import json
import pprint

from deck import Deck

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

## New game.

iterator = 0
sim_results = []

while iterator < 100:
    iterator += 1
    print(f"Starting simulation #{iterator}.")
    deck.new_hand()
    deck.play_turn()
    deck.play_turn()
    deck.play_turn()
    deck.play_turn()
    deck.play_turn()
    deck.play_turn()
    deck.play_turn()
    deck.play_turn()

    sim_results.append(deck.trigger_count)

print(f"The average damage dealt by dragons in X turns is {sum(sim_results)/len(sim_results):.2f}.")
print(f"The % of games that dealt more than 20 damage is {len([i for i in sim_results if i >= 20.0])/len(sim_results):.2f}")
