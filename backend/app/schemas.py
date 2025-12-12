from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


class UserBase(BaseModel):
    """Campos comunes compartidos por varias respuestas relacionadas con usuarios."""
    
    id: Optional[int] = None
    name: str
    email: EmailStr
    created_at: Optional[datetime] = None


class UserCreate(UserBase):
    """Payload esperado cuando se crea un usuario a través de la API."""
    password: str
    

class Like(BaseModel):
    """Modelo para indicar si se crea o elimina un voto sobre un Feature."""

    feature_id: int
    dir: conint(ge=0, le=1)  # 1 for upvote, 0 for remove vote


class FeatureBase(BaseModel):
    """Campos básicos que definen el contenido de un feature."""
    
    title: str
    description: str
    #published: Optional[bool] = True

class FeatureUpdate(BaseModel):
    """Campos básicos que definen el contenido de un feature."""

    title: Optional[str] = None
    description: Optional[str] = None
    #published: Optional[bool] = True

class FeatureOut(FeatureBase):
    """Feature que se devuelve la información actualizada, enriquecido con información del autor."""

    id: Optional[int] = None
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class FeatureSummary(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    #published: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
    likes: int

class FeatureCollection(BaseModel):
    meta: dict
    data: list[FeatureSummary]


class Token(BaseModel):
    """Representa el token JWT emitido al autenticarse."""

    token_type: str = "Bearer"
    access_token: str


class TokenData(BaseModel):
    """Datos mínimos almacenados dentro del JWT (por ahora sólo el user_id)."""

    id: Optional[str] = None
    
    
class CommentCreate(BaseModel):
    """Datos para crear un comentario.""" 

    feature_id: int
    body: str 

class CommentOut(CommentCreate):
    """Datos para devolver de un comentario.""" 
   
    id: Optional[int] = None
    user_id: int
    created_at: Optional[datetime] = None
    
class CommentSummary(BaseModel):
    id: int
    user_id: int
    body: str 
    created_at: datetime

class CommentCollection(BaseModel):
    meta: dict
    data: list[CommentSummary]