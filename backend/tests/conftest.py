from sqlmodel import create_engine, Session, SQLModel
from app.config import settings
from app.main import app
from app.database import get_session
from fastapi.testclient import TestClient
import pytest
from pytest import fixture

# Cadena de conexión dinámica tomada del archivo .env con _test para la base de datos de pruebas.
SQLMODEL_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}_test"
# Motor de base de datos global para reutilizar conexiones en toda la aplicación.
engine = create_engine(SQLMODEL_DATABASE_URL, echo=False)

# Fixtures de pytest para configurar la base de datos de pruebas
@fixture(scope="session")
def session():
    SQLModel.metadata.drop_all(engine)    
    SQLModel.metadata.create_all(engine)
    """Provee una sesión nueva por petición y garantiza su cierre al finalizar."""
    with Session(engine) as test_session:
        yield test_session
        
# Fixture para el cliente de pruebas FastAPI que llama a session para la base de datos       
@pytest.fixture(scope="session")
def client(session):
    """Cliente de pruebas para simular peticiones HTTP a la aplicación FastAPI."""
    # Sobrescribe la dependencia de get_session para usar la sesión de pruebas
    def override_get_session():
        yield session
    # Funcion de sobrescritura de la dependencia 
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()