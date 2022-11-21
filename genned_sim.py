import json
import pprint

from deck_v2 import Deck

import pilot

pp = pprint.PrettyPrinter(indent=4)


# LOAD THE CARD DATABASE.


file = open("data/Deck.json", "r", encoding="utf8")
CARDS = json.load(file)


# LOAD THE CARDS.


deck_txt = open("data/genned_decklist.txt", "r", newline='')
cards_dict = {}

for line in deck_txt.readlines():

    pieces = line.split("'")
    for piece in pieces:
        if piece == "[" or piece == ", " or piece == "]":
            continue
        if piece in cards_dict:
            cards_dict[piece] += 1
        else:
            cards_dict[piece] = 1
    



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

deck.verbose = False

sim_starting_hands = []
sim_winning_battlefields = []
best_count = 0

#print(f"The deck's library is {deck.get_human_names(deck.library)} cards.")

while sim_iter < 1000:
    sim_iter += 1
    print("\n")
    deck.new_hand()
    hand = []
    for card in deck.hand:
        hand.append(card['name'])
    sim_starting_hands.append(hand)
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

    if deck.trigger_count < 20:
        print("Hand failed.")
        sim_starting_hands.pop()
    else:
        battlefield = []
        for card in deck.battlefield:
            battlefield.append(card['name'])
        sim_winning_battlefields.append(battlefield)
    

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
print("Starting hands that results in >20 triggers.")
for hand in sim_starting_hands:
    print(hand)
print("Battlefields that result in >20 triggers.")
for field in sim_winning_battlefields:
    print(field)
print("\nSimulation complete.")

