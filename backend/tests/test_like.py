def test_like_feature_successful(authorized_client, add_features):
    """Prueba el endpoint de dar like a un feature."""
    feature = add_features[2]
    res = authorized_client.post("/likes/", json={"feature_id": feature.id, "dir": 1})
    assert res.status_code == 201
    
def test_like_feature_twice(authorized_client, add_features):
    """Prueba que dar like a un feature dos veces falla."""
    feature = add_features[2]
    res1 = authorized_client.post("/likes/", json={"feature_id": feature.id, "dir": 1})
    res2 = authorized_client.post("/likes/", json={"feature_id": feature.id, "dir": 1})
    assert res2.status_code == 409  

def test_unlike_feature_successful(authorized_client, add_features):
    """Prueba el endpoint de quitar like a un feature."""
    feature = add_features[2]
    # Primero doy like
    res1 = authorized_client.post("/likes/", json={"feature_id": feature.id, "dir": 1})
    assert res1.status_code == 201
    # Luego quito el like
    res2 = authorized_client.post("/likes/", json={"feature_id": feature.id, "dir": 0})
    assert res2.status_code == 200

def test_unlike_feature_not_liked(authorized_client, add_features):
    """Prueba que quitar like a un feature no gustado falla."""
    feature = add_features[2]
    res = authorized_client.post("/likes/", json={"feature_id": feature.id, "dir": 0})
    assert res.status_code == 400

def test_like_nonexistent_feature(authorized_client):
    """Prueba que dar like a un feature inexistente falla."""
    res = authorized_client.post("/likes/", json={"feature_id": 12345678910, "dir": 1})
    assert res.status_code == 404

def test_like_feature_unauthorized(client, add_features):
    """Prueba el endpoint de dar like a un feature."""
    feature = add_features[2]
    res = client.post("/likes/", json={"feature_id": feature.id, "dir": 1})
    assert res.status_code == 401