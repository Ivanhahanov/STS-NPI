"""empty message

Revision ID: cea472471dae
Revises: 28502fbdf676
Create Date: 2019-12-04 19:44:32.918188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cea472471dae'
down_revision = '28502fbdf676'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client_user', sa.Column('INN', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'client_user', 'legalentity', ['INN'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'client_user', type_='foreignkey')
    op.drop_column('client_user', 'INN')
    # ### end Alembic commands ###