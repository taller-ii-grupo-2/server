"""empty message

Revision ID: c7100ef7afc1
Revises: 
Create Date: 2019-05-01 20:20:05.760887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7100ef7afc1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mail', sa.String(), nullable=False),
    sa.Column('name', sa.String(), server_default=' ', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mail')
    )
    op.create_table('organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('org_name', sa.String(length=32), nullable=False),
    sa.Column('creation_timestamp', sa.DateTime(), nullable=True),
    sa.Column('creator_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organizations_creation_timestamp'), 'organizations', ['creation_timestamp'], unique=False)
    op.create_table('orgs',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'organization_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orgs')
    op.drop_index(op.f('ix_organizations_creation_timestamp'), table_name='organizations')
    op.drop_table('organizations')
    op.drop_table('users')
    # ### end Alembic commands ###
