from database_engine import *

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
    change_database(Delivery.create, **params)


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
    change_database(delivery.save, **{})


def delete_delivery():
    print()
    print_deliveries()
    delivery = input('which delivery: ')
    params = {
        'pk': delivery
    }
    change_database(Delivery.delete_by_id, **params)
