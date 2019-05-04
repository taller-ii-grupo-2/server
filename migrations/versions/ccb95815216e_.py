"""empty message

Revision ID: ccb95815216e
Revises: 32d49973b7c3
Create Date: 2019-05-04 02:28:50.829424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccb95815216e'
down_revision = '32d49973b7c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('organizations', sa.Column('url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('organizations', 'url')
    # ### end Alembic commands ###
