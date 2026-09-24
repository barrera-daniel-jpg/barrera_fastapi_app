"""add unique product name index

Revision ID: a7c4e1d2f890
Revises: d34b82694cc1

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a7c4e1d2f890"
down_revision: Union[str, Sequence[str], None] = "d34b82694cc1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "uq_app_inv_products_name_lower",
        "app_inv_products",
        [sa.text("lower(name)")],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "uq_app_inv_products_name_lower",
        table_name="app_inv_products",
    )