import peewee as pv
import datetime as dt

db = pv.MySQLDatabase(database='sitado', user='sitado_admin', password='123456', host='localhost', port=3306)

class Market(pv.Model):
    name = pv.CharField(null=False)
    active = pv.BooleanField(null=False)
    class Meta:
        database = db
class Log_Market(pv.Model):
    access_type = pv.CharField(null=False)
    record_id = pv.IntegerField(null=False)
    logged_at = pv.DateTimeField(constraints=[pv.SQL('DEFAULT CURRENT_TIMESTAMP')])
    class Meta:
        database = db

class Item(pv.Model):
    name = pv.CharField()
    start_time = pv.DateTimeField(constraints=[pv.SQL('DEFAULT CURRENT_TIMESTAMP')])
    end_time = pv.DateTimeField(constraints=[pv.SQL('DEFAULT \'2100-01-01 09:00:00\'')])
    price = pv.FloatField()
    food = pv.BooleanField()
    class Meta:
        database = db
class Log_Item(pv.Model):
    access_type = pv.CharField(null=False)
    record_id = pv.IntegerField(null=False)
    logged_at = pv.DateTimeField(constraints=[pv.SQL('DEFAULT CURRENT_TIMESTAMP')])
    class Meta:
        database = db

class Delivery(pv.Model):
    national_code = pv.CharField(primary_key=True)
    first_name = pv.CharField(null=False)
    last_name = pv.CharField(null=False)
    phone_number = pv.CharField(null=False, constraints=[pv.Check('phone_number REGEXP \'^([0-9]\{11\})$\'')])
    class Meta:
        database = db
class Log_Delivery(pv.Model):
    access_type = pv.CharField(null=False)
    record_id = pv.IntegerField(null=False)
    logged_at = pv.DateTimeField(constraints=[pv.SQL('DEFAULT CURRENT_TIMESTAMP')])
    class Meta:
        database = db

class Client(pv.Model):
    national_code = pv.CharField(primary_key=True)
    first_name = pv.CharField(null=False)
    last_name = pv.CharField(null=False)
    phone_number = pv.CharField(null=False, constraints=[pv.Check('phone_number REGEXP \'^([0-9]\{11\})$\'')])
    birth_year = pv.IntegerField(null=False)
    class Meta:
        database = db
class Log_Client(pv.Model):
    access_type = pv.CharField(null=False)
    record_id = pv.IntegerField(null=False)
    logged_at = pv.DateTimeField(constraints=[pv.SQL('DEFAULT CURRENT_TIMESTAMP')])
    class Meta:
        database = db

class Address(pv.Model):
    national_code_id = pv.ForeignKeyField(Client, null=False, on_delete='CASCADE')
    name = pv.CharField(null=False)
    address = pv.CharField(null=False)
    phone_number = pv.CharField(null=False, constraints=[pv.Check('phone_number REGEXP \'^([0-9]\{11\})$\'')])
    class Meta:
        primary_key = pv.CompositeKey('national_code_id', 'name')
        database = db
class Log_Address(pv.Model):
    access_type = pv.CharField(null=False)
    national_code_id = pv.IntegerField(null=False)
    name = pv.CharField(null=False)
    logged_at = pv.DateTimeField(constraints=[pv.SQL('DEFAULT CURRENT_TIMESTAMP')])
    class Meta:
        database = db

class Receipt(pv.Model):
    price = pv.FloatField(null=False)
    address = pv.CharField(null=True)
    client_id = pv.ForeignKeyField(Client, null=True)
    market_id = pv.ForeignKeyField(Market, null=True)
    delivery_id = pv.ForeignKeyField(Delivery, null=True)
    at = pv.DateTimeField(constraints=[pv.SQL('DEFAULT CURRENT_TIMESTAMP')])
    class Meta:
        database = db
class Log_Receipt(pv.Model):
    access_type = pv.CharField(null=False)
    record_id = pv.IntegerField(null=False)
    logged_at = pv.DateTimeField(constraints=[pv.SQL('DEFAULT CURRENT_TIMESTAMP')])
    class Meta:
        database = db

