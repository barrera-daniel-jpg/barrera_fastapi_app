"""merge the existing migration heads

Revision ID: c2e8f1a0b7d3
Revises: 3915f83734d8, a7c4e1d2f890

"""
from typing import Sequence, Union

from alembic import op


revision: str = "c2e8f1a0b7d3"
down_revision: Union[str, Sequence[str], None] = (
    "3915f83734d8",
    "a7c4e1d2f890",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass