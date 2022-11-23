import random

# A general deck, with deck-related functions.
# Does not contain pilot logic.
class Deck():
    def __init__(self, cards, tokens):
        self._deck_list = cards     
        self._token_list = tokens

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
        self.verbose = False
        self.log = []
        self.graveyard = []


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
        self.log.append(f"NEW GAME: Starting Hand: {self.get_human_names(self.hand)}.\n")


    # Cast a card.
    # Pay its mana. Put it on the battlefield. 
    # Look at triggers.
    def cast(self, card):
        if not self.can_cast(card): return False
        
        self.hand.remove(card)
        self.pay_mana_costs(card)
        self.enter_the_battlefield(card)
        
        if self.verbose: print(f">> Cast {card['name'].upper()}! <<")


    # Generate Red or Colorless mana.
    def tap_lands(self):
        for card in self.battlefield:
            if "Land" in card["types"]:
                self.tap_land(card)


    # Tap the individual land.
    def tap_land(self, card):
        if card['name'] == "Mountain":
            self.mana_pool["R"] += 1
        else:
            self.mana_pool["C"] += 1

    # End turn, start next turn.
    def next_turn(self):
        self.log.append(f" Turn: {self.turn}. Trigger count: {self.trigger_count}. Hand: {self.get_human_names(self.hand)}. Battlefield: {self.get_human_names(self.battlefield)}.\n")

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

    
    # Put the card on the battlefield.
    # Trigger effects.
    # Note: Does not remove from hand.
    def enter_the_battlefield(self, card):
        if not self.dies_to_legend_rule(card):
            self.battlefield.append(card)

        # Check for Dragon triggers.
        if "Dragon" in card["subtypes"] or "Shapeshifter" in card["subtypes"]:
            dragons = 0
            triggers = 0
            for permanent in self.battlefield:
                if "Dragon" in permanent["subtypes"] or "Shapeshifter" in permanent["subtypes"]:
                    dragons += 1
                if "Dragon Tempest" in permanent["name"] or "Scourge of Valkas" in permanent["name"]:
                    triggers += 1
            
            self.trigger_count += dragons * triggers
        
        if "Land" in card["types"]:
            self.land_dropped = True


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
        dragon_mana = self.mana_pool["Dragon"] if "Dragon" in card["subtypes"] or "Shapeshifter" in card["subtypes"] else 0
        if R + C > self.mana_pool["R"] + self.mana_pool["C"] + dragon_mana or R > self.mana_pool["R"] + dragon_mana:
            return False
        for c in self.hand:
            if c == card:
                return True
        return False


    # Return an array of card names.
    def get_human_names(self, cards):
        names = []
        for card in cards:
            names.append(card["name"])
        return sorted(names)
    

    # Return the Red mana and the Colorless mana required for this card.
    def get_mana_cost(self, card):
        R, C = 0, 0
        
        if 'Token' in card['types'] or card["convertedManaCost"] == 0.0: 
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

    
    # Pay arbitrary cost
    def spend_mana(self, R, C, is_dragon):
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


    # Pay the costs for the card.
    def pay_mana_costs(self, card):
        R, C = self.get_mana_cost(card)
        is_dragon = "Dragon" in card["subtypes"] or "Shapeshifter" in card["subtypes"]
        self.spend_mana(R, C, is_dragon)
            


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
    

    def get_floating_mana(self):
        return self.mana_pool["Dragon"] + self.mana_pool["R"] + self.mana_pool["C"]
    

    def discard(self, card):
        self.hand.remove(card)
        self.graveyard.append(card)
        if self.verbose: print(f"Card discarded: {card['name'].upper()}")


    def hand_has(self, card_property):
        for card in self.hand:
            if card_property in card["name"] or card_property in card["types"]:
                return card
        return False

    
    def battlefield_has(self, card_property):
        for card in self.battlefield:
            if card_property in card["name"] or card_property in card["types"]:
                return card
        return False

    
