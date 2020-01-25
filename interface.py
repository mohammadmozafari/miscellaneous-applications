from datetime import datetime
from database_engine import *
from utils_delivery import *
from utils_market import *
from utils_item import *
from utils_client import *

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

# reports
def show_user_reports():
    print()
    client = input('which client: ')
    print('reports')
def show_manager_reports():
    print()
    print('reports')


def food_material():
    general_menu('FOODS', 2, ['show all items', 'add new item', 'update item', 'delete item'], [show_items, add_item, update_item, delete_item])

def client():
    general_menu('CLIENTS', 4, ['show all clients', 'show all addresses', 'add new client', 'update some client', 'delete some client', 'add address'],
                                [show_clients, show_addresses, add_client, update_client, delete_client, add_address])

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
    general_menu('MAIN MENU', 1, ['new order', 'foods & materials', 'clients', 'deliveries', 'markets', 'reports', 'exit'],
                          [new_order, food_material, client, delivery, market, None, exit])
