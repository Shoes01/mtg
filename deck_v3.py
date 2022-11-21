import random

# A general deck, with deck-related functions.
# Does not contain pilot logic.
class Deck():
    def __init__(self, cards, tokens):
        self._deck_list = cards     
        self._token_list = tokens

        self.library = self._deck_list.copy()
        self.turn = 0
        self.hand = []
        self.battlefield = []
        self.land_dropped = False
        self.mana_pool = {"R": 0, "C": 0, "Dragon": 0}
        self.graveyard = []

        self.trigger_count = 0
        self.verbose = True
        self.log = []


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
    

    # Cast a card from hand.
    # 
    def cast(self, card_name):
        card = self.get_card_by_name(card_name)
        if card is None:
            print(f"ERROR: Card {card_name} not found.")
            return
        if "Land" in card["types"]:
            if self.land_dropped:
                return
            self.land_dropped = True
        elif self.can_pay_cost(card):
            self.pay_cost(card)
            self.battlefield.append(card)
            self.hand.remove(card)
            if self.verbose: print(f"Card cast: {card['name'].upper()}.\nBattlefield: {self.get_human_names(self.battlefield)}.")

    # Get a card by name.
    def get_card_by_name(self, card_name):
        for card in self.hand:
            if card_name in card["name"]:
                return card
        return None
    

    def can_pay_cost(self, card):
        R, C = self.get_mana_cost(card)
        dragon_mana = self.mana_pool["Dragon"] if "Dragon" in card["subtypes"] else 0
        if R + C > self.mana_pool["R"] + self.mana_pool["C"] + dragon_mana or R > self.mana_pool["R"] + dragon_mana:
            return False
        return True


    def pay_cost(self, card):
        R, C = self.get_mana_cost(card)
        is_dragon = "Dragon" in card["subtypes"]
        self.spend_mana(R, C, is_dragon)


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