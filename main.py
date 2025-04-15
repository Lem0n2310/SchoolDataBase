import psycopg2 as psy
from psycopg2 import sql
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


connect = psy.connect(
    # Настройки подключения к базе данных
    host='79.174.88.238',
    port=15221,
    dbname='school_db',
    user='school',
    password='School1234*',
)


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
    who_table = who + "s"

    cursor.execute(f"""
            INSERT INTO uskov_klyuchnikov.{who_table} (firstName, secondName) 
            VALUES (%s, %s) RETURNING {who}Id;
        """, (first_name, second_name))

    result = cursor.fetchone()[0]
    connect.commit()
    cursor.close()
    return result


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

    if driverId not in all_drivers and customerId not in all_customers:
        print("Ни водителя с таким номером не существует, ни пассажира с таким номером не существует")
        return "Ни водителя с таким номером не существует, ни пассажира с таким номером не существует"
    elif driverId not in all_drivers:
        print("Водителя с таким номером не существует")
        return "Водителя с таким номером не существует"
    elif customerId not in all_customers:
        print("Пассажира с таким номером не существует")
        return "Пассажира с таким номером не существует"
    else:
        cursor.execute(f"""
            INSERT INTO uskov_klyuchnikov.taxi (startDestination, endDestination, orderTime, carNumber, driverId, customerId, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
            RETURNING orderId;
        """, (startDestination, endDestination, orderTime, carNumber, driverId, customerId, status))

        result = cursor.fetchone()[0]
        connect.commit()
        cursor.close()
        return f"Id: {result}"


def update_order(orderId, status):
    cursor = connect.cursor()

    all_orders = get_id("taxi")
    if orderId in all_orders:
        cursor.execute("""
            UPDATE uskov_klyuchnikov.taxi 
            SET status = %s 
            WHERE orderId = %s;
        """, (status, orderId))

        connect.commit()
        print("Успешно")
        return "Complete!"
    else:
        print("Заказа с таким номером не существует")
        return "Something went wrong..."
    cursor.close()


def delete_record(table, id):
    cursor = connect.cursor()
    permission = False
    column = None

    if table == "drivers":
        column = "driverId"
        cursor.execute(f"SELECT {column} FROM uskov_klyuchnikov.taxi;")
        result = cursor.fetchall()
        table_ids = [row[0] for row in result]
        if id not in table_ids:
            permission = True
    elif table == "taxi":
        column = "orderId"
        permission = True
    elif table == "customers":
        column = "customerId"
        cursor.execute(f"SELECT {column} FROM uskov_klyuchnikov.taxi;")
        result = cursor.fetchall()
        table_ids = [row[0] for row in result]
        if id not in table_ids:
            permission = True

    if permission:
        cursor.execute(f"DELETE FROM uskov_klyuchnikov.{table} WHERE {column} = %s;", (id,))
        connect.commit()
        print("Успешно")
    else:
        print("Запись с таким идентификатором не существует или удаление запрещено.")

    cursor.close()


if __name__ == '__main__':
    print(get_table("taxi"))
    connect.close()
