from sqlmodel import create_engine, Session

SQLMODEL_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"  # <-- mismo DB que psycopg2

engine = create_engine(SQLMODEL_DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
