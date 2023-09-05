import psycopg2

# Функция создания таблиц
def create_table(cur, text):
    cur.execute(f'CREATE TABLE IF NOT EXISTS {text}')
    conn.commit()
# Функция добавления пользователей
def add_data_peoples(cur, names, surnames, emails):
    cur.execute("""INSERT INTO peoples (name, surname, email)
                                    VALUES (%s, %s, %s) RETURNING id, name, surname, email;""",
                (names, surnames, emails))
    print(cur.fetchone())
# Функция добавления номеров и их связи с пользователями
def add_data_phones(cur, phones, names_id, phones_id):
    cur.execute("""INSERT INTO phone (phone)
                                        VALUES (%s) RETURNING id, phone;""",
                (phones, ))
    print(cur.fetchone())
    cur.execute("""INSERT INTO peoples_phone (name_id, phone_id)
                                            VALUES (%s, %s) RETURNING id, name_id, phone_id;""",
                (names_id, phones_id))
    print(cur.fetchone())
# Функция обновления данных пользователя
def update_data_peoples(cur, names, surnames, emails, update_id):
    cur.execute("""
            UPDATE peoples SET name=%s, surname=%s, email=%s WHERE id=%s;
            """, (names, surnames, emails, update_id))
    cur.execute("""
            SELECT * FROM peoples;
            """)
    print(cur.fetchall())

# Функция обновления номера телефона
def update_data_phone(cur, phone_old, phone_new):
    cur.execute("""
                    UPDATE phone SET phone=%s WHERE phone=%s;
                    """, (phone_new, phone_old))
    cur.execute("""
                SELECT * FROM phone;
                """)
    print(cur.fetchall())

# Функция удаления номера телефона
def delete_data_phone(cur, phone_id):
    cur.execute("""
                DELETE FROM peoples_phone WHERE phone_id=%s;
                """, (phone_id,))
    cur.execute("""
            DELETE FROM phone WHERE id=%s;
            """, (phone_id,))
    cur.execute("""
            SELECT * FROM phone;
            """)
    print(cur.fetchall())

# Функция полного удаления клиента
def delete_data_peoples(cur, peoples_id):
    cur.execute("""
                    SELECT * FROM peoples_phone;
                    """)
    data = cur.fetchall()
    cur.execute("""
                DELETE FROM peoples_phone WHERE name_id=%s;
                """, (peoples_id,))
    cur.execute("""
            DELETE FROM peoples WHERE id=%s;
            """, (peoples_id,))
    for i in data:
        if i[1] == peoples_id:
            cur.execute("""
                        DELETE FROM phone WHERE id=%s;
                        """, (i[0],))
    cur.execute("""
            SELECT * FROM peoples;
            """)
    print(cur.fetchall())
    cur.execute("""
                SELECT * FROM phone;
                """)
    print(cur.fetchall())
    cur.execute("""
                    SELECT * FROM peoples_phone;
                    """)
    print(cur.fetchall())

def search_peoples(cur, text):
    cur.execute("""
            SELECT name, surname, email, phone FROM peoples ps 
            join peoples_phone pp on pp.name_id=ps.id
            join phone p on pp.phone_id=p.id
            where 
            name=%s or surname=%s or email=%s or phone=%s;
            """, (text, text, text, text))
    print(f'это тут {cur.fetchall()}')

# Основная часть программы
with psycopg2.connect(database='test', user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:
        try:
            cur.execute("""
                DROP TABLE peoples_phone;
                DROP TABLE peoples;
                DROP TABLE phone;
                """)
        except:
            pass
        # Создаем таблицы
        create_table(cur, """
                    peoples(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(40),
                        surname VARCHAR(40),
                        email VARCHAR(40)
                );
                """)
        create_table(cur, """
                    phone(
                        id SERIAL PRIMARY KEY,
                        phone VARCHAR(40)
                );
                """)
        create_table(cur, """
                    peoples_phone(
                        id SERIAL PRIMARY KEY,
                        name_id INT NOT NULL REFERENCES peoples(id),
                        phone_id INT NOT NULL REFERENCES phone(id)
                );
                """)

        '''Все функции'''
        # add_data_peoples(cur, "Vladislav", 'Ivanishchev', 'Aloverdoz1135852@gmail.com')
        # add_data_peoples(cur, "Oleg", 'Zverev', 'God@gmail.com')
        # add_data_phones(cur, '89996502948', 1, 1)
        # add_data_phones(cur, '89996502949', 1, 2)
        # add_data_phones(cur, '89998887766', 2, 3)
        # update_data_peoples(cur, 'Ivan', 'Grozniy', 'groza@mail.ru', 1)
        # update_data_phone(cur, '89996502948', '89996502950')
        # delete_data_phone(cur, 1)
        # delete_data_peoples(cur, 1)
        # search_peoples(cur, 'Oleg')





