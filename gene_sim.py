import json
import pprint
import time

from deck_v2 import Deck

import pilot
import genetic

pp = pprint.PrettyPrinter(indent=4)


# LOAD THE CARD DATABASE.


file = open("data/Deck.json", "r", encoding="utf8")
CARDS = json.load(file)


# LOAD THE CARDS.


deck_txt = open("data/gen_deck.txt", "r", newline='')
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

tokens_txt = open("data/tokens.txt", "r", newline='')
tokens_array = []

for line in tokens_txt.read().splitlines():
    tokens_array.append(line)

tokens = []
for item in tokens_array:
    tokens.append(TOKENS[item])

# ASSEMBLE MTG DECK.

cards = []

deck_set = []

for key, value in cards_dict.items():
    # key: card name
    # value: number in deck
    cards.extend([CARDS[key],] * value)
    if CARDS[key] not in deck_set:
        deck_set.append(CARDS[key])

deck = Deck(cards, tokens)

# SIMULATOR.


def display_function(candidate_deck):
    print(f"Score: {candidate_deck.Fitness}")
    print(f"Deck: {deck.get_human_names(candidate_deck.Genes)}")


def fitness_function(candidate_deck):
    # Run the deck 6 turns x 100 games.
    # Average the results.
    # Return the average.
    trigger_counts = []
    simulation_count = 0
    while simulation_count < 400:
        simulation_count += 1
        turn_count = 0
        candidate_deck.new_hand()
        pilot.play(candidate_deck)
        while turn_count < 6:
            turn_count += 1
            candidate_deck.next_turn()
            pilot.play(candidate_deck)
        trigger_counts.append(candidate_deck.trigger_count)
    average_triggers = sum(trigger_counts) / len(trigger_counts)
    dragons, tempest= 0, 0
    for card in candidate_deck._deck_list:
        if "Dragon" in card['subtypes']: 
            dragons += 1
        if "Dragon Tempest" in card['name'] or "Scourge of Valkas" in card['name']: 
            tempest += 1

    score = dragons + tempest * 2 + average_triggers * 100
    #print(f"This deck's score is {dragons} + {tempest}x2 + {average_triggers}x10 = {score}.")
    return score

print("Being simulation.")

best = genetic.get_best(fitness_function,60,100000.0,deck_set,tokens,display_function)

print(f"Best deck: {deck.get_human_names(best.Genes)}")

