from database_engine import *
from datetime import datetime

def show_items():
    print()
    print_items()
    input('press enter to return to main menu')


def add_item():
    print()
    name = input('enter name of the new item: ')
    price = float(input('enter the item cost: '))
    food = int(input('is the new item food (1/0): '))
    params = {
        'name': name,
        'price': price,
        'food': food
    }
    change_database(Item.create, **params)


def update_item():
    print()
    print_items()
    item = input('which item: ')
    name = input('enter name of the new item: ')
    price = float(input('enter the item cost: '))
    food = int(input('is the new item food (1/0): '))
    params = {
        'name': name,
        'price': price,
        'food': food
    }
    item = Item.get_by_id(item)
    item.end_time = datetime.now()
    if change_database(Item.create, **params):
        change_database(item.save, **{})


def delete_item():
    print()
    print_items()
    item = input('which item: ')
    item = Item.get_by_id(item)
    item.end_time = datetime.now()
    change_database(item.save, **{})
