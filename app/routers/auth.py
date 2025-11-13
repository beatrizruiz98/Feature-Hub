from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from ..database import get_session
from ..models import Users
from ..oauth2 import create_access_token, get_current_user
from ..utils import verify, get_password_hash
from ..schemas import UserBase, UserCreate, Token

# Router encargado de la autenticación basada en username/password -> JWT.
router = APIRouter(tags=["Authentication"],
                   prefix="/auth")

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserBase)
def register_user(payload: UserCreate, db: Session = Depends(get_session)):
    """Registra un usuario nuevo tras validar email y almacenar la contraseña cifrada."""
    payload.password = get_password_hash(payload.password)
    user = Users(**payload.model_dump())
    if db.exec(select(Users).where(Users.email == user.email)).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    db.add(user, id)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=Token)
def login_user(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """Valida credenciales recibidas vía formulario OAuth2 y emite un token JWT."""
    # OAuth2PasswordRequestForm tiene "username" y "password", no email, tenemos que modificarlo aunque username = email usuario a efectos prácticos
    # Esta request se hace desde form-data
    user = db.exec(select(Users).where(Users.email == payload.username)).first()
    # Si no existe el usuario
    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    # Verificar la contraseña
    if verify(payload.password, user.password) is False:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    else:
        access_token = create_access_token(data={"user_id": user.id})
        return {"access_token": access_token}

@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserBase)
def get_user(current_user: str = Depends(get_current_user),
             db: Session = Depends(get_session)):
    """Devuelve la información del usuario; requiere autenticación."""
    user = db.get(Users, int(current_user))
    if not user:
        raise HTTPException(status_code=404, detail=f"User not authenticated")
    return user
