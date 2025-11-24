from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from ..database import get_session
from ..models import Users
from ..oauth2 import create_access_token, get_current_user
from ..schemas import Token, UserBase, UserCreate
from ..utils import get_password_hash, verify

# Router encargado de la autenticación basada en username/password -> JWT.
router = APIRouter(tags=["Authentication"],
                   prefix="/auth")

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserBase,
    summary="Registrar usuario",
    description="Crea un usuario nuevo.",
)
def register_user(payload: UserCreate, db: Session = Depends(get_session)):
    payload.password = get_password_hash(payload.password)
    user = Users(**payload.model_dump())
    if db.exec(select(Users).where(Users.email == user.email)).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    summary="Iniciar sesión",
    description="Valida credenciales vía formulario OAuth2 y devuelve un token JWT Bearer.",
)
def login_user(
    payload: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):
    # OAuth2PasswordRequestForm expone username/password y se envía como form-data.

    user = db.exec(select(Users).where(Users.email == payload.username)).first()
    if not user or not verify(payload.password, user.password):
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token}

@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserBase,
    summary="Perfil del usuario",
    description="Devuelve la información del usuario autenticado utilizando el token Bearer.",
)
def get_user(
    current_user: int = Depends(get_current_user), db: Session = Depends(get_session)
):
    """Devuelve la información del usuario; requiere autenticación."""
    user = db.get(Users, current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not authenticated")
    return user
