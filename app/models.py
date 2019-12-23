from app import db
from flask_login import UserMixin
import datetime
class ClientUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(64))
    INN = db.Column(db.BigInteger, db.ForeignKey('legalentity.INN'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class AdminLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20))
    user_pass = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Contract(db.Model):
    contract_number = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String())
    addition_id = db.relationship('Addition', backref='document', lazy='dynamic')
    appendix_id = db.relationship('Appendix', backref='document', lazy='dynamic')

class Addition(db.Model):
    addition_number = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(128))
    contract = db.Column(db.Integer, db.ForeignKey('contract.contract_number'))

class Appendix(db.Model):
    appendix_number = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(128))
    contract = db.Column(db.Integer, db.ForeignKey('contract.contract_number'))


contracts = db.Table('contracts',
                     db.Column('contract_id', db.Integer, db.ForeignKey('contract.contract_number')),
                     db.Column('legalentity_id', db.BigInteger, db.ForeignKey('legalentity.INN'))
                     )


class License(db.Model):
    license_number = db.Column(db.BigInteger, primary_key=True)
    organization = db.Column(db.String)
    date = db.Column(db.DateTime)
    legalentity = db.relationship('Legalentity', backref='license', lazy='dynamic')

class Legalentity(db.Model):
    INN = db.Column(db.BigInteger(), primary_key=True)
    full_name = db.Column(db.String())
    short_name = db.Column(db.String())
    company_name = db.Column(db.String())
    OGRN = db.Column(db.BigInteger())
    legal_address = db.Column(db.String())
    real_address = db.Column(db.String())
    license_number = db.Column(db.BigInteger, db.ForeignKey('license.license_number'))
    employee_number = db.relationship('Employee', backref='legal', lazy='dynamic')
    user = db.relationship('ClientUser', backref='legalentity', lazy='dynamic')
    contract = db.relationship('Contract', secondary=contracts, backref=db.backref('legal', lazy='dynamic'))

    def __str__(self):
        return str(self.INN)

class EmployeeRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String())
    employee = db.relationship('Employee', backref='role', lazy='dynamic')

class Employee(db.Model):
    employee_code = db.Column(db.Integer, primary_key=True)
    employee_role = db.Column(db.Integer, db.ForeignKey('employee_role.id'))
    employee_FIO = db.Column(db.String())
    legalentity = db.Column(db.BigInteger, db.ForeignKey('legalentity.INN'))






class Executor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FIO_executor = db.Column(db.String(64))
    position = db.Column(db.String(64))
    mail_address = db.Column(db.String(64))
    conclusion = db.relationship('Conclusion', backref='executor', lazy='dynamic')

class Statement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    statement_number = db.Column(db.Integer)
    INN = db.Column(db.BigInteger, db.ForeignKey('legalentity.INN'))

class Conclusion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conclusion_number = db.Column(db.Integer)
    executor_info = db.Column(db.Integer, db.ForeignKey('executor.id'))
    file = db.Column(db.String(128))
    data = db.Column(db.DateTime)

class EnterStatement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enter_conclusion_number = db.Column(db.Integer)
    code = db.Column(db.Integer, db.ForeignKey('classification.code'))
    expertise_number = db.Column(db.String, db.ForeignKey('expertise.expertise_number'))
    passport = db.Column(db.BigInteger, db.ForeignKey('technical_document.passport_code'))
    legalentity = db.Column(db.BigInteger, db.ForeignKey('legalentity.INN'))


class Classification(db.Model):
    code = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String)
    conclusion = db.relationship('EnterStatement', backref='classification', lazy='dynamic')

class Expertise(db.Model):
    expertise_number = db.Column(db.String, primary_key=True)
    expertise_conclusion = db.Column(db.String)  # TODO: create new table for expertise conclusion
    address = db.Column(db.String)
    organization_name = db.Column(db.String)
    expert_FIO = db.Column(db.String)
    statement = db.relationship('EnterStatement', backref='expertise', lazy='dynamic')

class TechnicalDocument(db.Model):
    passport_code = db.Column(db.BigInteger, primary_key=True)
    manual = db.Column(db.String)
    specific = db.Column(db.String)
    document_number = db.relationship('SupplementaryDocument', backref='tech', lazy='dynamic')
    statement = db.relationship('EnterStatement', backref='tech', lazy='dynamic')

class SupplementaryDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_name = db.Column(db.String)
    document = db.Column(db.String)
    technical_doc = db.Column(db.BigInteger, db.ForeignKey('technical_document.passport_code'))