class Item_Receipt(pv.Model):
    item_id = pv.ForeignKeyField(Item)
    receipt_id = pv.ForeignKeyField(Receipt)
    class Meta:
        primary_key = pv.CompositeKey('item_id', 'receipt_id')
        database = db
class Log_Item_Receipt(pv.Model):
    access_type = pv.CharField(null=False)
    item_id = pv.IntegerField(null=False)
    receipt_id = pv.IntegerField(null=False)
    logged_at = pv.DateTimeField(constraints=[pv.SQL('DEFAULT CURRENT_TIMESTAMP')])
    class Meta:
        database = db

class Item_Market(pv.Model):
    item_id = pv.ForeignKeyField(Item)
    market_id  = pv.ForeignKeyField(Market)
    class Meta:
        primary_key = pv.CompositeKey('item_id', 'market_id')
        database = db
class Log_Item_Market(pv.Model):
    access_type = pv.CharField(null=False)
    item_id = pv.IntegerField(null=False)
    market_id = pv.IntegerField(null=False)
    logged_at = pv.DateTimeField(constraints=[pv.SQL('DEFAULT CURRENT_TIMESTAMP')])
    class Meta:
        database = db

name_model = {
    'market': Market,
    'item': Item,
    'client': Client,
    'address': Address,
    'delivery': Delivery,
    'receipt': Receipt,
    'item_receipt': Item_Receipt,
    'item_market': Item_Market,

    'log_market': Log_Market,
    'log_item': Log_Item,
    'log_client': Log_Client,
    'log_address': Log_Address,
    'log_delivery': Log_Delivery,
    'log_receipt': Log_Receipt,
    'log_item_receipt': Log_Item_Receipt,
    'log_item_market': Log_Item_Market
}

def setup_database():
    query = "DROP EVENT IF EXISTS second_event"
    db.connect()
    db.execute_sql("SET FOREIGN_KEY_CHECKS=0")
    db.execute_sql(query)
    for x in name_model.keys():
        create_table(x)
    add_triggers()
    add_store_precedure()
    db.execute_sql("SET FOREIGN_KEY_CHECKS=1")
    db.close()

def create_table(table_name):
    tables = db.get_tables()
    model = name_model[table_name]
    if table_name in tables:
        db.drop_tables([model])
    db.create_tables([model])

def add_triggers():
    first_query =  'Create Trigger {0} AFTER {1} ON {2} FOR EACH ROW BEGIN INSERT INTO log_{2}(access_type, record_id, logged_at) VALUES(\'{1}\', {3}, NOW()); END'
    second_query = 'Create Trigger {0} AFTER {1} ON {2} FOR EACH ROW BEGIN INSERT INTO log_{2}(access_type, {3}, {4}, logged_at) VALUES(\'{1}\', {5}, {6}, NOW()); END'
    tables = [
        ('market', 'id'),
        ('item', 'id'),
        ('client', 'national_code'),
        ('delivery', 'national_code'),
        ('receipt', 'id'),
    ]
    for t in tables:
        db.execute_sql(first_query.format('insert_'+t[0], 'insert', t[0], 'NEW.'+t[1]))
        db.execute_sql(first_query.format('update_'+t[0], 'update', t[0], 'OLD.'+t[1]))
        db.execute_sql(first_query.format('delete_'+t[0], 'delete', t[0], 'OLD.'+t[1]))
    tables = [
        ('item_market', 'item_id', 'market_id'),
        ('item_receipt', 'item_id', 'receipt_id'),
        ('address', 'national_code_id', 'name')
    ]
    for t in tables:
        db.execute_sql(second_query.format('insert_'+t[0], 'insert', t[0], t[1], t[2], 'NEW.'+t[1], 'NEW.'+t[2]))
        db.execute_sql(second_query.format('update_'+t[0], 'update', t[0], t[1], t[2], 'OLD.'+t[1], 'OLD.'+t[2]))
        db.execute_sql(second_query.format('delete_'+t[0], 'delete', t[0], t[1], t[2], 'OLD.'+t[1], 'OLD.'+t[2]))


