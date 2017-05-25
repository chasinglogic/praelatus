"""Add required default data

This adds the anonymous user and the default system roles.

Revision ID: 44c838f2b288
Revises: c3de6b6f6d80
Create Date: 2017-05-14 09:00:30.369654

"""
from alembic import op
from praelatus.models import User
from praelatus.models import Role
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44c838f2b288'
down_revision = 'c3de6b6f6d80'
branch_labels = None
depends_on = None


def upgrade():
    ins = User.__table__.insert()
    op.execute(ins.values(username='anonymous',
                          full_name='System Anonymous User'))
    op.bulk_insert(Role.__table__,
                   [
                       {
                           'name': 'Administrator'
                       },
                       {
                           'name': 'Contributor'
                       },
                       {
                           'name': 'User'
                       },
                       {
                           'name': 'Anonymous'
                       }
                   ])


def downgrade():
    pass
