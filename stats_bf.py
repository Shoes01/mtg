import pprint

pp = pprint.PrettyPrinter(indent=4)

file = open("data/genned_bfs.txt", "r", newline='')
battlefields = {}
line_count = 0
for line in file.readlines():
    line_count += 1
    cards = []
    # turn string array into proper array
    pieces = line.split("'")
    for piece in pieces:
        if piece == "[" or piece == ", " or piece == "]" or "]" in piece or "\\" in piece or piece == "":
            continue
        cards.append(piece)
    battlefields[line_count] = cards

# calculate the most popular cards in each position of the array.
stats = {}

for key, battlefield in battlefields.items():
    # battlefield[key] is an array of cards, in order of appearance.
    for card_pos in range(len(battlefield)):
        if card_pos in stats:
            stats[card_pos].append(battlefield[card_pos])
        else:
            stats[card_pos] = [battlefield[card_pos],]





# calculate the percentage of times each card appears in each position.
for key, battlefield in stats.items():
    # battlefield[key] is an array of cards, in order of appearance.
    stats[key] = {}
    for card in battlefield:
        if card in stats[key]:
            stats[key][card] += 1
        else:
            stats[key][card] = 1

most_played = {}
count = 0
for card_pos, cards in stats.items():
    highest_count = 0
    for card, quantity in cards.items():
        if quantity > highest_count:
            highest_count = quantity
            most_played[card_pos] = card
    
pp.pprint(stats)
pp.pprint(most_played)
