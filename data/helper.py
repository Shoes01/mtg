import json

# Reduce the JSON db to _only_ the cards in the deck.

## PREPARE DECK

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

CARDS = list(cards_dict.keys())

# PREPARE ALL CARDS

file_path = "data/AtomicCards.json"
file = open(file_path, "r", encoding="utf8")
json_file = json.load(file)

ALL_CARDS = json_file["data"]

# WRITE NEW JSON

with open("data/Deck.json", "w") as f:
    full_list = {}
    for CARD in CARDS:
        #full_list.append({CARD: ALL_CARDS[CARD][0]})
        full_list[CARD] = ALL_CARDS[CARD][0]
    
    json.dump(full_list, f, ensure_ascii=True, indent=4)

## PREPARE TOKENS

tokens_txt = open("data/tokens.txt", "r", newline='')
tokens_array = []

for line in tokens_txt.readlines():
    tokens_array.append(line)

TOKENS = tokens_array

## PREPARE ALL TOKENS

file_path = "data/DOM.json"
file = open(file_path, "r", encoding="utf8")
json_file = json.load(file)

ALL_TOKENS = json_file["data"]['tokens']

# WRITE NEW JSON

with open("data/Tokens.json", "w") as f:
    full_list = {}
    for TOKEN in TOKENS:
        # TOKEN is the name.
        for all_token in ALL_TOKENS:
            if all_token['name'] == TOKEN:
                full_list[TOKEN] = all_token
    
    json.dump(full_list, f, ensure_ascii=True, indent=4)


print("Done.")