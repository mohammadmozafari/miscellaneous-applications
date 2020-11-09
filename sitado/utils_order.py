from database_engine import *

def new_order():
    print()
    deliver = input('deliver the food? (y, n): ')
    if deliver == 'y':
        if print_deliveries() == 0:
            return
        delivery = int(input('which delivery: '))
    else:
        delivery = None
    y = input('registered client ? (y/n): ')
    if y == 'y':
        print_clients()
        user = int(input('which user: '))
        if deliver == 'y':
            if print_addresses(user) == 0: return
            address = input('which address: ')
            for a in Address.select().where(Address.national_code_id == user, Address.name == address).execute(None):
                address = a.address
        else:
            address = None
    else:
        user = None
        if deliver:
            address = input('enter address: ')
        else:
            address = None
    if print_foods() == 0: return
    foods = input('which food (enter numbers seperated with space): ')
    foods = foods.split(' ')
    total_price = calculate_total_price(foods)
    params = {
        'price': total_price,
        'address': address,
        'client_id': user,
        'market_id': None,
        'delivery_id': delivery
    }
    receipt = Receipt(**params)
    change_database(receipt.save, **{})
    params = {
        'item_id': None,
        'receipt_id': receipt
    }
    for food in foods:
        params['item_id'] = int(food)
        change_database(Item_Receipt.create, **params)

def new_raw_material_order():
    print()
    if print_markets() == 0: return
    market = int(input('which market: '))
    if print_market_materials(market) == 0: return
    materials = input('which materials: ')
    materials = materials.split(' ')
    total_price = calculate_total_price(materials)
    params = {
        'price': total_price,
        'address': None,
        'client_id': None,
        'market_id': market,
        'delivery_id': None
    }
    receipt = Receipt(**params)
    change_database(receipt.save, **{})
    params = {
        'item_id': None,
        'receipt_id': receipt.id
    }
    for material in materials:
        params['item_id'] = int(material)
        change_database(Item_Receipt.create, **params)
