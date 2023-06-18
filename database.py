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

