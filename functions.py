MASTER = {
    'monthly_dining': 'Dining',
    'monthly_groceries': 'Grocery',
    'monthly_gas': 'Gas',
    'monthly_streaming': 'Streaming',
    'monthly_online_shopping': 'Online_Shopping',
    'monthly_drugstore/pharmacy': "Drugstore",
    'monthly_other': 'Other',

    # travel (non-portal)
    'monthly_travel': 'Travel',
    'monthly_hotel': 'Hotel',
    'monthly_flights': 'Flights',

    # travel (portal)
    'monthly_hotel_portal': 'PORTAL_HOTEL',
    'monthly_flights_portal': 'PORTAL_FLIGHT',
    'monthly_car_rental_portal': 'PORTAL_CAR'
}

PORTAL_BY_ISSUER = {
    'American Express': {
        'unified': 'AmexTravel',
        'hotel':  'AmexTravel Hotels (Prepaid)',
        'flight': 'AmexTravel Flights',
        'car': 'AmexTravel Car Rentals'
    },
    'Chase': {
        'unified': 'Chase Travel',
        'hotel':  'Chase Travel - Hotels',
        'flight': 'Chase Travel - Flights',
        'car': 'Chase Travel - Car Rentals'
    },
    'Capital One': {
        'unified': 'Capital One Travel',
        'hotel':  'Capital One Travel - Hotels',
        'flight': 'Capital One Travel - Flights',
        'car': 'Capital One Travel - Car Rentals'
    },
}

def get_MASTER():
    return MASTER

def get_issuer_portals():
    return PORTAL_BY_ISSUER


def resolve_formal(formal_cat: str, card: dict) -> str:
    
    # If the category is not related to a portal category, return the category (e.g. Dining, Grocery, etc.)
    if formal_cat not in ('PORTAL_HOTEL', 'PORTAL_FLIGHT', 'PORTAL_CAR'):
        return formal_cat

    issuer = card.get('issuer')

    # Single out the travel portal for the issuer
    portal = PORTAL_BY_ISSUER.get(issuer, {})
    card_cats = card.get('spending_categories', {})

    # If the card has a specific label (e.g. Chase Travel - Hotel) use that 
    if formal_cat == 'PORTAL_HOTEL':
        specific = portal.get('hotel')
        unified  = portal.get('unified')
        # If the card has a specific label (e.g. Chase Travel - Hotel) use that 
        if specific and specific in card_cats:
            return specific
        # Not the card doesn't have portal cateogry for it, fallback to general travel portal
        if unified and unified in card_cats:
            return unified
        return 'Other'  # last-resort fallback

    if formal_cat == 'PORTAL_FLIGHT':
        specific = portal.get('flight')
        unified  = portal.get('unified')
        if specific and specific in card_cats:
            return specific
        if unified and unified in card_cats:
            return unified
        return 'Other'
    
    if formal_cat == 'PORTAL_CAR':
        specific = portal.get('car')
        unified  = portal.get('unified')
        if specific and specific in card_cats:
            return specific
        if unified and unified in card_cats:
            return unified
        return 'Other'


def calc_point_return(user, card):
    user_spend = user['spending_categories']
    card_cats  = card['spending_categories']

    total_points = 0
    breakdown = {}

    for user_cat, amt in user_spend.items():
        # 1) default unknown user categories -> 'Other'
        formal = resolve_formal(MASTER.get(user_cat, 'Other'), card)
        # 2) if the card lacks that formal category, fall back to card's 'Other' (or 1x)
        if formal in card_cats:
            earn_rate = card_cats[formal]
        elif 'Other' in card_cats:
            earn_rate = card_cats['Other']
        else:
            earn_rate = 1

        pts = amt * earn_rate

        total_points += pts
        breakdown[user_cat] = dict(amount=amt, formal=formal,
                                   earn_rate=earn_rate, points=pts)

    return total_points, breakdown


def best_points_card(user, cards: dict):
    '''
    user: take in a whole instance in users.json
    cards: the entirety of card_data.json

    returns: the sorted cards from earning points by spend (descending).
    
    '''

    points_dict = {}

    for key, value in cards.items():
        points_dict[key] = calc_point_return(user, cards[key])[0]

    points_dict = dict(sorted(points_dict.items(), key=lambda item: item[1], reverse=True))
    
    return points_dict



