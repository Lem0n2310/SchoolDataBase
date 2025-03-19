import psycopg2 as psy
from datetime import datetime


# сделать общий connect
def first_connect():
    connect = psy.connect(
        # Настройки подключения к базе данных
        host='79.174.88.238',
        port=15221,
        dbname='school_db',
        user='school',
        password='School1234*',
    )

    migrations = ""
    with open("migration.sql") as f:
        migrations = f.read()

    with connect.cursor() as cursor:
        for st in migrations.split(";"):
            if st.strip():
                cursor.execute(st.strip())
                print(f"Excecuted: {st.strip()}")
        connect.commit()


def get_connect():
    connect = psy.connect(
        # Настройки подключения к базе данных
        host='79.174.88.238',
        port=15221,
        dbname='school_db',
        user='school',
        password='School1234*',
    )


connect = get_connect()


def get_id(table):
    if table == "drivers":
        column = "driverId"
    elif table == "taxi":
        column = "orderId"
    else:
        column = "customerId"
    cursor = connect.cursor()
    cursor.execute(f"""select {column} from  uskov_klyuchnikov.{table};""")
    result = cursor.fetchall()
    cursor.close()
    table_ids = [row[0] for row in result]

    return table_ids


def get_table(table):
    cursor = connect.cursor()
    cursor.execute(
        f"""select * from uskov_klyuchnikov.{table};"""
    )

    result = cursor.fetchall()
    cursor.close()
    return result


def add_driver_customer(who, first_name, second_name):
    cursor = connect.cursor()
    who_id = who + "Id"
    who_table = who + "s"

    cursor.execute(f"""select {who_id} from uskov_klyuchnikov.{who_table} order by {who_id} desc limit 1;""")
    id = int(cursor.fetchall()[0][0])
    cursor.execute(f"""
        insert into uskov_klyuchnikov.{who_table} values ({id + 1},'{first_name}', '{second_name}');
        select {who_id} from uskov_klyuchnikov.{who_table} order by {who_id} desc limit 1;
    """)

    result = cursor.fetchall()[0][0]
    connect.commit()
    cursor.close()
    return f"Id: {result}"


def add_order(
        startDestination,
        endDestination,
        orderTime,
        carNumber,
        driverId,
        customerId,
        status
):
    orderTime = datetime.strptime(orderTime, "%Y-%m-%d %H:%M:%S.%f")
    cursor = connect.cursor()

    all_drivers = get_id("drivers")
    all_customers = get_id("customers")

    if not (driverId in all_drivers):
        print("Водителя с таким номером не существует")
    elif not (customerId in all_customers):
        print("Пассажира с таким номером не существует")
    elif not (customerId in all_customers and driverId in all_drivers):
        print("Ни водителя с таким номером не существует, ни пассажира с таким номером не существует")
    else:
        cursor.execute("""select orderId from uskov_klyuchnikov.taxi order by orderId desc limit 1;""")
        id = int(cursor.fetchall()[0][0])
        cursor.execute(f"""
                    insert into uskov_klyuchnikov.taxi values ({id + 1},
                    '{startDestination}', 
                    '{endDestination}', 
                    '{orderTime}', 
                    '{carNumber}',
                    '{driverId}',
                    '{customerId}',
                    '{status}'
                    );
                    select orderId from uskov_klyuchnikov.taxi order by orderId desc limit 1;
                """)
        result = cursor.fetchall()[0][0]
        connect.commit()
        cursor.close()
        return f"Id: {result}"


def update_order(orderId, status):
    cursor = connect.cursor()

    all_orders = get_id("taxi")
    if orderId in all_orders:
        cursor.execute(f"""update uskov_klyuchnikov.taxi set status = '{status}' where orderId = {orderId};""")
        print("Успешно")
        connect.commit()
    else:
        print("Заказа с таким номером не существует")
    cursor.close()


def delete(table, id):
    cursor = connect.cursor()
    permission = False
    if table == "drivers":
        column = "driverId"
        cursor.execute(f"""select driverId  from  uskov_klyuchnikov.taxi;""")
        result = cursor.fetchall()
        table_ids = [row[0] for row in result]
        if not (id in table_ids): permission = True
    elif table == "taxi":
        column = "orderId"
        permission = True
    else:
        column = "customerId"
        cursor.execute(f"""select customerId  from  uskov_klyuchnikov.taxi;""")
        result = cursor.fetchall()
        table_ids = [row[0] for row in result]
        if not (id in table_ids): permission = True

    if permission:
        cursor.execute(f"""delete from uskov_klyuchnikov.{table} where {column} = {id};""")
        connect.commit()
        cursor.close()
        print("Успешно")


if __name__ == '__main__':
    print(get_table("taxi"))
    connect.close()
