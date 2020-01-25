from datetime import datetime
from database_engine import *

def new_order():
    print()
    y = input('registered client ? (y/n): ')
    if y == 'y':
        print('showing all the users')
        user = int(input('which user: '))
        print('showing user\'s addresses')
        address = int(input('which address: '))
    else:
        user = None
    
    print()
    print('showing all the items on the menu')
    foods = input('which food (enter numbers seperated with space): ')
    foods = foods.split(' ')

    # find total price
    total_price = 0

    print()
    deliver = input('deliver the food? (y, n): ')
    if deliver == 'y':
        print('showing all available deliveries')
        delivery = int(input('which delivery: '))
    else:
        delivery = None

    market = None

    print()
    print('new order added.')
    # add order to list of orders

def new_raw_material_order():
    print()
    print('showing all raw materials')
    raw = int(input('which material: '))
    print('list of active markets for the material')
    market = int(input('which market: '))
    print('new raw material order added.')

# food management
def show_food():
    print()
    print('showing all the foods')
    input('press enter to return to main menu')
def add_food():
    print()
    name = input('enter name of the new food: ')
    price = float(input('enter the food cost: '))
    # set its expiration date
    print('new food added')
def update_food():
    print()
    print('showing all foods')
    food = input('which food: ')
    price = float(input('enter the new food cost: '))
    # set its expiration date
    print('food updated')
def delete_food():
    print()
    print('showing all foods')
    food = input('which food: ')
    print('food deleted')

# client management
def show_clients():
    print()
    print('showing all the foods')
    input('press enter to return to main menu')
def show_addresses():
    print()
    print('all clients')
    client = input('which client: ')
    print('showing all client addresses')
    input('press enter to return to main menu')
def add_client():
    print()
    first_name = input('enter first name: ')
    last_name = input('enter last name: ')
    phone_number = input('enter mobile phone number: ')
    age = input('enter age: ')
    address = input('enter address (only 1, later you can add more): ')
    phone = input('enter home phone number: ')
    # set its expiration date
    print('new client added')
def update_client():
    print()
    print('showing all clients')
    client = input('which client: ')
    first_name = input('enter first name: ')
    last_name = input('enter last name: ')
    phone_number = input('enter mobile phone number: ')
    # set its expiration date
    print('client updated')
def delete_client():
    print()
    print('showing all clients')
    client = input('which client: ')
    print('client deleted')
def add_address():
    print()
    print('all clients')
    client = input('which client: ')
    address = input('enter new address: ')
    phone = input('enter home phone: ')
    print('address added')

# delivery management
def show_deliveries():
    print()
    print_deliveries()
    input('press enter to return to main menu')
def add_delivery():
    print()
    first_name = input('enter first name: ')
    last_name = input('enter last name: ')
    phone = input('enter phone number: ')
    params = {
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone
    }
    if change_database(Delivery.create, **params):
        print('new delivery added')
    else:
        print('something went wrong')
def update_delivery():
    print()
    print_deliveries()
    delivery = input('which delivery: ')
    first_name = input('enter first name: ')
    last_name = input('enter last name: ')
    phone = input('enter phone number: ')
    delivery = Delivery.get_by_id(delivery)
    delivery.first_name = first_name
    delivery.last_name = last_name
    delivery.phone_number = phone
    if change_database(delivery.save, **{}):
        print('delivery updated')
    else:
        print('something went wrong')
def delete_delivery():
    print()
    print_deliveries()
    delivery = input('which delivery: ')
    params = {
        'pk': delivery
    }
    if change_database(Delivery.delete_by_id, **params):
        print('delivery deleted')
    else:
        print('something went wrong')

# market management
def show_markets():
    print()
    print_markets()
    input('press enter to return to main menu')
def add_market():
    print()
    name = input('enter name of the new market: ')
    active = 1
    Market.create(name=name, active=active)
    print('new market added')
def update_market():
    print()
    print_markets()
    market = input('which market: ')
    name = input('enter name of the new market: ')
    market = Market.get_by_id(market)
    market.name = name
    market.save()
    print('market updated')
def delete_market():
    print()
    print_markets()
    market = input('which market: ')
    Market.delete_by_id(market)
    print('market deleted')

# reports
def show_user_reports():
    print()
    client = input('which client: ')
    print('reports')
def show_manager_reports():
    print()
    print('reports')


def food():
    general_menu('FOODS', 2, ['show all foods', 'add new food', 'update some food', 'delete food'], [show_food, add_food, update_food, delete_food])

def client():
    general_menu('CLIENTS', 4, ['show all clients', 'add new client', 'update some client', 'delete some client', 'show all addresses', 'add address'], [])

def market():
    general_menu('MARKETS', 6, ['show all markets', 'add new market', 'update existing market', 'delete market'],
                                [show_markets, add_market, update_market, delete_market])

def delivery():
    general_menu('DELIVERIES', 5, ['show all deliveries', 'add new delivery', 'update existing delivery', 'delete delivery'],
                                    [show_deliveries, add_delivery, update_delivery, delete_delivery])

def general_menu(title, base, titles, functions):
    print()
    print('**************************************************')
    print(title)
    for i, title in enumerate(titles):
        print('%d.%d- %s' % (base, i+1, title))
    choice = int(input('WHAT DO YOU WANNA DO: '))
    functions[choice-1]()

while True:
    general_menu('MAIN MENU', 1, ['new order', 'foods', 'raw_materials', 'clients', 'deliveries', 'markets', 'reports', 'exit'],
                          [new_order, food, None, None, delivery, market, None, exit])
