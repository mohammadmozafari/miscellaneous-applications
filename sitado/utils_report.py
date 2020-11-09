from database_engine import *

def show_client_reports():
    print()
    if print_clients() == 0:
        return
    client = int(input('which client: '))
    print_client_reports(client)
    input('press enter to return to the main menu')


def show_manager_reports():
    print()
    print_manager_reports()
    input('press enter to return to the main menu')
