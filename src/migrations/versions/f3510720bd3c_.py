"""empty message

Revision ID: f3510720bd3c
Revises: 981a5ae0fc5e
Create Date: 2017-04-16 15:26:13.740933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3510720bd3c'
down_revision = '981a5ae0fc5e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'roles', ['name'])
    pass


def downgrade():
    op.drop_constraint(None, 'roles', ['name'])
    pass
