from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Features, Likes
from ..oauth2 import get_current_user
from ..schemas import Like

# Router con la lógica para crear o eliminar likes sobre features.
router = APIRouter(
    prefix="/likes",
    tags=["Likes"],
)


@router.post("/")
def like(payload: Like,
         db: Session = Depends(get_session),
         current_user: str = Depends(get_current_user)):
    """Crea un voto (dir=1) o lo elimina (dir=0) según la dirección solicitada."""
    new_like = Likes(**payload.model_dump(), user_id=int(current_user))
    like_query = db.exec(select(Likes).where(
        Likes.feature_id == new_like.feature_id,
        Likes.user_id == new_like.user_id
    )).first()

    feature_id_list = db.exec(select(Features.id)).all()
    if new_like.feature_id not in feature_id_list:
        # Si se intenta votar un feature que no existe, lanzamos error
        raise HTTPException(status_code=404, detail=f"Feature {new_like.feature_id} does not exist")

    if payload.dir == 1:
        if like_query:
            # Si el voto ya existe y se intenta crear otro, lanzamos error
            raise HTTPException(status_code=409, detail=f"User {new_like.user_id} already liked for feature {new_like.feature_id}")
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        raise HTTPException(status.HTTP_201_CREATED, detail="Like added successfully")
    if payload.dir == 0:
        if not like_query:
            raise HTTPException(status_code=400, detail=f"User did not like the feature {new_like.feature_id}")
        db.delete(like_query)
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Like removed successfully")
