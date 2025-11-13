from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, func, select
from sqlalchemy import or_, and_
from datetime import datetime
from typing import Optional

from ..database import get_session
from ..models import Features, Likes
from ..oauth2 import get_current_user
from ..schemas import FeatureBase, FeatureUpdate, FeatureOut, FeatureCollection, FeatureSummary

# Router dedicado a todo el CRUD de features más el agregado de votos.
router = APIRouter(
    prefix="/features",
    tags=["Features"]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=FeatureCollection)
def get_features(db: Session = Depends(get_session),
                current_user: str = Depends(get_current_user),  
                limit: int = 10,
                skip: int = 0,
                search: str = "",
                user_id: Optional[str] = None,
                owner: Optional[str] = None):
    
    """Lista los features aplicando paginación, filtro por título/descripción, usuario y conteo de votos."""
    
    query = (
        select(Features, func.count(Likes.user_id).label("likes"))
        .join(Likes, Likes.feature_id == Features.id, isouter=True)
        .limit(limit)
        .offset(skip)
        .group_by(Features.id)
        .order_by((func.count(Likes.user_id)).desc())
        .order_by(Features.id.desc())
        )
    
    if search:
        pattern = f"%{search}%"
        query = query.where(
            or_(
                Features.title.ilike(pattern),
                Features.description.ilike(pattern),
            )
        )
       
    if owner == "me":
        query = query.where(Features.user_id == current_user)
    elif user_id is not None:
        query = query.where(Features.user_id == user_id)
        
    features = db.exec(query).all()

    data = [
        {
            "id": field.Features.id,
            "user_id": field.Features.user_id,
            "title": field.Features.title,
            "description": field.Features.description,
            "published": field.Features.published,
            "created_at": field.Features.created_at,
            "updated_at": field.Features.updated_at,
            "likes": field.likes,
        }
        for field in features
    ]
    return {
        "meta": {"total": len(data), "limit": limit, "skip": skip},
        "data": data,
    }


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=FeatureSummary)
def get_feature(id: int,
               db: Session = Depends(get_session),
               current_user: str = Depends(get_current_user)):
    """Devuelve un feature específico, verificando que pertenezca al usuario autenticado."""
    feature = db.exec(
        select(Features, func.count(Likes.user_id).label("likes"))
        .join(Likes, Likes.feature_id == Features.id, isouter=True)
        .group_by(Features.id)
        .where(Features.id == id)
    ).first()

    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {id} was not found")
    if feature.Features.user_id != int(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")

    print(feature)
    return {
        "id": feature.Features.id,
        "user_id": feature.Features.user_id,
        "title": feature.Features.title,
        "description": feature.Features.description,
        "published": feature.Features.published,
        "created_at": feature.Features.created_at,
        "updated_at": feature.Features.updated_at,
        "likes": feature.likes,
    }

    return data

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=FeatureBase)
def create_feature(payload: FeatureBase,
                db: Session = Depends(get_session),
                current_user: str = Depends(get_current_user)):
    """Crea un nuevo feature asociándolo automáticamente al usuario autenticado."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    new_feature = Features(**payload.model_dump(), user_id=int(current_user))
    db.add(new_feature)
    db.commit()
    db.refresh(new_feature)
    return new_feature


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=FeatureOut)
def update_feature(id: int,
                payload: FeatureUpdate,
                db: Session = Depends(get_session),
                current_user: str = Depends(get_current_user)):
    """Permite editar un feature siempre que sea propiedad del usuario autenticado."""
    feature = db.get(Features, id)
    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {id} was not found")
    if feature.user_id != int(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    # Actualizamos los campos manualmente para mantener el control sobre cada atributo.
    feature.title = payload.title or feature.title
    feature.description = payload.description or feature.description
    feature.published = payload.published or feature.published
    feature.updated_at = datetime.utcnow()

    db.add(feature)      # opcional, pero recomendable para dejar constancia del merge.
    db.commit()
    db.refresh(feature)  # refrescamos para devolver la versión persistida.
    
    return feature


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feature(id: int,
                db: Session = Depends(get_session),
                current_user: str = Depends(get_current_user)):
    """Elimina un feature existente si pertenece al usuario autenticado."""
    feature = db.get(Features, id)
    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {id} was not found")
    if feature.user_id != int(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    db.delete(feature)
    db.commit()
    return
