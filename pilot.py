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
    # GENERATE MANA
    #

    deck.tap_lands()

    for card in deck.battlefield:
        if card["name"] == "Sarkhan, Fireblood":
            deck.mana_pool["Dragon"] += 2
        elif card["name"] == "Chandra, Dressed to Kill":
            deck.mana_pool["R"] += 1

    print(f"Mana pool current has {deck.mana_pool['R']} R, {deck.mana_pool['C']} C and {deck.mana_pool['Dragon']} Dragon.")

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
    # ATTEMPT TO CAST SPELLS SMARTLY
    #

    #
    # SARKHAN, FIREBLOOD
    #

    # 1) If Tempest/Scourge are not on the battlefield, discard/draw (Mountain/Nykthos/other)
    # 2) If +2 mana would allow me to cast a dragon, do it
    # 3) If I have 4 lands down, discard/draw a Mountain
    # 4) If I have a Nykthos down, and one in hand, discard/draw it

    # Cast Dragon Tempest or Scourge as high priority.
    for card in deck.hand:
        if "Dragon Tempest" in card['name'] or "Scourge of Valkas" in card['name']:
            if deck.can_cast(card): 
                deck.cast(card)
                print(f"{card['name'].upper()} has been priority-cast!")

    # Attempt to cast Verix and kick it!
    mana_float = 0
    for value in deck.mana_pool.values():
        mana_float += value
    if mana_float >= 7 and deck.mana_pool["R"] + deck.mana_pool["Dragon"] >= 2:
        for card in deck.hand:
            if "Verix Bladewing" in card['name']:
                deck.cast(card)
                # Fake-cast the token.
                for token in deck._token_list:
                    if "Karox Bladewing" in token['name']:
                        deck.enter_the_battlefield(token)
                        deck.spend_mana(R=0, C=3, is_dragon=False)
                        print(f"{card['name'].upper()} was kicked!")

    # Attempt to activate Dragon Whisperer.    
    mana_float = 0
    for value in deck.mana_pool.values():
        mana_float += value
    total_power = 0
    for card in deck.battlefield:
        if 'power' in card:
            total_power += int(card['power'])
    if mana_float >= 6 and total_power >= 8:
        for card in deck.battlefield:
            if 'Dragon Whisperer' in card['name']:
                C = 4
                R = 2
                while deck.mana_pool["R"] >= R and deck.mana_pool["R"] + deck.mana_pool["C"] >= R+C:
                    for token in deck._token_list:
                        if "Dragon" in token['name']:
                            deck.spend_mana(R=R, C=C, is_dragon=False)
                            deck.enter_the_battlefield(token)
                            print(f"{card['name'].upper()} actviated an ability!")

    # Sort hand by CMC.
    cmc_hand= {} # { cmc:int, cards:array}
    for card in deck.hand:
        cmc = int(card["convertedManaCost"])
        if card["convertedManaCost"] in cmc_hand:
            cmc_hand[cmc].append(card)
        else:
            cmc_hand[cmc] = [card,]
    # Get mana float.
    mana_float = 0
    for key, value in deck.mana_pool.items():
        mana_float += value

    for cmc in range(mana_float, 0, -1):
        if cmc in cmc_hand:
            for card in cmc_hand[cmc]:
                if deck.can_cast(card): 
                    deck.cast(card)
                    #print(f">>>>>>> {card['name']} has been smart-cast.")


    #
    # CAST REMAINING SPELLS
    #

    for card in deck.hand:
        if deck.can_cast(card): 
            deck.cast(card)
            print(f"Remaining mana: {deck.mana_pool}.")

    print(f"Cards on the battlefield: {deck.get_human_names(deck.battlefield)}.")
    print(f"Dragon Trigger count: {deck.trigger_count}.")