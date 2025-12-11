from app import schemas
from sqlmodel import Session, select
from app.main import app
from app.oauth2 import SECRET_KEY, ALGORITHM
import jwt
import pytest

# def test_root(client):
#     """Prueba el endpoint de salud raíz."""
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"Server status": "Alive"}
    
@pytest.mark.parametrize("email, name, password, status_code", [
                        ("", "test", "password123", 422), 
                        ("test.com", "test", "password123", 422),
                        ("test@test.com", None, "password123", 422),
                        ("test.com", "test", None, 422),
])                    
def test_register_failed(client, email, name, password, status_code):
    """Prueba el endpoint de registro de usuarios con datos inválidos."""
    res = client.post("/auth/register/", 
                      data={"username": email, "name": name, "password": password})
    assert res.status_code == status_code


def test_login_successful(user, client):
    """Prueba el endpoint de registro de usuarios."""
    res = client.post("/auth/login/" , 
                      data={"username": user['email'], "password": user['password']})
    token = schemas.Token(**res.json())
    payload = jwt.decode(token.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id = payload.get("user_id")
    # Compruebo que el id del token coincide con el id del usuario creado en el fixture
    assert id == user['id']
    assert token.token_type == "Bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
                        ("fake@test.com", "password123", 403), 
                        ("test@test.com", "wrongpassword", 403),
                        ("fake@test.com", "wrongpassword", 403),
                        ("", "password123", 403),
                        ("", "", 403),
                        ("test@test.com", "", 403)
])    
def test_login_failed(client, email, password, status_code):
    """Prueba el endpoint de login con credenciales incorrectas."""
    res = client.post("/auth/login/" , 
                      data={"username": email, "password": password})
    assert res.status_code == status_code