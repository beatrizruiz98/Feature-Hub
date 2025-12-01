from app import schemas, models
from sqlmodel import Session, select
import pytest
from app.main import app

def test_root(client):
    """Prueba el endpoint de salud raíz."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Server status": "Alive"}
    
def test_register(client):
    """Prueba el endpoint de registro de usuarios."""
    user_data = {
        "name": "Test User",
        "email": "test@test.com",
        "password": "password123"
    }
    res = client.post("/auth/register/", json=user_data)  
    print(res.json())
    assert res.status_code == 201
    new_user = schemas.UserBase(**res.json())
    assert new_user.email == user_data["email"]