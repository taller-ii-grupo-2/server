"""bots: change from org_id to org_name

Revision ID: da969dbec37b
Revises: 8be7e10aaf8d
Create Date: 2019-07-02 03:05:21.448124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da969dbec37b'
down_revision = '8be7e10aaf8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bots', sa.Column('organization_name', sa.String(length=32), nullable=True))
    op.drop_constraint('bots_organization_id_fkey', 'bots', type_='foreignkey')
    op.drop_column('bots', 'organization_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bots', sa.Column('organization_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('bots_organization_id_fkey', 'bots', 'organizations', ['organization_id'], ['id'])
    op.drop_column('bots', 'organization_name')
    # ### end Alembic commands ###
