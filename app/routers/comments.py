from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, func, select
from datetime import datetime
from typing import Optional

from ..database import get_session
from ..schemas import CommentCreate, CommentOut
from ..oauth2 import get_current_user
from ..models import Comments, Features

# Router dedicado a todo el CRUD de features más el agregado de votos.
router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.get("/{id}", status_code = status.HTTP_200_OK, response_model=CommentOut)
def get_comment(id: int,
                db: Session = Depends(get_session),
                current_user: str = Depends(get_current_user)):

    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    comment = db.get(Comments, id)
    return comment

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=CommentOut)
def create_comment(payload: CommentCreate,
                db: Session = Depends(get_session),
                current_user: str = Depends(get_current_user)):

    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    feature = db.get(Features, payload.feature_id)

    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {id} was not found")

    new_comment = Comments(**payload.model_dump(), user_id=int(current_user))
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int,
                db: Session = Depends(get_session),
                current_user: str = Depends(get_current_user)):
    """Elimina un comentario existente si pertenece al usuario autenticado."""
    comment = db.get(Comments, id)
    if not comment:
        raise HTTPException(status_code=404, detail=f"Comment {id} was not found")
    if comment.user_id != int(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    db.delete(comment)
    db.commit()
    return



    
    


