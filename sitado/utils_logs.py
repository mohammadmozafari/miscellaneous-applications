from database_engine import *

def log_menu():
    print_tables_list()
    i = int(input('which table: '))
    if i == 1:
        first_group_logs(Log_Client)
    elif i == 2:
        second_group_logs('log_address')
    elif i == 3:
        first_group_logs(Log_Delivery)
    elif i == 4:
        first_group_logs(Log_Item)
    elif i == 5:
        first_group_logs(Log_Market)
    elif i == 6:
        first_group_logs(Log_Receipt)
    elif i == 7:
        second_group_logs('log_item_market')
    elif i == 8:
        second_group_logs('log_item_receipt')
    input('press enter to continue')


def first_group_logs(M):
    print('-----------------\n')
    print('| {:>3} | {:<15} | {:>10} | {:<20} |'.format('id', 'access type', 'record id', 'logged at'))
    for x in M.select().execute(None):
        print('| {:>3} | {:<15} | {:>10} | {:<20} |'.format(x.id, x.access_type, x.record_id, str(x.logged_at)))
    print()
    x = Item.select().count(None)
    print(x, 'item[s] found.')
    print('-----------------')
    return x

def second_group_logs(m):
    query = "SELECT * FROM " + m
    result = db.execute_sql(query)
    print('-----------------\n')
    print('| {:>3} | {:<15} | {:<12} | {:>12} | {:<20} |'.format('id', 'access type', 'record id 1', 'record id 2', 'logged at'))
    for x in result:
        print('| {:>3} | {:<15} | {:<12} | {:>12} | {:<20} |'.format(x[0], x[1], x[2], x[3], str(x[4])))
    print()
    x = Item.select().count(None)
    print(x, 'item[s] found.')
    print('-----------------')
    return x
