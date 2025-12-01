from sqlmodel import create_engine, Session, SQLModel
from app.config import settings
from app.main import app
from app.database import get_session
from fastapi.testclient import TestClient
import pytest
from pytest import fixture

# Cadena de conexión dinámica tomada del archivo .env.
SQLMODEL_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}_test"
# Motor de base de datos global para reutilizar conexiones en toda la aplicación.
engine = create_engine(SQLMODEL_DATABASE_URL, echo=False)

@fixture(scope="session")
def session():
    SQLModel.metadata.drop_all(engine)    
    SQLModel.metadata.create_all(engine)
    """Provee una sesión nueva por petición y garantiza su cierre al finalizar."""
    with Session(engine) as test_session:
        yield test_session
        
@pytest.fixture(scope="session")
def client(session):
    """Cliente de pruebas para simular peticiones HTTP a la aplicación FastAPI."""
    def override_get_session():
        yield session
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()