from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel


class Features(SQLModel, table=True):
    """Tabla principal para almacenar el contenido que crean los usuarios."""

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    published: bool = Field(default=True)
    # Uso SQLAlchemy para definir la clave foránea con ondelete="CASCADE" (no disponible en SQLModel).
    user_id: int = Field(sa_column=Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(nullable=True)


class Users(SQLModel, table=True):
    """Información básica de cada usuario registrado y autenticado."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Likes(SQLModel, table=True):
    """Tabla intermedia que relaciona usuarios con features votados."""

    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    )
    feature_id: int = Field(
        sa_column=Column(Integer, ForeignKey("features.id", ondelete="CASCADE"), primary_key=True)
    )
    
class Comments(SQLModel, table=True):
    """Tabla principal para almacenar el contenido que crean los usuarios."""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(sa_column=Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False))
    feature_id: int = Field(sa_column=Column(Integer, ForeignKey(
        "features.id", ondelete="CASCADE"), nullable=False))   
    body: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)