"""Endpoints responsables de gestionar features, likes y el agregado básico de comentarios."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, func, select
from sqlalchemy import or_

from datetime import datetime
from typing import Optional

from ..database import get_session
from ..models import Features, Likes, Comments
from ..oauth2 import get_current_user
from ..schemas import (
    CommentCollection,
    FeatureBase,
    FeatureCollection,
    FeatureOut,
    FeatureSummary,
    FeatureUpdate,
)

# Router dedicado a todo el CRUD de features más el agregado de likes y comentarios.
router = APIRouter(
    prefix="/features",
    tags=["Features"]
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=FeatureCollection,
    summary="Listar features",
    description=(
        "Devuelve un listado paginado de features. Permite buscar por título/descripcion, "
        "filtrar por usuario o limitar los resultados al propietario autenticado."
    ),
)
def get_features(
    db: Session = Depends(get_session),
    current_user: int = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str = "",
    user_id: Optional[int] = None,
    owner: Optional[str] = None,
):
    
    """Lista los features aplicando paginación, filtro por título/descripción, usuario y conteo de votos."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    # Query base que cuenta likes por feature mediante LEFT JOIN.
    query = (
        select(Features, func.count(Likes.user_id).label("likes"))
        .join(Likes, Likes.feature_id == Features.id, isouter=True)
        .limit(limit)
        .offset(skip)
        .group_by(Features.id)
        .order_by((func.count(Likes.user_id)).desc(), Features.id.desc()))
    
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
            "id": f.Features.id,
            "user_id": f.Features.user_id,
            "title": f.Features.title,
            "description": f.Features.description,
            #"published": f.Features.published,
            "created_at": f.Features.created_at,
            "updated_at": f.Features.updated_at,
            "likes": f.likes,
        }
        for f in features
    ]
    return {
        "meta": {"total": len(data), "limit": limit, "skip": skip},
        "data": data,
    }


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=FeatureSummary,
    summary="Consultar un feature",
    description="Recupera un feature propiedad del usuario autenticado junto con su conteo de likes.",
)
def get_feature(
    id: int,
    db: Session = Depends(get_session),
    current_user: int = Depends(get_current_user),
):
    """Devuelve un feature específico, verificando que pertenezca al usuario autenticado."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    feature = (
        db.exec(
            select(Features, func.count(Likes.user_id).label("likes"))
            .join(Likes, Likes.feature_id == Features.id, isouter=True)
            .group_by(Features.id)
            .where(Features.id == id)
        ).first()
    )

    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {id} was not found")

    # Normalizamos los campos para cumplir con FeatureSummary.
    return FeatureSummary(
        id=feature.Features.id,
        user_id=feature.Features.user_id,
        title=feature.Features.title,
        description=feature.Features.description,
        #published=feature.Features.published,
        created_at=feature.Features.created_at,
        updated_at=feature.Features.updated_at,
        likes=feature.likes,
)
    
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=FeatureBase,
    summary="Crear un feature",
    description="Registra un nuevo feature asociándolo automáticamente al usuario autenticado.",
    )
def create_feature(
    payload: FeatureBase,
    db: Session = Depends(get_session),
    current_user: int = Depends(get_current_user),
):
    """Crea un nuevo feature asociándolo automáticamente al usuario autenticado."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    new_feature = Features(**payload.model_dump(), user_id=current_user)
    db.add(new_feature)
    db.commit()
    db.refresh(new_feature)
    return new_feature


@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=FeatureOut,
    summary="Actualizar un feature",
    description="Permite editar un feature siempre que sea propiedad del usuario autenticado.",
)
def update_feature(
    id: int,
    payload: FeatureUpdate,
    db: Session = Depends(get_session),
    current_user: int = Depends(get_current_user),
):
    """Permite editar un feature siempre que sea propiedad del usuario autenticado."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    feature = db.get(Features, id)
    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {id} was not found")
    if feature.user_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    # Actualizamos los campos manualmente para mantener el control sobre cada atributo.
    feature.title = payload.title or feature.title
    feature.description = payload.description or feature.description
    #feature.published = payload.published or feature.published
    feature.updated_at = datetime.utcnow()

    db.add(feature)      # opcional, pero recomendable para dejar constancia del merge.
    db.commit()
    db.refresh(feature)  # refrescamos para devolver la versión persistida.
    
    return feature


@router.delete(
    "/{id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_feature(
    id: int,
    db: Session = Depends(get_session),
    current_user: int = Depends(get_current_user)
):
    """Elimina un feature existente si pertenece al usuario autenticado."""
    feature = db.get(Features, id)
    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {id} was not found")
    if feature.user_id != int(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    db.delete(feature)
    db.commit()
    return

@router.get(
    "/{id}/comments", 
    status_code=status.HTTP_200_OK, 
    response_model=CommentCollection
)
def get_comments(
    id: int,
    db: Session = Depends(get_session),
    current_user: int = Depends(get_current_user)
):
    """Devuelve los comentarios asociados a un feature existente."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    feature = db.get(Features, id)
    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {id} was not found")

    comments = db.exec(select(Comments)
                               .where(Comments.feature_id == id)
                               .order_by((Comments.created_at).desc())).all()
    
    data = [
        {
            "id": c.id,
            "user_id": c.user_id,
            "body": c.body,
            "created_at": c.created_at
        }
        for c in comments
    ]
    print(data)
    return {
        "meta": {"total": len(data)},
        "data": data
        }
