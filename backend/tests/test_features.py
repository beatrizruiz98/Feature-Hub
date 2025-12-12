from app.schemas import FeatureCollection, FeatureBase, FeatureSummary
import pytest

############ GET TESTS ############

def test_get_all_features_successful(authorized_client, add_features):
    """Prueba el endpoint de obtención de features con cliente autorizado."""
    res = authorized_client.get("/features/")
    # Valido la respuesta contra el schema
    collection = FeatureCollection(**res.json())
    # Para acceder a la data sería collection.data[0].title
    assert res.status_code == 200
    assert collection.meta["total"] == 3
    
def test_get_features_unauthorized(client):
    """Prueba el endpoint de obtención de features con cliente no autorizado."""
    res = client.get("/features/")
    assert res.status_code == 401
    
def test_get_a_feature_successful(authorized_client, add_features):
    """Prueba el endpoint de obtención de una feature con cliente autorizado."""
    # Con add_features[0] accedo al primer feature creado en el fixture (la primera posición de la lista)
    res = authorized_client.get(f"/features/{add_features[0].id}/")
    feature = FeatureSummary(**res.json())
    assert res.status_code == 200
    assert feature.id == add_features[0].id
    
def test_get_a_feature_notfound(authorized_client, add_features):
    """Prueba el endpoint de obtención de una feature con cliente autorizado."""
    # Con add_features[0] accedo al primer feature creado en el fixture (la primera posición de la lista)
    res = authorized_client.get(f"/features/{12345678910}/")
    assert res.status_code == 404
    
def test_get_a_feature_unauthorized(client, add_features):
    """Prueba el endpoint de obtención de una feature con cliente no autorizado."""
    res = client.get(f"/features/{add_features[0].id}/")
    assert res.status_code == 401

############ POST TESTS ############

@pytest.mark.parametrize("title, description ,status_code", [
    ("Test Feature Title", "Test Description", 201),
    ("Another Feature Title", "Another Description", 201)
]) 
def test_post_a_feature_successful(authorized_client, title, description, status_code):
    """Prueba la creación de feature con cliente autorizado."""
    res = authorized_client.post("/features/", json={
        "title": title,
        "description": description
    })
    feature = FeatureBase(**res.json())
    assert res.status_code == status_code
    assert feature.title == title      

@pytest.mark.parametrize("title, description ,status_code", [ 
    (None, "Test description", 422),  # Título vacío
    ("Test Feature Title", None, 422),  # Descripción vacía
]) 
def test_post_a_feature_invalid_schema(authorized_client, title, description, status_code):
    """Prueba la creación de feature con cliente autorizado."""
    res = authorized_client.post("/features/", json={
        "title": title,
        "description": description
    })
    assert res.status_code == status_code
                       
def test_post_a_feature_unathorized(client):
    """Prueba la creación de feature con cliente no autorizado."""
    res = client.post("/features/", json={
        "title": "New Feature Posted",
        "description": "This is a new feature"
    })                            
    assert res.status_code == 401
    
############ DELETE TESTS ############

def test_delete_a_feature_successful(authorized_client, add_features):
    """Prueba la eliminación de feature con cliente autorizado."""
    feature = add_features[0]
    res = authorized_client.delete(f"/features/{feature.id}/")                         
    assert res.status_code == 204    
    
def test_delete_a_feature_forbidden(authorized_client, add_features):
    """Prueba la eliminación de feature con un usuario no owner de la feature."""
    feature = add_features[2]
    res = authorized_client.delete(f"/features/{feature.id}/")                         
    assert res.status_code == 403    
    
def test_delete_a_feature_notfound(authorized_client, add_features):
    """Prueba la eliminación de feature con cliente autorizado."""
    feature = add_features[0]
    res = authorized_client.delete(f"/features/{12345678910}/")                         
    assert res.status_code == 404    
    
def test_delete_a_feature_unathorized(client, add_features):
    """Prueba la eliminación de feature con cliente no autorizado."""
    feature = add_features[0]
    res = client.delete(f"/features/{feature.id}/")                         
    assert res.status_code == 401

############ PUT TESTS ############

def test_update_a_feature_successful(authorized_client, add_features):
    """Prueba la actualización de feature con cliente autorizado."""
    feature = add_features[0]
    updated_data = {
        "title": "Updated Feature Title",
        "description": "Updated Description"
    }
    res = authorized_client.put(f"/features/{feature.id}/", json=updated_data)                         
    updated_feature = FeatureBase(**res.json())
    assert res.status_code == 200    
    assert updated_feature.title == updated_data['title']
    assert updated_feature.description == updated_data['description']
    
def test_update_a_feature_unauthorized(client, add_features):
    """Prueba la actualización de feature con cliente autorizado."""
    feature = add_features[0]
    updated_data = {
        "title": "Updated Feature Title",
        "description": "Updated Description"
    }
    res = client.put(f"/features/{feature.id}/", json=updated_data)                         
    assert res.status_code == 401

def test_update_a_feature_forbiden(authorized_client, add_features):
    """Prueba la actualización de feature con cliente autorizado."""
    feature = add_features[2]
    updated_data = {
        "title": "Updated Feature Title",
        "description": "Updated Description"
    }
    res = authorized_client.put(f"/features/{feature.id}/", json=updated_data)                         
    assert res.status_code == 403

def test_update_a_feature_notfound(authorized_client, add_features):
    """Prueba la actualización de feature con cliente autorizado."""
    feature = add_features[0]
    updated_data = {
        "title": "Updated Feature Title",
        "description": "Updated Description"
    }
    res = authorized_client.put(f"/features/{12345678910}/", json=updated_data)                         
    assert res.status_code == 404