def add_store_precedure():
    query = ("CREATE EVENT `second_event`"
            " ON SCHEDULE EVERY 10 SECOND STARTS '2015-09-01 00:00:00'"
            " ON COMPLETION PRESERVE"
            " DO BEGIN"
            " delete from log_address"
            " where TIMESTAMPDIFF(SECOND, logged_at, now()) > 20;"
            " delete from log_client" 
            " where TIMESTAMPDIFF(SECOND, logged_at, now()) > 20;"
            " delete from log_delivery" 
            " where TIMESTAMPDIFF(SECOND, logged_at, now()) > 20;"
            " delete from log_item" 
            " where TIMESTAMPDIFF(SECOND, logged_at, now()) > 20;"
            " delete from log_item_market" 
            " where TIMESTAMPDIFF(SECOND, logged_at, now()) > 20;"
            " delete from log_item_receipt" 
            " where TIMESTAMPDIFF(SECOND, logged_at, now()) > 20;"
            " delete from log_market" 
            " where TIMESTAMPDIFF(SECOND, logged_at, now()) > 20;"
            " delete from log_receipt" 
            " where TIMESTAMPDIFF(SECOND, logged_at, now()) > 20;"
            " END")
    db.execute_sql(query)
             
def print_markets():
    print('-----------------\n')
    print('| {:>3} | {:<15} | {:<6} |'.format('id', 'name', 'active'))
    for x in Market.select().execute(None):
        print('| {:>3} | {:<15} | {:<6} |'.format(x.id, x.name, x.active))
    print()
    x = Market.select().count(None)
    print(x, 'market[s] found.')
    print('-----------------')
    return x
            
def print_deliveries():
    print('-----------------\n')
    print('| {:>15} | {:<30} | {:<11} |'.format('national code', 'name', 'phone'))
    for x in Delivery.select().execute(None):
        print('| {:>15} | {:<30} | {:<11} |'.format(x.national_code, x.first_name + ' ' + x.last_name, x.phone_number))
    print()
    x = Delivery.select().count(None)
    print(x, 'delivery[s] found.')
    print('-----------------')
    return x

def print_items():
    print('-----------------\n')
    print('| {:>3} | {:<15} | {:>5} | {:<5} |'.format('id', 'name', 'price', 'food?'))
    for x in Item.select().where(Item.end_time == '2100-01-01 09:00:00').execute(None):
        print('| {:>3} | {:<15} | {:>5} | {:<5} |'.format(x.id, x.name, x.price, x.food))
    print()
    x = Item.select().where(Item.end_time == '2100-01-01 09:00:00').count(None)
    print(x, 'item[s] found.')
    print('-----------------')
    return x

def print_foods():
    print('-----------------\n')
    print('| {:>3} | {:<15} | {:>5} | {:<11} |'.format('id', 'name', 'price', 'food'))
    for x in Item.select().where(Item.food, Item.end_time == '2100-01-01 09:00:00').execute(None):
        print('| {:>3} | {:<15} | {:>5} | {:<11} |'.format(x.id, x.name, x.price, x.food))
    print()
    x = Item.select().where(Item.food, Item.end_time == '2100-01-01 09:00:00').count(None)
    print(x, 'food[s] found.')
    print('-----------------')
    return x

def print_materials():
    print('-----------------\n')
    print('| {:>3} | {:<15} | {:<5} |'.format('id', 'name', 'price'))
    for x in Item.select().where(not Item.food, Item.end_time == '2100-01-01 09:00:00').execute(None):
        print('| {:>3} | {:<15} | {:>5} |'.format(x.id, x.name, x.price))
    print()
    x = Item.select().where(not Item.food, Item.end_time == '2100-01-01 09:00:00').count(None)
    print(x, 'material[s] found.')
    print('-----------------')
    return x

def print_clients():
    print('-----------------\n')
    print('| {:>15} | {:<30} | {:<11} | {:<3} |'.format('national code', 'name', 'phone', 'age'))
    for x in Client.select().execute(None):
        print('| {:>15} | {:<30} | {:<11} | {:<3} |'.format(x.national_code, x.first_name + ' ' + x.last_name, x.phone_number, dt.datetime.now().year - x.birth_year))
    print()
    x = Client.select().count(None)
    print(x, 'client[s] found.')
    print('-----------------')
    return x

