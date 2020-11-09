from datetime import datetime
from database_engine import *
from utils_delivery import *
from utils_market import *
from utils_item import *
from utils_client import *
from utils_order import *
from utils_report import *
from utils_recreation import *
from utils_logs import *

def food_material():
    general_menu('FOODS', 3, ['show all items', 'add new item', 'update item', 'delete item'], [show_items, add_item, update_item, delete_item])

def client():
    general_menu('CLIENTS', 4, ['show all clients', 'show all addresses', 'add new client', 'update some client', 'delete some client', 'add address'],
                                [show_clients, show_addresses, add_client, update_client, delete_client, add_address])

def delivery():
    general_menu('DELIVERIES', 5, ['show all deliveries', 'add new delivery', 'update existing delivery', 'delete delivery'],
                 [show_deliveries, add_delivery, update_delivery, delete_delivery])

def market():
    general_menu('MARKETS', 6, ['show all markets', 'add new market', 'update existing market', 'delete market'],
                                [show_markets, add_market, update_market, delete_market])

def report():
    general_menu('REPORTS', 7, ['manager reports', 'user reports'],
                                [show_manager_reports, show_client_reports])

def manage_tables():
    general_menu('TABLES', 8, ['create', 'delete'], [build_table, remove_table])

def log():
    log_menu()

def general_menu(title, base, titles, functions):
    print()
    print('**************************************************')
    print(title)
    for i, title in enumerate(titles):
        print('%d.%d - %s' % (base, i+1, title))
    choice = int(input('WHAT DO YOU WANNA DO: '))
    functions[choice-1]()

while True:
    general_menu('MAIN MENU', 1, ['new order', 'new material order', 'foods & materials', 'clients', 'deliveries', 'markets', 'reports', 'tables', 'logs', 'exit'],
                                 [new_order, new_raw_material_order, food_material, client, delivery, market, report, manage_tables, log, exit])
