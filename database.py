from sqlalchemy import create_engine, text
import secret_data as s


engine = create_engine(s.DB_CONNECTION_STRING)


def load_services_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from service"))
        services = []
        for row in result.all():
            services.append(row)
    return services


def load_service_from_db(id):  # функция выводит
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM service WHERE service.id={id}"))
        rows = []
        for row in result.all():
            rows.append(row._mapping)
        if len(rows) == 0:
            return None
        else:
            return row


def load_master_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text(f"select title, name, surname, patronymic from service INNER JOIN master ON (service.idmaster=master.id) where service.id = {id}"))
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
                                   f"service.id=types_of_services.id_service) where service.id={id}"))
        services = []
        for row in result.all():
            services.append(row)
    return services


def add_application_to_db():
    with engine.connect() as conn:
        query = text("INSERT INTO client (name, surname, patronymic, phone) VALUES ()")


