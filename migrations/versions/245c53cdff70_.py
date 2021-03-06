"""empty message

Revision ID: 245c53cdff70
Revises: 
Create Date: 2019-12-15 19:54:10.126270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '245c53cdff70'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.String(length=20), nullable=True),
    sa.Column('user_pass', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('classification',
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('code_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('contract',
    sa.Column('contract_number', sa.Integer(), nullable=False),
    sa.Column('organization', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('contract_number')
    )
    op.create_table('employee_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('executor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('FIO_executor', sa.String(length=64), nullable=True),
    sa.Column('position', sa.String(length=64), nullable=True),
    sa.Column('mail_address', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expertise',
    sa.Column('expertise_number', sa.String(), nullable=False),
    sa.Column('expertise_conclusion', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('organization_name', sa.String(), nullable=True),
    sa.Column('expert_FIO', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('expertise_number')
    )
    op.create_table('license',
    sa.Column('license_number', sa.BigInteger(), nullable=False),
    sa.Column('organization', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('license_number')
    )
    op.create_table('technical_document',
    sa.Column('passport_code', sa.BigInteger(), nullable=False),
    sa.Column('manual', sa.String(), nullable=True),
    sa.Column('specific', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('passport_code')
    )
    op.create_table('addition',
    sa.Column('addition_number', sa.Integer(), nullable=False),
    sa.Column('file', sa.String(length=128), nullable=True),
    sa.Column('contract', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contract'], ['contract.contract_number'], ),
    sa.PrimaryKeyConstraint('addition_number')
    )
    op.create_table('appendix',
    sa.Column('appendix_number', sa.Integer(), nullable=False),
    sa.Column('file', sa.String(length=128), nullable=True),
    sa.Column('contract', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contract'], ['contract.contract_number'], ),
    sa.PrimaryKeyConstraint('appendix_number')
    )
    op.create_table('conclusion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conclusion_number', sa.Integer(), nullable=True),
    sa.Column('executor_info', sa.Integer(), nullable=True),
    sa.Column('file', sa.String(length=128), nullable=True),
    sa.Column('data', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['executor_info'], ['executor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('legalentity',
    sa.Column('INN', sa.BigInteger(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('short_name', sa.String(), nullable=True),
    sa.Column('company_name', sa.String(), nullable=True),
    sa.Column('OGRN', sa.BigInteger(), nullable=True),
    sa.Column('legal_address', sa.String(), nullable=True),
    sa.Column('license_number', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['license_number'], ['license.license_number'], ),
    sa.PrimaryKeyConstraint('INN')
    )
    op.create_table('supplementary_document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document_name', sa.String(), nullable=True),
    sa.Column('document', sa.String(), nullable=True),
    sa.Column('technical_doc', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['technical_doc'], ['technical_document.passport_code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('client_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=64), nullable=True),
    sa.Column('INN', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['INN'], ['legalentity.INN'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('contracts',
    sa.Column('contract_id', sa.Integer(), nullable=True),
    sa.Column('legalentity_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['contract_id'], ['contract.contract_number'], ),
    sa.ForeignKeyConstraint(['legalentity_id'], ['legalentity.INN'], )
    )
    op.create_table('employee',
    sa.Column('employee_code', sa.Integer(), nullable=False),
    sa.Column('employee_role', sa.Integer(), nullable=True),
    sa.Column('employee_FIO', sa.String(), nullable=True),
    sa.Column('legalentity', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['employee_role'], ['employee_role.id'], ),
    sa.ForeignKeyConstraint(['legalentity'], ['legalentity.INN'], ),
    sa.PrimaryKeyConstraint('employee_code')
    )
    op.create_table('enter_statement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enter_conclusion_number', sa.Integer(), nullable=True),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.Column('expertise_number', sa.String(), nullable=True),
    sa.Column('passport', sa.BigInteger(), nullable=True),
    sa.Column('legalentity', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['code'], ['classification.code'], ),
    sa.ForeignKeyConstraint(['expertise_number'], ['expertise.expertise_number'], ),
    sa.ForeignKeyConstraint(['legalentity'], ['legalentity.INN'], ),
    sa.ForeignKeyConstraint(['passport'], ['technical_document.passport_code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('statement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('statement_number', sa.Integer(), nullable=True),
    sa.Column('INN', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['INN'], ['legalentity.INN'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('statement')
    op.drop_table('enter_statement')
    op.drop_table('employee')
    op.drop_table('contracts')
    op.drop_table('client_user')
    op.drop_table('supplementary_document')
    op.drop_table('legalentity')
    op.drop_table('conclusion')
    op.drop_table('appendix')
    op.drop_table('addition')
    op.drop_table('technical_document')
    op.drop_table('license')
    op.drop_table('expertise')
    op.drop_table('executor')
    op.drop_table('employee_role')
    op.drop_table('contract')
    op.drop_table('classification')
    op.drop_table('admin_logs')
    # ### end Alembic commands ###
