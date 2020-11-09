from database_engine import *

def show_markets():
    print()
    print_markets()
    input('press enter to return to main menu')


def add_market():
    print()
    name = input('enter name of the new market: ')
    active = 1
    params = {
        'name': name,
        'active': active
    }
    change_database(Market.create, **params)


def update_market():
    print()
    print_markets()
    market = input('which market: ')
    name = input('enter name of the new market: ')
    active = int(input('is market active (1/0): '))
    market = Market.get_by_id(market)
    market.name = name
    market.active = active
    change_database(market.save, **{})


def delete_market():
    print()
    print_markets()
    market = input('which market: ')
    market = Market.get_by_id(market)
    market.active = 0
    change_database(market.save, **{})
