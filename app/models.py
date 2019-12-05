from app import db
from flask_login import UserMixin

class ClientUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    INN = db.Column(db.Integer, db.ForeignKey('legalentity.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Addition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addition_number = db.Column(db.Integer)
    file = db.Column(db.String(128))
    contract = db.Column(db.Integer, db.ForeignKey('contract.id'))

class Appendix(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appendix_number = db.Column(db.Integer)
    file = db.Column(db.String(128))
    contract = db.Column(db.Integer, db.ForeignKey('contract.id'))


contracts = db.Table('contracts',
                     db.Column('contract_id', db.Integer, db.ForeignKey('contract.id')),
                     db.Column('legalentity_id', db.Integer, db.ForeignKey('legalentity.id'))
                     )


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_number = db.Column(db.Integer)
    organization = db.Column(db.String(128))
    addition_id = db.relationship('Addition', backref='document', lazy='dynamic')
    appendix_id = db.relationship('Appendix', backref='document', lazy='dynamic')


class Legalentity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    INN = db.Column(db.Integer)
    license_id = db.Column(db.Integer, db.ForeignKey('license.id'))
    user = db.relationship('ClientUser', backref='legalentity', lazy='dynamic')
    contract = db.relationship('Contract', secondary=contracts, backref=db.backref('legal', lazy='dynamic'))

class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_number = db.Column(db.Integer, nullable=False)
    legalentity = db.relationship('Legalentity', backref='license', lazy='dynamic')


class Executor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FIO_director = db.Column(db.String(64))
    FIO_executor = db.Column(db.String(64))
    position = db.Column(db.String(64))
    mail_address = db.Column(db.String(64))
    index = db.Column(db.Integer)
    conclusion = db.relationship('Conclusion', backref='executor', lazy='dynamic')

class Statement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    statement_number = db.Column(db.Integer)
    INN = db.Column(db.Integer, db.ForeignKey('legalentity.id'))

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
    passport = db.Column(db.String)


class Classification(db.Model):
    code = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String)
    conclusion = db.relationship('EnterStatement', backref='classification', lazy='dynamic')

class Expertise(db.Model):
    expertise_number = db.Column(db.String, primary_key=True)
    expertise_conclusion = db.Column(db.String)
    address = db.Column(db.String)
    organization_name = db.Column(db.String)
    expert_FIO = db.Column(db.String)
    statement = db.relationship('EnterStatement', backref='expertise', lazy='dynamic')

class TechnicalDocument(db.Model):
    passport_code = db.Column(db.BigInteger, primary_key=True)
    manual = db.Column(db.String)
    specific = db.Column(db.String)
    document_number = db.relationship('SupplementaryDocument', backref='tech', lazy='dynamic')

class SupplementaryDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_name = db.Column(db.String)
    document = db.Column(db.String)
    technical_doc = db.Column(db.BigInteger, db.ForeignKey('technical_document.passport_code'))
