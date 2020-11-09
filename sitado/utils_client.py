from database_engine import *

def show_clients():
    print()
    print_clients()
    input('press enter to return to main menu')


def show_addresses():
    print()
    print_clients()
    if Client.select().count(None) == 0:
        return
    client = int(input('which client: '))
    print_addresses(client)
    input('press enter to return to main menu')


def add_client():
    print()
    national_code = int(input('enter national code: '))
    first_name = input('enter first name: ')
    last_name = input('enter last name: ')
    phone_number = input('enter mobile phone number: ')
    birth_year = int(input('enter birth year: '))
    address = input('enter address (only 1, later you can add more): ')
    phone = input('enter home phone number: ')
    params1 = {
        'national_code': national_code,
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number,
        'birth_year': birth_year,
    }
    change_database(Client.create, **params1)
    params2 = {
        'national_code_id': national_code,
        'name': last_name,
        'address': address,
        'phone_number': phone
    }
    change_database(Address.create, **params2)


def update_client():
    print()
    print_clients()
    client = input('which client: ')
    first_name = input('enter first name: ')
    last_name = input('enter last name: ')
    phone_number = input('enter mobile phone number: ')
    birth_year = int(input('enter birth year: '))
    client = Client.get_by_id(client)
    client.first_name = first_name
    client.last_name = last_name
    client.phone_number = phone_number
    client.birth_year = birth_year
    change_database(client.save, **{})


def delete_client():
    print()
    print_clients()
    client = input('which client: ')
    params = {
        'pk': client
    }
    change_database(Client.delete_by_id, **params)


def add_address():
    print()
    print_clients()
    client = input('which client: ')
    address = input('enter new address: ')
    phone = int(input('enter home phone: '))
    name = input(
        'enter name of the address (unique between names of addresses of a person): ')
    params = {
        'national_code_id': client,
        'address': address,
        'phone_number': phone,
        'name': name
    }
    change_database(Address.create, **params)
