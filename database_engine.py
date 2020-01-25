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
    class Meta:
        database = db

class Item(pv.Model):
    name = pv.CharField(null=False)
    start_time = pv.DateTimeField(constraints=[pv.SQL('DEFAULT CURRENT_TIMESTAMP')])
    end_time = pv.DateTimeField(constraints=[pv.SQL('DEFAULT \'2100-01-01 09:00:00\'')])
    price = pv.FloatField(null=False)
    food = pv.BooleanField(null=False)
    class Meta:
        database = db
class Log_Item(pv.Model):
    access_type = pv.CharField(null=False)
    record_id = pv.IntegerField(null=False)
    class Meta:
        database = db

class Delivery(pv.Model):
    first_name = pv.CharField(null=False)
    last_name = pv.CharField(null=False)
    phone_number = pv.CharField(null=False, constraints=[pv.Check('phone_number REGEXP \'^([0-9]\{11\})$\'')])
    class Meta:
        database = db
class Log_Delivery(pv.Model):
    access_type = pv.CharField(null=False)
    record_id = pv.IntegerField(null=False)
    class Meta:
        database = db

class Client(pv.Model):
    id = pv.IntegerField(primary_key=True)
    first_name = pv.CharField(null=False)
    last_name = pv.CharField(null=False)
    phone_number = pv.CharField(null=False, constraints=[pv.Check('phone_number REGEXP \'^([0-9]\{11\})$\'')])
    age = pv.IntegerField(null=False)
    class Meta:
        database = db
class Log_Client(pv.Model):
    access_type = pv.CharField(null=False)
    record_id = pv.IntegerField(null=False)
    class Meta:
        database = db

class Address(pv.Model):
    client_id = pv.ForeignKeyField(Client, null=False)
    name = pv.CharField(null=False)
    address = pv.CharField(null=False)
    phone_number = pv.CharField(null=False, constraints=[pv.Check('phone_number REGEXP \'^([0-9]\{11\})$\'')])
    class Meta:
        database = db
class Log_Address(pv.Model):
    access_type = pv.CharField(null=False)
    record_id = pv.IntegerField(null=False)
    class Meta:
        database = db

class Receipt(pv.Model):
    price = pv.FloatField(null=False)
    address = pv.CharField()
    client_id = pv.ForeignKeyField(Client)
    market_id = pv.ForeignKeyField(Market)
    delivery_id = pv.ForeignKeyField(Delivery)
    class Meta:
        database = db
class Log_Receipt(pv.Model):
    access_type = pv.CharField(null=False)
    record_id = pv.IntegerField(null=False)
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
    record1_id = pv.IntegerField(null=False)
    record2_id = pv.IntegerField(null=False)
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
    record1_id = pv.IntegerField(null=False)
    record2_id = pv.IntegerField(null=False)
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
    db.connect()
    db.execute_sql("SET FOREIGN_KEY_CHECKS=0")
    for x in name_model.keys():
        create_table(x)
    add_triggers()
    db.execute_sql("SET FOREIGN_KEY_CHECKS=1")
    db.close()

def create_table(table_name):
    tables = db.get_tables()
    model = name_model[table_name]
    if table_name in tables:
        db.drop_tables([model])
    db.create_tables([model])
    # if table_name == 'client' or table_name == 'delivery' or table_name == 'address':
    #     db.execute_sql("ALTER TABLE %s ADD CONSTRAINT phone_number_check CHECK(phone_number REGEXP '^([0-9]\{11\})$')" % table_name)

def add_triggers():
    first_query =  ("Create Trigger {0}"
                  " AFTER {1} ON {2}"
                  " FOR EACH ROW"
                  " BEGIN"
                  " INSERT INTO log_{3}(access_type, record_id) VALUES(\'{4}\', {5}.id);"
                  " END")

    second_query = ("Create Trigger {0}"
                   " AFTER {1} ON {2}_{3}"
                   " FOR EACH ROW"
                   " BEGIN"
                   " INSERT INTO log_{4}_{5}(access_type, record1_id, record2_id) VALUES(\'{6}\', {7}.{8}_id, {9}.{10}_id);"
                   " END")
    tables = [
        'market',
        'item',
        'client',
        'address',
        'delivery',
        'receipt',
    ]
    for table in tables:
        db.execute_sql(first_query.format('insert_'+table, 'insert', table, table, 'insert', 'NEW'))
        db.execute_sql(first_query.format('update_'+table, 'update', table, table, 'update', 'OLD'))
        db.execute_sql(first_query.format('delete_'+table, 'delete', table, table, 'delete', 'OLD'))

    tables = [
        ('item', 'market'),
        ('item', 'receipt')
    ]
    for t1, t2 in tables:
        db.execute_sql(second_query.format('insert_'+t1+'_'+t2, 'insert', t1, t2, t1, t2, 'insert', 'NEW', t1, 'NEW', t2))
        db.execute_sql(second_query.format('update_'+t1+'_'+t2, 'update', t1, t2, t1, t2, 'update', 'OLD', t1, 'OLD', t2))
        db.execute_sql(second_query.format('delete_'+t1+'_'+t2, 'delete', t1, t2, t1, t2, 'delete', 'OLD', t1, 'OLD', t2))

def print_markets():
    print('-----------------')
    for x in Market.select().execute(None):
        print('{:>3} | {:<15} | {}'.format(x.id, x.name, x.active))
    print()    
    print(Market.select().count(None), 'market[s] found.')
    print('-----------------')
            
def print_deliveries():
    print('-----------------')
    for x in Delivery.select().execute(None):
        print('{:>3} | {:<30} | {}'.format(x.id, x.first_name + ' ' + x.last_name, x.phone_number))
    print()
    print(Delivery.select().count(None), 'delivery[s] found.')
    print('-----------------')

def change_database(function, **args):
    try:
        function(**args)
    except:
        print('something went wrong :(')
        return
    print('database updated :)')