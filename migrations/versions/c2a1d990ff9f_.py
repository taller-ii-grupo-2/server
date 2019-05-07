"""empty message

Revision ID: c2a1d990ff9f
Revises: 781165f2a739
Create Date: 2019-05-05 23:28:37.984135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2a1d990ff9f'
down_revision = '781165f2a739'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usrs',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'channel_id')
    )
    op.add_column('channels', sa.Column('organization_id', sa.Integer(), nullable=False))
    op.drop_constraint('channels_organization_fkey', 'channels', type_='foreignkey')
    op.create_foreign_key(None, 'channels', 'organizations', ['organization_id'], ['id'])
    op.drop_column('channels', 'organization')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('channels', sa.Column('organization', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'channels', type_='foreignkey')
    op.create_foreign_key('channels_organization_fkey', 'channels', 'organizations', ['organization'], ['id'])
    op.drop_column('channels', 'organization_id')
    op.drop_table('usrs')
    # ### end Alembic commands ###