# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlmodel import Session, func, select

# from ..database import get_session
# from ..models import Features, Votes
# from ..oauth2 import get_current_user
# from ..schemas import FeatureBase, FeatureCreate, FeatureOut, FeatureUpdated

# # Router dedicado a todo el CRUD de features más el agregado de votos.
# router = APIRouter(
#     prefix="/features",
#     tags=["Features"],
# )


# @router.get("/", status_code=status.HTTP_200_OK, response_model=list[FeatureOut])
# def get_features(db: Session = Depends(get_session),
#               limit: int = 10,
#               skip: int = 0,
#               search: str = ""):
#     """Lista los features aplicando paginación, filtro por título y conteo de votos."""
#     features = db.exec(
#         select(Features, func.count(Votes.user_id).label("votes"))
#         .join(Votes, Votes.feature_id == Feature.id, isouter=True)
#         .where(Features.title.contains(search))
#         .limit(limit)
#         .offset(skip)
#         .group_by(Features.id)
#         .order_by((func.count(Votes.user_id)).desc())
#     ).all()
#     return features


# @router.get("/{id}", status_code=status.HTTP_200_OK, response_model=FeaturesOut)
# def get_a_feature(id: int,
#                db: Session = Depends(get_session),
#                current_user: str = Depends(get_current_user)):
#     """Devuelve un feature específico, verificando que pertenezca al usuario autenticado."""
#     feature = db.exec(
#         select(Features, func.count(Votes.user_id).label("votes"))
#         .join(Votes, Votes.feature_id == Features.id, isouter=True)
#         .group_by(Features.id)
#         .where(Features.id == id)
#     ).first()

#     if not feature:
#         raise HTTPException(status_code=404, detail=f"Feature {id} was not found")
#     if feature.Features.user_id != int(current_user):
#         raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
#     print(feature)
#     return feature


# @router.feature("/", status_code=status.HTTP_201_CREATED, response_model=FeatureCreate)
# def create_feature(payload: FeatureBase,
#                 db: Session = Depends(get_session),
#                 current_user: str = Depends(get_current_user)):
#     """Crea un nuevo feature asociándolo automáticamente al usuario autenticado."""
#     if current_user is None:
#         raise HTTPException(status_code=401, detail="Invalid token payload")
#     new_feature = Features(**payload.model_dump(), user_id=int(current_user))
#     db.add(new_feature)
#     db.commit()
#     db.refresh(new_feature)
#     return new_feature


# @router.put("/{id}", status_code=status.HTTP_200_OK, response_model=FeatureBase)
# def update_feature(id: int,
#                 payload: FeatureBase,
#                 db: Session = Depends(get_session),
#                 current_user: str = Depends(get_current_user)):
#     """Permite editar un feature siempre que sea propiedad del usuario autenticado."""
#     feature = db.get(Features, id)
#     if not feature:
#         raise HTTPException(status_code=404, detail=f"Feature {id} was not found")
#     if feature.user_id != int(current_user):
#         raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
#     # Actualizamos los campos manualmente para mantener el control sobre cada atributo.
#     feature.title = payload.title
#     feature.content = payload.content
#     feature.published = payload.published

#     db.add(feature)      # opcional, pero recomendable para dejar constancia del merge.
#     db.commit()
#     db.refresh(feature)  # refrescamos para devolver la versión persistida.
#     return feature


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_feature(id: int,
#                 db: Session = Depends(get_session),
#                 current_user: str = Depends(get_current_user)):
#     """Elimina un feature existente si pertenece al usuario autenticado."""
#     feature = db.get(Features, id)
#     if not feature:
#         raise HTTPException(status_code=404, detail=f"Feature {id} was not found")
#     if feature.user_id != int(current_user):
#         raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
#     db.delete(feature)
#     db.commit()
#     return
