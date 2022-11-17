import json
import pprint

from deck_v2 import Deck

import pilot

pp = pprint.PrettyPrinter(indent=4)


# LOAD THE CARD DATABASE.


file = open("data/Deck.json", "r", encoding="utf8")
CARDS = json.load(file)


# LOAD THE CARDS.


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


# LOAD THE TOKENS DATABASE


file = open("data/Tokens.json", "r", encoding="utf8")
TOKENS = json.load(file)


# LOAD THE TOKENS

tokens_txt = open("data/tokens.txt", "r", newline='')
tokens_array = []

for line in tokens_txt.read().splitlines():
    tokens_array.append(line)

# ASSEMBLE MTG DECK.

cards = []
tokens = []

for key, value in cards_dict.items():
    # key: card name
    # value: number in deck
    cards.extend([CARDS[key],] * value)

for item in tokens_array:
    tokens.append(TOKENS[item])

deck = Deck(cards, tokens)


# SIMULATOR.


print("Begin simulation.\n")

sim_results = []
sim_iter = 0

deck.verbose = True

while sim_iter < 1:
    sim_iter += 1
    print("\n")
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
    deck.next_turn()
    pilot.play(deck)
    deck.next_turn()
    pilot.play(deck)

    sim_results.append(deck.trigger_count)

file = open("file.txt", "w")
for line in deck.log:
    file.write(line)

print(f"\nThe average number of triggers was {sum(sim_results)/len(sim_results)}.")
print(f"The most triggers in a game was {max(sim_results)}. The least was {min(sim_results)}.")
print(f"The number of 0-trigger games is {sim_results.count(0)}.")
lethal_count = 0
for result in sim_results:
    if result >= 20:
        lethal_count += 1
print(f"The number of 20-trigger games is {lethal_count}.")
print("\nSimulation complete.")