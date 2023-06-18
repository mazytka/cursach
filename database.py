from sqlalchemy import create_engine, text

engine = create_engine('mysql+pymysql://root:1234@127.0.0.1/парикмахерская')


def load_services_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from service"))
        services = []
        for row in result.all():
            services.append(row)
    return services

