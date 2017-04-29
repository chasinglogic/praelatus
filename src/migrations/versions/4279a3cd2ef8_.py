"""empty message

Revision ID: 4279a3cd2ef8
Revises: 
Create Date: 2017-04-10 10:58:47.955561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4279a3cd2ef8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('field_options',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fields',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('data_type', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('labels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permission_schemes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    perm_table = op.create_table('permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    from praelatus.models import Permissions
    for perm in Permissions:
        op.execute(perm_table.insert().values(name=perm.value))
    
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticket_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('profile_pic', sa.String(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workflows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fields_options',
    sa.Column('field_id', sa.Integer(), nullable=True),
    sa.Column('option_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ),
    sa.ForeignKeyConstraint(['option_id'], ['field_options.id'], )
    )
    op.create_table('permission_scheme_permissions',
    sa.Column('permission_scheme_id', sa.Integer(), nullable=True),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['permission_scheme_id'], ['permission_schemes.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.UniqueConstraint('permission_scheme_id', 'role_id', 'permission_id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('key', sa.String(), nullable=True),
    sa.Column('homepage', sa.String(), nullable=True),
    sa.Column('icon_url', sa.String(), nullable=True),
    sa.Column('repo', sa.String(), nullable=True),
    sa.Column('lead_id', sa.Integer(), nullable=True),
    sa.Column('permission_scheme_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lead_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['permission_scheme_id'], ['permission_schemes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tickets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('key', sa.String(), nullable=True),
    sa.Column('summary', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('reporter_id', sa.Integer(), nullable=True),
    sa.Column('assignee_id', sa.Integer(), nullable=True),
    sa.Column('ticket_type_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('workflow_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assignee_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['reporter_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['statuses.id'], ),
    sa.ForeignKeyConstraint(['ticket_type_id'], ['ticket_types.id'], ),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transitions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('to_status_id', sa.Integer(), nullable=True),
    sa.Column('from_status_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['from_status_id'], ['statuses.id'], ),
    sa.ForeignKeyConstraint(['to_status_id'], ['statuses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('field_values',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.Column('field_id', sa.Integer(), nullable=True),
    sa.Column('int_value', sa.Integer(), nullable=True),
    sa.Column('str_value', sa.String(length=255), nullable=True),
    sa.Column('opt_value', sa.String(length=255), nullable=True),
    sa.Column('flt_value', sa.Float(), nullable=True),
    sa.Column('date_value', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hooks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('method', sa.String(length=10), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('transition_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['transition_id'], ['transitions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('labels_tickets',
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.Column('label_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['label_id'], ['labels.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], )
    )
    op.create_table('users_roles',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.UniqueConstraint('user_id', 'role_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_roles')
    op.drop_table('labels_tickets')
    op.drop_table('hooks')
    op.drop_table('field_values')
    op.drop_table('comments')
    op.drop_table('transitions')
    op.drop_table('tickets')
    op.drop_table('projects')
    op.drop_table('permission_scheme_permissions')
    op.drop_table('fields_options')
    op.drop_table('workflows')
    op.drop_table('users')
    op.drop_table('ticket_types')
    op.drop_table('statuses')
    op.drop_table('roles')
    op.drop_table('permissions')
    op.drop_table('permission_schemes')
    op.drop_table('labels')
    op.drop_table('fields')
    op.drop_table('field_options')
    # ### end Alembic commands ###
