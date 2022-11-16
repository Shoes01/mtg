import random

# A general deck, with deck-related functions.
# Does not contain pilot logic.
class Deck():
    def __init__(self, cards):
        self._deck_list = cards     

        self.library = self._deck_list.copy()
        self.turn = 0
        self.trigger_count = 0
        self.hand = []
        self.battlefield = []
        self.land_dropped = False
        self.mana_pool = {
            "R": 0,
            "C": 0, # Don't need other colors...
            "Dragon": 0,
        }
        self.verbose = True


    #
    # CORE FUNCTIONS
    #


    # Reset everything for a new game.
    def _reset(self):
        self.library = self._deck_list.copy()
        random.shuffle(self.library)
        self.turn = 1
        self.trigger_count = 0
        self.hand = []
        self.battlefield = []
        self.mana_pool = {"R": 0, "C": 0, "Dragon": 0,}
    

    # Draw a new card.
    def draw(self, new_hand=False):
        card = self.library.pop()
        self.hand.append(card)
        if self.verbose and not new_hand: print(f"Card drawn: {card['name'].upper()}.\nHand: {self.get_human_names(self.hand)}.")
    

    # Reset, then draw X cards.
    def new_hand(self, draw=7):
        self._reset()
        for _ in range(draw):
            self.draw(new_hand=True)
        if self.verbose: 
            print(f"-- NEW GAME --") 
            print(f"-- STARTING TURN {self.turn} --")
            print(f"Starting Hand: {self.get_human_names(self.hand)}.")


    # Cast a card.
    # Pay its mana. Put it on the battlefield. 
    # Look at triggers.
    def cast(self, card):
        self.hand.remove(card)
        if not self.dies_to_legend_rule(card):
            self.battlefield.append(card)


        self.pay_mana_costs(card)

        # Check for Dragon triggers.
        if "Dragon" in card["subtypes"]:
            dragons = 0
            triggers = 0
            for permanent in self.battlefield:
                if "Dragon" in permanent["subtypes"]: 
                    dragons += 1
                if "Dragon Tempest" in permanent["name"] or "Scourge of Valkas" in permanent["name"]:
                    triggers += 1
            
            self.trigger_count += dragons * triggers
        
        if "Land" in card["types"]:
            self.land_dropped = True
        
        if self.verbose: print(f">> Cast {card['name'].upper()}! <<")


    # Generate R, C or Dragon mana.
    def generate_mana(self):
        # TODO: Have some code for tapping Nykthos
        for card in self.battlefield:
            if "Land" in card["types"]:
                if card["name"] == "Mountain": 
                    self.mana_pool["R"] += 1
                else:
                    self.mana_pool["C"] += 1
            
            elif card["name"] == "Sarkhan, Fireblood":
                self.mana_pool["Dragon"] += 2
            
            elif card["name"] == "Chandra, Dressed to Kill":
                self.mana_pool["R"] += 1
        
        if self.verbose: print(f"Mana pool current has {self.mana_pool['R']} R, {self.mana_pool['C']} C and {self.mana_pool['Dragon']} Dragon.")


    # End turn, start next turn.
    def next_turn(self):
        self.turn += 1
        if self.verbose: print(f"\n-- STARTING TURN {self.turn} --")
        empty_mana_pool = True
        for card in self.battlefield:
            if "Leyline Tyrant" in card['name']:
                empty_mana_pool = False
                break
        if empty_mana_pool:
            for key in self.mana_pool.keys():
                self.mana_pool[key] = 0
        self.draw()
        self.land_dropped = False


    #
    # HELPER FUNCTIONS
    #

    # Return True if the card can be cast.
    def can_cast(self, card):
        # Only one land per turn
        if "Land" in card["types"] and self.land_dropped:
            return False
        # Need to afford the card.
        R, C = self.get_mana_cost(card)
        dragon_mana = self.mana_pool["Dragon"] if "Dragon" in card["subtypes"] else 0
        if R + C > self.mana_pool["R"] + self.mana_pool["C"] + dragon_mana or R > self.mana_pool["R"] + dragon_mana:
            return False
        
        return True


    # Return an array of card names.
    def get_human_names(self, cards):
        names = []
        for card in cards:
            names.append(card["name"])
        return sorted(names)
    

    # Return the Red mana and the Colorless mana required for this card.
    def get_mana_cost(self, card):
        R, C = 0, 0
        
        if card["convertedManaCost"] == 0.0: 
            return R, C
        
        for _cost in card["manaCost"].split("{"):
            cost = _cost[:-1]
            if len(cost) == 1:
                if cost.isnumeric():
                    C += int(cost)
                elif cost == 'R':
                    R += 1
                elif cost == 'X':
                    C += 1

        return R, C

    
    # Pay the costs for the card.
    def pay_mana_costs(self, card):
        R, C = self.get_mana_cost(card)
        is_dragon = "Dragon" in card["subtypes"]

        if is_dragon:
            # Pay for R using Dragon mana.
            while R and self.mana_pool["Dragon"]:
                self.mana_pool["Dragon"] -= 1
                R -= 1
            # Pay fro C using Dragon mana, if there is any left.
            while C and self.mana_pool["Dragon"]:
                self.mana_pool["Dragon"] -= 1
                C -= 1

        # Pay for R using R mana.
        while R and self.mana_pool["R"]:
            self.mana_pool["R"] -= 1
            R -= 1
        # Pay for C using C mana.
        while C and self.mana_pool["C"]:
            self.mana_pool["C"] -= 1
            C -= 1
        # Finally, pay for C using R mana.
        while C and self.mana_pool["R"]:
            self.mana_pool["R"] -= 1
            C -= 1
            


    def dies_to_legend_rule(self, card):
        is_legendary = "Legendary" in card["supertypes"]

        if is_legendary:
            for permanent in self.battlefield:
                # In the case of Nykthos.
                # or In the cast of PW.
                if (permanent["name"] == card["name"]) \
                    or ("Planeswalker" in card["types"] and card["subtypes"] == permanent["subtypes"]):
                    if self.verbose: print(f"[WARNING] {card['name']} dies to the Legend Rule.")
                    return True

        return False
    

    def get_devotion(self):
        devotion = 0
        for card in self.battlefield:
            R, _ = self.get_mana_cost(card)
            devotion += R
        return devotion