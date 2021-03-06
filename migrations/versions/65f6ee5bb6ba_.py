"""empty message

Revision ID: 65f6ee5bb6ba
Revises: b15ff883236d
Create Date: 2019-12-24 17:03:08.620870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65f6ee5bb6ba'
down_revision = 'b15ff883236d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timeline',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timeline')
    # ### end Alembic commands ###
