from sqlalchemy import create_engine, text
import secret_data as s
import time
import math

engine = create_engine(s.DB_CONNECTION_STRING, pool_pre_ping=True)


def load_services_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from service"))
        services = []
        for row in result.all():
            services.append(row)
    return services


def load_service_from_db(id):  # функция выводит
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM service WHERE id='{id}'"))
        rows = []
        for row in result.all():
            rows.append(row._mapping)
        if len(rows) == 0:
            return None
        else:
            return row


def load_master_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text(f"select master.id, title, name, surname, patronymic from service INNER JOIN master ON (service.idmaster=master.id) where service.id = '{id}'"))
        rows = []
        for row in result.all():
            rows.append(row._mapping)
        if len(rows) == 0:
            return None
        else:
            return row


def load_client_from_db():  # функция выводит всех клиентов
    with engine.connect() as conn:
        result = conn.execute(text('select * from client'))
        for i in result:
            return i


def load_service_price_from_db(id):  # функция выводит услуги предоставляемые мастером
    with engine.connect() as conn:
        result = conn.execute(text(f"select types, price from service INNER JOIN types_of_services ON ("
                                   f"service.id=types_of_services.id_service) where service.id='{id}'"))
        services = []
        for row in result.all():
            services.append(row)
    return services


def add_application_to_db(id_service, id_master, data):
    with engine.connect() as conn:
        query = text(f"INSERT INTO entry (idservice, full_name, idmaster, data) VALUES ( '{id_service}', '{data['full_name']}', '{id_master}', '{data['date']}' )")
        conn.execute(query)
        conn.commit()

def add_client_to_db(data):
    with engine.connect() as conn:
        query = text(
            f"INSERT INTO client (full_name, phone) VALUES ( '{data['full_name']}', '{data['phone']}')")
        conn.execute(query)
        conn.commit()


def add_user(email, password):
    with engine.connect() as conn:

        query1 = text(f"select count(useraname) as 'count' from user where useraname = '{email}'")
        result = conn.execute(query1)
        if result.fetchone()[0] > 0:
            return False

        query = text(f"INSERT INTO user (useraname, password) VALUES ('{email}', '{password}')")
        conn.execute(query)
        conn.commit()
    return True

def get_user(user_id):
    with engine.connect() as conn:
        query = text(f"select * from user where id = '{user_id}' LIMIT 1")
        result = conn.execute(query).fetchone()
        if not result:
            print('Пользователь не найден')
            return False
        return result


def get_user_by_email(email):
    with engine.connect() as conn:
        query = text(f"select * from user where useraname = '{email}' LIMIT 1")
        result = conn.execute(query).fetchone()
        if not result:
            print('Пользователь не найден')
            return False
        return result



