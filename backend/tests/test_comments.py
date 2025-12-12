from app.schemas import CommentCollection, CommentOut
import pytest

############# GET FEATURE COMMENTS ############

def test_get_comments_for_feature_successful(authorized_client, add_features, add_comments):
    """Prueba obtener comentarios para una feature con cliente autorizado."""
    feature = add_features[0]
    res = authorized_client.get(f"/features/{feature.id}/comments/")                         
    collection = CommentCollection(**res.json())
    assert res.status_code == 200    
    assert collection.meta["total"] == 2

def test_get_comments_for_feature_unauthorized(client, add_features, add_comments):
    """Prueba obtener comentarios para una feature con cliente autorizado."""
    feature = add_features[0]
    res = client.get(f"/features/{feature.id}/comments/")                         
    assert res.status_code == 401    

def test_get_comments_for_feature_nonexist(authorized_client, add_features, add_comments):
    """Prueba obtener comentarios para una feature con cliente autorizado."""
    res = authorized_client.get(f"/features/{12345678910}/comments/")                         
    assert res.status_code == 404    

############# POST A COMMENT ############

def test_create_comment_successful(authorized_client, add_features):
    """Prueba la creación de comentario con cliente autorizado."""
    feature = add_features[0]
    comment_data = {
        "feature_id": feature.id,
        "body": "This is a test comment"
    }
    res = authorized_client.post(f"/comments/", json=comment_data)                         
    created_comment = CommentOut(**res.json())
    assert res.status_code == 201    
    assert created_comment.body == comment_data['body']
    assert created_comment.feature_id == comment_data['feature_id'] 

@pytest.mark.parametrize("feature_id, body", [
    (None, "This is a test comment"), 
    (1, None),
    (None, None),])
def test_create_comment_invalid_data(authorized_client, add_features, feature_id, body):
    """Prueba la creación de comentario con datos inválidos."""
    comment_data = {
        "feature_id": feature_id,
        "body": body
    }
    res = authorized_client.post(f"/comments/", json=comment_data)                         
    assert res.status_code == 422

def test_create_comment_unauthorized(client, add_features):
    """Prueba la creación de comentario con cliente no autorizado."""
    feature = add_features[0]
    comment_data = {
        "feature_id": feature.id,
        "body": "This is a test comment"
    }
    res = client.post(f"/comments/", json=comment_data)                         
    assert res.status_code == 401

def test_create_comment_nonexist_feature(authorized_client, add_features):
    """Prueba la creación de comentario para una feature inexistente."""
    comment_data = {
        "feature_id": 12345678910,
        "body": "This is a test comment"
    }
    res = authorized_client.post(f"/comments/", json=comment_data)                         
    assert res.status_code == 404

############# GET A COMMENT ############
def test_get_a_comment_successful(authorized_client, add_comments):
    """Prueba el endpoint de obtención de un comentario con cliente autorizado."""
    comment = add_comments[0]
    res = authorized_client.get(f"/comments/{comment.id}/")
    fetched_comment = CommentOut(**res.json())
    assert res.status_code == 200
    assert fetched_comment.id == comment.id

def test_get_a_comment_unauthorized(client, add_comments):
    """Prueba el endpoint de obtención de un comentario con cliente no autorizado."""
    comment = add_comments[0]
    res = client.get(f"/comments/{comment.id}/")
    assert res.status_code == 401

def test_get_a_comment_forbidden(authorized_client, add_comments):
    """Prueba el endpoint de obtención de un comentario con cliente autorizado."""
    comment = add_comments[1]
    res = authorized_client.get(f"/comments/{comment.id}/")
    assert res.status_code == 403

def test_get_a_comment_notfound(authorized_client, add_comments):
    """Prueba el endpoint de obtención de un comentario con cliente autorizado."""
    res = authorized_client.get(f"/comments/{12345678910}/")
    assert res.status_code == 404

############# DELETE A COMMENT ############
def test_delete_a_comment_successful(authorized_client, add_comments):
    """Prueba el endpoint de eliminación de un comentario con cliente autorizado."""
    comment = add_comments[0]
    res = authorized_client.delete(f"/comments/{comment.id}/")
    assert res.status_code == 204

def test_delete_a_comment_unauthorized(client, add_comments):
    """Prueba el endpoint de eliminación de un comentario con cliente no autorizado."""
    comment = add_comments[0]
    res = client.delete(f"/comments/{comment.id}/")
    assert res.status_code == 401

def test_delete_a_comment_forbidden(authorized_client, add_comments):
    """Prueba el endpoint de eliminación de un comentario con cliente autorizado."""
    comment = add_comments[1]
    res = authorized_client.delete(f"/comments/{comment.id}/")
    assert res.status_code == 403

