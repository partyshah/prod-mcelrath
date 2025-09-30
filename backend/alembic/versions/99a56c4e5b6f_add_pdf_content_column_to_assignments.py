"""Add pdf_content column to assignments

Revision ID: 99a56c4e5b6f
Revises: add_pdf_fields
Create Date: 2025-09-23 14:00:40.710276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99a56c4e5b6f'
down_revision: Union[str, None] = 'add_pdf_fields'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('assignments', sa.Column('pdf_content', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('assignments', 'pdf_content')
