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
    def reset(self):
        self.library = self._deck_list.copy()
        random.shuffle(self.library)
        self.turn = 0
        self.trigger_count = 0
        self.hand = []
        self.battlefield = []
        self.mana_pool = {"R": 0, "C": 0, "Dragon": 0,}
    

    # Draw a new card.
    def draw(self):
        self.hand.append(self.library.pop())
        if self.verbose: print(f"Card drawn. Hand: {self._get_human_names(self.hand)}.")
    

    # Reset, then draw X cards.
    def new_hand(self, draw=7):
        self.reset()
        for _ in range(draw):
            self.draw()
        if self.verbose: print(f"Card drawn. Hand: {self._get_human_names(self.hand)}.")


    # Cast a card.
    # Pay its mana. Put it on the battlefield. 
    # Look at triggers.
    def cast(self, card):
        self.hand.remove(card)
        self.battlefield.append(card)
        if self.verbose: print(f">> Cast {card['name']}! <<\nCards on the battlefield: {self.get_human_names(self.battlefield)}.")

        self.pay_mana_costs(card)

        if "Dragon" in card["subtypes"]:
            dragons = 0
            triggers = 0
            for permanent in self.battlefield:
                if "Dragon" in permanent["subtypes"]: 
                    dragons += 1
                if "Dragon Tempest" in permanent["name"] or "Scourge of Valkas" in permanent["name"]:
                    triggers += 1
            
            self.trigger_count += dragons * triggers



    #
    # HELPER FUNCTIONS
    #


    # Return an array of card names.
    def get_human_names(self, cards):
        names = []
        for card in cards:
            names.append(card["name"])
        return names
    

    # Return the Red mana and the Colorless mana required for this card.
    def get_mana_cost(self, card):
        R, C = 0

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
            cannot_afford_colorless = self.mana_pool["C"] < C

            # Cover the colorless cost using Dragon mana.
            if cannot_afford_colorless:
                to_spend = C - self.mana_pool["C"]

                C -= to_spend
                self.mana_pool["Dragon"] -= to_spend
                
            to_spend = 0
            if self.mana_pool["Dragon"] <= R:
                to_spend = self.mana_pool["Dragon"]
            else:
                to_spend = R
            
            self.mana_pool["Dragon"] -= to_spend            
            R -= to_spend

            # Now attempt to pay colorless cost.
            if self.mana_pool["Dragon"] > 0:
                to_spend = 0
                if self.mana_pool["Dragon"] <= C:
                    to_spend = self.mana_pool["Dragon"]
                else:
                    to_spend = C
                
                self.mana_pool["Dragon"] -= to_spend            
                C -= to_spend

        # Pay remaining red mana.
        if self.mana_pool["R"] >= R:
            self.mana_pool["R"] -= R
        else:
            print(f"ERROR! Tried to cast {card['name']} without enough mana to pay red cost!")
        
        # Pay remaining colorless mana.
        if self.mana_pool["R"] + self.mana_pool["C"] >= C:
            # First, pay using colorless.
            to_spend = 0

            if self.mana_pool["C"] <= C:
                to_spend = self.mana_pool["C"]
            else:
                to_spend = C
            
            self.mana_pool["C"] -= to_spend            
            C -= to_spend

            # Then, pay using red.
            to_spend = 0

            if self.mana_pool["R"] <= C:
                to_spend = self.mana_pool["R"]
            else:
                to_spend = C
            
            self.mana_pool["R"] -= to_spend            
            C -= to_spend

        else:
            print(f"ERROR! Tried to cast {card['name']} without enough mana to pay colorless cost!")

        pass