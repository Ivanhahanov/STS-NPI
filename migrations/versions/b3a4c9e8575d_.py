"""empty message

Revision ID: b3a4c9e8575d
Revises: cea472471dae
Create Date: 2019-12-04 21:07:14.470446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3a4c9e8575d'
down_revision = 'cea472471dae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('legalentity', sa.Column('INN', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('legalentity', 'INN')
    # ### end Alembic commands ###
