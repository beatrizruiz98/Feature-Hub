from sqlmodel import create_engine, Session, SQLModel
from app.config import settings
from app.main import app
from app.models import Features
from app.database import get_session
from fastapi.testclient import TestClient
from app.oauth2 import create_access_token
import pytest
from pytest import fixture

# Cadena de conexión dinámica tomada del archivo .env con _test para la base de datos de pruebas.
SQLMODEL_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}_test"
# Motor de base de datos global para reutilizar conexiones en toda la aplicación.
engine = create_engine(SQLMODEL_DATABASE_URL, echo=False)

# Fixtures de pytest para configurar la base de datos de pruebas
@pytest.fixture
def session():
    SQLModel.metadata.drop_all(engine)    
    SQLModel.metadata.create_all(engine)
    """Provee una sesión nueva por petición y garantiza su cierre al finalizar."""
    with Session(engine) as test_session:
        yield test_session
        
# Fixture para el cliente de pruebas FastAPI que llama a session para la base de datos       
@pytest.fixture
def client(session):
    """Cliente de pruebas para simular peticiones HTTP a la aplicación FastAPI."""
    # Sobrescribe la dependencia de get_session para usar la sesión de pruebas
    def override_get_session():
        yield session
    # Funcion de sobrescritura de la dependencia (función de fastapi por defecto)
    # Sobreescribe get_session con test_session en todo el código
    """To override a dependency for testing, you put as a key the original dependency (a function), and as the value, your dependency override (another function)."""
    app.dependency_overrides[get_session] = override_get_session
    """You can use the TestClient class to test FastAPI applications without creating an actual HTTP and socket connection, just communicating directly with the FastAPI code."""
    with TestClient(app) as test_client:
        yield test_client
    # Limpia las dependencias sobrescritas después de las pruebas
    app.dependency_overrides.clear()

@pytest.fixture
def user(client):
    """Crea un usuario de prueba en la base de datos."""
    user_data = {
        "name": "Test User",
        "email": "test@test.com",
        "password": "password123"
    }
    res = client.post("/auth/register/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user

@pytest.fixture
def user2(client):
    """Crea otro usuario de prueba en la base de datos."""
    user_data = {
        "name": "Test User 2",
        "email": "test2@test.com",
        "password": "password123"
    }
    res = client.post("/auth/register/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user

@pytest.fixture
def token(user):
    """Genera un token de acceso JWT para el usuario de prueba."""
    return create_access_token(data={"user_id": user['id']})

@pytest.fixture
def authorized_client(client, token):
    """Cliente de pruebas con encabezado de autorización incluido."""
    client.headers.update({
        "Authorization": f"Bearer {token}"
    })
    return client

@pytest.fixture
# Aquí solo posteo a la BBDD, no me hace falta cliente
# Cuando implique interacciones con la base de datos usar session fixture
def add_features(user, user2, session):
    """Prueba el endpoint de crear features con cliente autorizado."""
    feature_sample = [
        {
            "title": "Test Feature",
            "description": "This is a test feature",
            "user_id": user['id']
        },
        {
            "title": "Another Feature",
            "description": "This is another test feature",
            "user_id": user['id']   
        },
        {
            "title": "Third Feature",
            "description": "This is the third test feature",
            "user_id": user2['id']
        }
    ]
    # Mapeo los datos de feature para ajustalo al model de la bbdd e incluir el user_id del usuario de prueba
    def create_feature_model(feature):
        return Features(**feature)
    # Creo los objetos Feature (mapeandolos con la lista) y los añado a la sesión
    sample = list(map(create_feature_model, feature_sample))
    session.add_all(sample)
    session.commit()
    for feature in sample:
        session.refresh(feature)
    return sample

@pytest.fixture
def add_comments(user, user2, add_features, session):
    """Agrega comentarios de prueba a las features existentes."""
    from app.models import Comments
    comment_sample = [
        {
            "body": "This is a test comment",
            "feature_id": add_features[0].id,
            "user_id": user['id']
        },
        {
            "body": "This is another test comment",
            "feature_id": add_features[0].id,
            "user_id": user2['id']
        },
        {
            "body": "This is a comment for the second feature",
            "feature_id": add_features[1].id,
            "user_id": user2['id']
        }
    ]
    def create_comment_model(comment):
        return Comments(**comment)
    sample = list(map(create_comment_model, comment_sample))
    session.add_all(sample)
    session.commit()
    for comment in sample:
        session.refresh(comment)
    return sample