def print_addresses(client):
    print('-----------------\n')
    print('| {:<15} | {:<30} | {:<11} |'.format('name', 'address', 'phone'))
    for x in Address.select().where(Address.national_code_id == client).execute(None):
        print('| {:<15} | {:<30} | {:<11} |'.format(x.name, x.address, x.phone_number))
    print()
    x = Address.select().where(Address.national_code_id == client).count(None)
    print(x, 'address\'[s] found.')
    print('-----------------')
    return x

def print_market_materials(market):
    print('-----------------\n')
    print('| {:>3} | {:<15} | {:>5} |'.format('id', 'name', 'price'))
    for x in Item.select().join(Item_Market).where(Item_Market.market_id == market).execute(None):
        print('| {:>3} | {:<15} | {:>5} |'.format(x.id, x.name, x.price))
    print()
    x = Item.select().join(Item_Market).where(Item_Market.market_id == market).count(None)
    print(x, 'material[s] found.')
    print('-----------------')
    return x

def print_client_reports(client):
    query = ("SELECT receipt.id, receipt.address, item.name, item.price"
            " FROM receipt"
            " INNER JOIN item_receipt ON receipt.id = item_receipt.receipt_id"
            " INNER JOIN item ON item.id = item_receipt.item_id"
            " WHERE receipt.client_id = " + str(client))
    query2 = ("SELECT item.name, count(*) as times"
              " FROM receipt"
              " INNER JOIN item_receipt ON receipt.id = item_receipt.receipt_id"
              " INNER JOIN item ON item.id = item_receipt.item_id"
              " WHERE receipt.client_id = '" + str(client) + "' GROUP BY item.food ORDER BY times DESC LIMIT 1")
    fav_food = None
    for x in db.execute_sql(query2):
        fav_food = x[0]
    
    print('-----------------\n')
    print('| {:>3} | {:<50} | {:<10} | {:<10} |'.format('id', 'address', 'food name', 'food price'))
    count, total = 0, 0
    for x in db.execute_sql(query):
        print('| {:>3} | {:<50} | {:<10} | {:<10} |'.format(str(x[0]), str(x[1]), str(x[2]), str(x[3])))
        total += x[3]
        count += 1
    
    print()
    x = count
    print(x, 'item[s] found')
    print('total cost:', total)
    print('favorite food:', fav_food)
    print('-----------------')
    return x

def print_manager_reports():
    total = 0
    print('-----------------\n')
    query = ("SELECT receipt.id, item.price, receipt.address, item.food"
            " FROM receipt" 
            " INNER JOIN item_receipt ON receipt.id = item_receipt.receipt_id"
            " INNER JOIN item ON item.id = item_receipt.item_id"
            " WHERE (receipt.at > DATE_SUB(now(), INTERVAL 1 DAY));")

    print('| {:>3} | {:<7} | {:<50} | {:<10} |'.format('id', 'price', 'address', 'is food'))
    query_result = db.execute_sql(query)
    for x in query_result:
        print('| {:>3} | {:<7} | {:<50} | {:<10} |'.format(x[0], x[1], str(x[2]), x[3]))
        if x[3]:
            total += x[1]
        else:
            total -= x[1]
    print()
    print('total profit:', total)
    print('-----------------')

def print_tables_list():
    print('-----------------')
    print('1 - client')
    print('2 - address')
    print('3 - delivery')
    print('4 - item')
    print('5 - market')
    print('6 - receipt')
    print('7 - item_market')
    print('8 - item_receipt')
    print('-----------------')

def calculate_total_price(foods):
    total = 0
    for i in foods:
        x = int(i)
        total += Item.get_by_id(x).price
    return total

def change_database(function, **args):
    # function(**args)
    
    try:
        function(**args)
    except Exception as e:
        print(e)
        print('something went wrong :(')
        return False
    print('database updated :)')
    return True

if __name__ == '__main__':
    setup_database()
    # pass
