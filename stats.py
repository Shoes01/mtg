import pprint

pp = pprint.PrettyPrinter(indent=4)

file = open("data/genned_hands.txt", "r", newline='')
cards_dict = {}
lines = 0
for line in file.readlines():
    lines += 1
    pieces = line.split("'")
    for piece in pieces:
        if piece == "[" or piece == ", " or piece == "]" or "]" in piece:
            continue
        if piece in cards_dict:
            cards_dict[piece] += 1
        else:
            cards_dict[piece] = 1

stats = {}
for key in cards_dict.keys():
    stats[key] = cards_dict[key] / lines

sum = 0
for value in stats.values():
    sum += value

print(sum)
sorted_cards={}
#sorted_cards = {v: k for k, v in sorted(stats.items(), key=lambda item: item[1])}
for key, value in sorted(stats.items()):
    value = int(100*value) / 100.0
    if value in sorted_cards:
        sorted_cards[value].append(key)
    else:
        sorted_cards[value] = [key,]
pp.pprint(sorted_cards)