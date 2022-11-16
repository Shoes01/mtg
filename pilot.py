from deck_v2 import Deck


def play(deck):

    #
    # PLAY LAND
    #

    if deck.turn < 3:
        # Only play mountains first.
        for card in deck.hand:
            if "Mountain" in card["name"]:
                deck.cast(card)
                break
        else:
            # No mountains! Try to play Nykthos.
            for card in deck.hand:
                if "Land" in card["types"]:
                    deck.cast(card)
                    break
    else:
        for card in deck.hand:
            if "Land" in card["types"]:
                deck.cast(card)
                break

    #
    # TAP LANDS
    #

    deck.generate_mana()

    #
    # NYTHOS CHECK
    #

    devotion = deck.get_devotion()
    if devotion >= 3 and deck.mana_pool["C"] + deck.mana_pool["R"] >= 3:
        for card in deck.battlefield:
            if "Nykthos, Shrine to Nyx" in card['name']: 
                # Tap Nykthos and 2 other lands.
                # IE, remove 3 mana from the pool. Colorless, ideally.
                # Then add R mana equal to devotion.
                nykthos_cost = 3
                while nykthos_cost and deck.mana_pool["C"]:
                    nykthos_cost -= 1
                    deck.mana_pool["C"] -= 1
                while nykthos_cost and deck.mana_pool["R"]:
                    nykthos_cost -= 1
                    deck.mana_pool["R"] -= 1
                if nykthos_cost == 0:
                    deck.mana_pool["R"] += devotion
                    print(f"Activated Nykthos ability.")
                    print(f"Mana pool current has {deck.mana_pool['R']} R, {deck.mana_pool['C']} C and {deck.mana_pool['Dragon']} Dragon.")
                else:
                    print(f"[ERROR] Tried to activate Nykthos ability, but there is still {nykthos_cost} mana left to pay!")
                
    

    #
    # CAST SPELL
    #

    for card in deck.hand:
        if deck.can_cast(card): 
            deck.cast(card)
            print(f"Remaining mana: {deck.mana_pool}.")

    print(f"Cards on the battlefield: {deck.get_human_names(deck.battlefield)}.")
    print(f"Dragon Trigger count: {deck.trigger_count}.")