import psycopg2 as psy


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

if __name__ == '__main__':
    print("complite!")