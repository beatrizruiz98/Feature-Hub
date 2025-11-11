"""Create posts table

Revision ID: f38d69caddfa
Revises: 
Create Date: 2025-11-11 17:02:54.388408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
# Documentation https://alembic.sqlalchemy.org/en/latest/ops.html#ops
# Importo las clases para poder hacer el script
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, ForeignKey, Integer
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = 'f38d69caddfa'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('content', sa.String(200), nullable=False),
        sa.Column('published', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow)
        # Uso sqlalchemy para definir la clave foránea con ondelete="CASCADE" (No disponible en SQLMOdel)
        #user_id: int = Field(sa_column=Column(Integer, ForeignKey(
        #    "users.id", ondelete="CASCADE"),nullable=False))
        # Devuelve el usuario asociado a este post (usado para devolver el autor del post)
        #user: "Users" = Relationship(back_populates="post")
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
    pass
