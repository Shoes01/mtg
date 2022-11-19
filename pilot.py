from deck_v2 import Deck


def play(deck):

    #
    # PLAY LAND
    # Unless I have Sarkhan in hand! Then I may want to discard it instead.

    has_sarkhan = deck.hand_has("Sarkhan, Fireblood")

    land_count = 0
    for card in deck.battlefield:
        if "Land" in card["types"]:
            land_count += 1
    print(f"Land count is {land_count}")

    if deck.turn < 3:
        # Only play mountains first.
        mountain = deck.hand_has('Mountain')
        land = deck.hand_has('Land')
        if mountain:
            deck.cast(mountain)
        elif land:
            deck.cast(land)
    elif land_count >= 5 and has_sarkhan:
        # I have enough lands and a Sarkhan in hand. Discard it.
        # Unless it's my first Nykthos.
        casted_nykthos = deck.battlefield_has('Nykthos, Shrine to Nyx')
        inhand_nythos = deck.hand_has('Nykthos, Shrine to Nyx')
        if not casted_nykthos and inhand_nythos:
            deck.cast(inhand_nythos)
    elif deck.get_devotion >= 3 and not deck.battlefield_has('Nykthos, Shrine to Nyx'):

        
    else:
        # Try to cast Nykthos first.
        for card in deck.hand:
            if "Nykthos, Shrine to Nyx" in card["name"]:
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
        if card["name"] == "Chandra, Dressed to Kill":
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
    # NOTE: The AI for using the +2 mana ability can be improved.
    
    for card in deck.battlefield:
        if "Sarkhan, Fireblood" in card["name"]:
            pilot_sarkhan(deck)

    # Try to play a land again. 
    if not deck.land_dropped:
        for card in deck.hand:
            if "Land" in card["types"]:
                deck.cast(card)
                deck.tap_land(card)
                break

    # Cast Dragon Tempest or Scourge as high priority.
    for card in deck.hand:
        if "Dragon Tempest" in card['name'] or "Scourge of Valkas" in card['name']:
            if deck.can_cast(card): 
                deck.cast(card)
                print(f"{card['name'].upper()} has been priority-cast!")

    # Attempt to cast Verix and kick it!
    mana_float = deck.get_floating_mana()
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
    for card in deck.hand:
        if "Dragon Whisperer" in card['name']:
            activate(deck, card)

    # Sort hand by CMC.
    cmc_hand= {} # { cmc:int, cards:array}
    for card in deck.hand:
        cmc = int(card["convertedManaCost"])
        if card["convertedManaCost"] in cmc_hand:
            cmc_hand[cmc].append(card)
        else:
            cmc_hand[cmc] = [card,]
    # Get mana float.
    mana_float = deck.get_floating_mana()
    for cmc in range(mana_float, 0, -1):
        if cmc in cmc_hand:
            for card in cmc_hand[cmc]:
                if deck.can_cast(card): 
                    deck.cast(card)
                    if "Sarkhan, Fireblood" in card["name"]:
                        pilot_sarkhan(deck)
                    if "Dragon Whisperer" in card["name"]:
                        activate(deck, card)
                    #print(f">>>>>>> {card['name']} has been smart-cast.")


    #
    # CAST REMAINING SPELLS
    #

    for card in deck.hand:
        if deck.can_cast(card): 
            deck.cast(card)
            if "Sarkhan, Fireblood" in card["name"]:
                pilot_sarkhan(deck)
            print(f"Remaining mana: {deck.mana_pool}.")

    print(f"Cards on the battlefield: {deck.get_human_names(deck.battlefield)}.")
    print(f"Dragon Trigger count: {deck.trigger_count}.")


def pilot_sarkhan(deck):
    print("Sarkhan, Fireblood is on the battlefield.")
    #
    # Use the +2 mana ability if it would allow me to cast a dragon.
    #
    highest_cmc = 0
    mana_pool = deck.get_floating_mana()
    for card in deck.hand:
        if "Dragon" in card["subtypes"]:
            card_cmc = int(card["convertedManaCost"])
            if "Verix Bladewing" in card["name"]:
                card_cmc += 3 # Cover the cost of Kicker.
            if card_cmc > highest_cmc:
                highest_cmc = card_cmc
    print(f"The dragon with highest cmc has {highest_cmc} cmc, and the mana_pool is has {mana_pool}.")
    if highest_cmc > mana_pool and highest_cmc <= mana_pool + 2:
        # +2 would allow me to cast a dragon.
        deck.mana_pool["Dragon"] += 2
        print(f"Activated Sarkhan's mana ability.")
        return

    #
    # If I have 5+ mana, discard/draw a land.
    #
    used_discard_ability = False
    if mana_pool >= 5:
        print("I have 5+ mana, so I will discard/draw a land.")
        # Discard/draw a land.
        for card in deck.hand:
            if "Land" in card["types"]:
                print(f"Activated Sarkhan's discard ability due to high mana pool.")
                deck.discard(card)
                deck.draw()
                used_discard_ability = True
                break
        else:
            print(f"[ERROR] Tried to discard a land, but there are no lands in hand!")
        if used_discard_ability:
            return
    
    #
    # If I have Nykthos down, and one in hand, discard/draw it.
    #
    has_nykthos = False
    for card in deck.battlefield:
        if "Nykthos, Shrine to Nyx" in card["name"]:
            has_nykthos = True
            break
    print(f"Has Nykthos: {has_nykthos}")
    if has_nykthos:
        for card in deck.hand:
            if "Nykthos, Shrine to Nyx" in card["name"]:
                print(f"Activated Sarkhan's discard ability due to Nykthos.")
                deck.discard(card)
                deck.draw()
                used_discard_ability = True
                break
        if used_discard_ability:
            return
    
    #
    # If Tempest/Scourge are not on the battlefield, discard/draw (Mountain/Nykthos/other)
    #
    has_dragon_trigger = False
    for card in deck.battlefield:
        if "Dragon Tempest" in card['name'] or "Scourge of Valkas" in card['name']:
            has_dragon_trigger = True
            break
    print(f"Has Dragon Tempest or Scourge of Valkas: {has_dragon_trigger}")
    if not has_dragon_trigger:
        # Discard/draw a land.
        for card in deck.hand:
            if "Land" in card["types"]:
                print(f"Activated Sarkhan's discard ability due to lack of Dragon Tempest/Scourge of Valkas.")
                deck.discard(card)
                deck.draw()
                used_discard_ability = True
                break
        else:
            for card in deck.hand:
                if "Dragon" not in card["types"]:
                    print(f"Activated Sarkhan's discard ability due to lack of Dragon Tempest/Scourge of Valkas.")
                    deck.discard(card)
                    deck.draw()
                    used_discard_ability = True
                    break
        if used_discard_ability:
            return
    
    print(f"[WARNING] Did not use Sarkhan's ability.")
    return


def activate(deck, card):
    if "Dragon Whisperer" in card['name']:
        mana_float = deck.get_floating_mana()
        total_power = 0
        for card in deck.battlefield:
            if 'power' in card:
                total_power += int(card['power'])
        if mana_float >= 6 and total_power >= 8:
            C, R = 4, 2
            while deck.mana_pool["R"] >= R and deck.mana_pool["R"] + deck.mana_pool["C"] >= R+C:
                for token in deck._token_list:
                    if "Dragon" in token['name']:
                        deck.spend_mana(R=R, C=C, is_dragon=False)
                        deck.enter_the_battlefield(token)
                        print(f"{card['name'].upper()} actviated an ability!")
        return
