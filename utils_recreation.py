from database_engine import *

def build_table():
    db.execute_sql("SET FOREIGN_KEY_CHECKS=0")
    print_tables_list()
    i = int(input('which one: '))
    try:
        if i == 1:
            db.create_tables([Client])
        elif i == 2:
            db.create_tables([Address])
        elif i == 3:
            db.create_tables([Delivery])
        elif i == 4:
            db.create_tables([Item])
        elif i == 5:
            db.create_tables([Market])
        elif i == 6:
            db.create_tables([Receipt])
        elif i == 7:
            db.create_tables([Item_Market])
        elif i == 8:
            db.create_tables([Item_Receipt])
    except Exception as e:
        print(e)
        print('something went wrong :(')
        db.execute_sql("SET FOREIGN_KEY_CHECKS=1")
        return
    print('table built successfully')
    db.execute_sql("SET FOREIGN_KEY_CHECKS=1")

def remove_table():
    db.execute_sql("SET FOREIGN_KEY_CHECKS=0")
    print_tables_list()
    i = int(input('which one: '))
    try:
        if i == 1:
            db.drop_tables([Client])
        elif i == 2:
            db.drop_tables([Address])
        elif i == 3:
            db.drop_tables([Delivery])
        elif i == 4:
            db.drop_tables([Item])
        elif i == 5:
            db.drop_tables([Market])
        elif i == 6:
            db.drop_tables([Receipt])
        elif i == 7:
            db.drop_tables([Item_Market])
        elif i == 8:
            db.drop_tables([Item_Receipt])
    except Exception as e:
        print(e)
        print('something went wrong :(')
        db.execute_sql("SET FOREIGN_KEY_CHECKS=1")
        return
    print('table removed successfully')
    db.execute_sql("SET FOREIGN_KEY_CHECKS=1")
