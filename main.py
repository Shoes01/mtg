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

while iterator < 1000:
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

print(f"The average damage dealt by dragons in 10 turns is {sum(sim_results)/len(sim_results)}.")


# Old sim.

"""
sim_it = 0
sim_results = []

while sim_it < 0:
    sim_it += 1
    success = False

    deck.new_hand()

    relevant_info = {
        "types": [],
        "convertedManaCost": [],
        "name": [],
    }

    # Store relevant info in a dict.
    for card in deck.hand:
        for key in relevant_info.keys():
            relevant_info[key].append(card[key])
        

    #pp.pprint(relevant_info)

    # Successful opening hand: 
    ## 2-4 lands, 1 CMC, 2 CMC, 3or4 CMC.    
    if (relevant_info["types"].count(["Land",]) >= 2 and relevant_info["types"].count(["Land",]) <= 4) \
        and ("Dragon Tempest" in relevant_info["name"]) \
        and (relevant_info["convertedManaCost"].count(3.0) >= 1 or relevant_info["convertedManaCost"].count(4.0) >= 1):
        success = True
    
    sim_results.append(success)

#success_rate = sum(sim_results)/len(sim_results)

#print(f"The success rate is {success_rate * 100}%.")

"""