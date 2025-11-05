from sqlmodel import create_engine, Session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"  # <-- mismo DB que psycopg2

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
