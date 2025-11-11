"""Add foreign-key to post table

Revision ID: 8a83602457d3
Revises: d7c9a21aaedc
Create Date: 2025-11-11 21:20:55.539469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, ForeignKey, Integer
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '8a83602457d3'
down_revision: Union[str, Sequence[str], None] = 'd7c9a21aaedc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", (sa.Column("user_id", sa.Integer(), nullable=False)))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users",
                          local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
    pass
