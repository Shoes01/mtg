# TODO: 
# Update decklist (why was I getting JSON errors?)
# Cast triggers before dragons
# Use mana from PWs
### YAY, but need to apply the legend rule. AKA: don't cast a legend card if there is only on the battlefield already.
# Use mana from nykthos
#
# Stretch goal: Run the deck 10k times to see average TTK. Then, make a change in the deck, see if it improves.
## It would be cool to make this a genetic algo of some sort ;)

import random

class Deck:
    def __init__(self, cards):
        self._deck_list = cards     
        self.library = self._deck_list.copy()
        
        self.hand = []
        self.battlefield = []
        self.mana_pool = {
            "R": 0,
            "C": 0, # Don't need other colors...
            "Dragon": 0,
        }
        self.turn = 0
        self.trigger_count = 0


    def restock_library(self):
        self.library = self._deck_list.copy()
        random.shuffle(self.library)


    def new_hand(self):
        self.restock_library()
        self.hand.clear()
        self.battlefield.clear()
        self.trigger_count = 0
        self.turn = 0

        for _ in range(0, 7):
            self.draw()
        
        print("\n ## NEW HAND ##\n")
        print(f"Starting hand: {self.get_human_names(self.hand)}.")

        self.turn = 1

    def draw(self):
        self.hand.append(self.library.pop())
        if self.turn >= 1:
            print(f"Card drawn. Hand: {self.get_human_names(self.hand)}.")


    def cast(self, card):
        # Remove card from hand.
        # Add card to battlefield.
        self.hand.remove(card)
        self.battlefield.append(card)
        print(f">> Cast {card['name']}! <<")
        print(f"Cards on the battlefield: {self.get_human_names(self.battlefield)}.")

        # Look to see if Tempest triggers.
        if "Dragon" in card["subtypes"]:
            #print(f"The following card is triggering ETB effects: {card['name']}.")
            # Count how many dragons are in play.
            # Count how many triggers are in play.
            dragons = 0
            triggers = 0
            for permanent in self.battlefield:
                if "Dragon" in permanent["subtypes"]: 
                    dragons += 1
                    #print(f"{permanent['name']} is a dragon.")
                if "Dragon Tempest" in permanent["name"] or "Scourge of Valkas" in permanent["name"]:
                    triggers += 1
                    #print(f"{permanent['name']} is a trigger.")
            
            self.trigger_count += dragons * triggers


    def play_turn(self):
        if self.turn != 0:
            print(f"\n ## TURN {self.turn} ##\n")

        if self.turn == 0:
            self.new_hand()
        else:
            self.draw()
        self._play_land()
        self._tap_lands()
        self._cast_cards()
        self._end_turn()


    def _play_land(self):
        if self.turn < 3:
            # Only play mountains first.
            for card in self.hand:
                if "Mountain" in card["name"]:
                    self.cast(card)
                    return
            else:
                # No mountains! Try to play Nykthos.
                for card in self.hand:
                    if "Land" in card["types"]:
                        self.cast(card)
                        return
                else:
                    print("No land played!")
        else:
            for card in self.hand:
                if "Land" in card["types"]:
                    self.cast(card)
                    return
            else:
                print("No land played!")


    def _tap_lands(self):
        for card in self.battlefield:
            if "Land" in card["types"]:
                if card["name"] == "Mountain": 
                    self.mana_pool["R"] += 1
                else:
                    self.mana_pool["C"] += 1
            
            elif card["name"] == "Sarkhan, Fireblood":
                self.mana_pool["Dragon"] += 2
        
        print(f"Mana pool current has {self.mana_pool['R']} red mana and {self.mana_pool['C']} colorless mana.")
    

    def _cast_cards(self):
        casted = False
        for card in self.hand:
            # Get mana cost.
            if card["convertedManaCost"] == 0.0: continue # Skip lands.

            C_cost = 0
            R_cost = 0
            for _cost in card["manaCost"].split("{"):
                cost = _cost[:-1]
                if len(cost) == 1:
                    if cost.isnumeric():
                        C_cost += int(cost)
                    if cost == 'R':
                        R_cost += 1
            #print(f"The card {card['name']} costs {C_cost} coloress and {R_cost} red.")
            
            # Attemps to cast card.
            if "Dragon" in card["subtypes"] and self.mana_pool["Dragon"] > 0:
                # Attempt to cast a dragon.
                # Dragon mana is considered red.
                if (self.mana_pool["R"] + self.mana_pool["C"] + self.mana_pool["Dragon"] >= R_cost + C_cost) \
                    and (self.mana_pool["R"] + self.mana_pool["Dragon"] >= R_cost):
                    casted = True
                    self.cast(card)
                    print(f"Using SARKHAN mana to cast {card['name']}. <<<<<<<<<<<<<<<<<")
                    # Pay for red.
                    self.mana_pool["Dragon"] -= R_cost
                    if self.mana_pool["Dragon"] < 0:
                        self.mana_pool["R"] += self.mana_pool["Dragon"]
                    # Pay Colorless. Use Red only if there isn't enough C.
                    if self.mana_pool["C"] < C_cost:
                        self.mana_pool["R"] -= (C_cost - self.mana_pool["C"])
                        self.mana_pool["C"] = 0
                    else:
                        self.mana_pool["C"] - C_cost

                    print(f"Mana pool current has {self.mana_pool['R']} red mana and {self.mana_pool['C']} colorless mana.")

                    # Try to cast more cards.
                    self._cast_cards()

            elif (self.mana_pool["R"] + self.mana_pool["C"] >= R_cost + C_cost)\
                and (self.mana_pool["R"] >= R_cost):
                casted = True
                print(f"Beginning to cast {card['name']}.")
                self.cast(card)
                # Pay Red.
                self.mana_pool["R"] -= R_cost
                # Pay Colorless. Use Red only if there isn't enough C.
                if self.mana_pool["C"] < C_cost:
                    self.mana_pool["R"] -= (C_cost - self.mana_pool["C"])
                    self.mana_pool["C"] = 0
                else:
                    self.mana_pool["C"] - C_cost
            
                print(f"Mana pool current has {self.mana_pool['R']} red mana and {self.mana_pool['C']} colorless mana.")

                # Try to cast more cards.
                self._cast_cards()
        
        if not casted:
            print("Unable to cast anything this turn.")


    def _end_turn(self):
        self.turn += 1
        for key in self.mana_pool.keys():
            self.mana_pool[key] = 0
        print(f"Tempest has triggered {self.trigger_count} times.")
        print("Turn ended.")


    def get_human_names(self, cards):
        names = []
        for card in cards:
            names.append(card["name"])
        return names
