"""Create user table

Revision ID: d7c9a21aaedc
Revises: f38d69caddfa
Create Date: 2025-11-11 21:10:48.878957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, ForeignKey, Integer
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = 'd7c9a21aaedc'
down_revision: Union[str, Sequence[str], None] = 'f38d69caddfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(100), nullable=False, unique=True),
        sa.Column('password', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow)
     )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
