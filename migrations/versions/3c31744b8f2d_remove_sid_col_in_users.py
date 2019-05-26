"""remove sid col in users

Revision ID: 3c31744b8f2d
Revises: cfa8fe8e3f47
Create Date: 2019-05-26 04:01:51.816697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c31744b8f2d'
down_revision = 'cfa8fe8e3f47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'sid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('sid', sa.VARCHAR(length=20), server_default=sa.text("' '::character varying"), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
