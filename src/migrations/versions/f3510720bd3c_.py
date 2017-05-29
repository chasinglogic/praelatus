"""empty message

Revision ID: f3510720bd3c
Revises: c0723755be7f
Create Date: 2017-04-16 15:26:13.740933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3510720bd3c'
down_revision = 'c0723755be7f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'roles', ['name'])
    pass


def downgrade():
    op.drop_constraint(None, 'roles', ['name'])
    pass
