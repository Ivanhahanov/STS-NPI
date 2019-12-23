from app.models import *
import random
import time
import hashlib
def gen_rand_int(num):
    return ''.join([str(random.randint(0, 9)) for _ in range(num)])

def gen_rand_file():
    return time.strftime(str(random.randint(0, 1000))+"%d%H%M%S%Y.pdf")

def docs():
    code = gen_rand_int(10)
    main_doc = TechnicalDocument(passport_code=code,
                                 manual=gen_rand_file(),
                                 specific=gen_rand_file()
                                 )
    doc = SupplementaryDocument(document_name=str(gen_rand_int(1)),
                                document=gen_rand_file(),
                                tech=main_doc)
    db.session.add(main_doc)
    db.session.add(doc)
    db.session.commit()
    return main_doc

def create_expertise():
    ex = Expertise()
    num = gen_rand_int(3)
    ex.expertise_number = num
    ex.expertise_conclusion = 'ok'
    ex.address = 'Moscow'
    ex.organization_name = 'expert_company'
    ex.expert_FIO = 'Alexandrov A.A.'

    return ex

def create_classification():
    cl = Classification()
    c = gen_rand_int(1)
    cl.code = c
    cl.code_name = 'Name'
    return cl

def create_enter_statement(code, expertise, tech, inn):

    enter_statement = EnterStatement()
    enter_statement.enter_conclusion_number = gen_rand_int(1)
    enter_statement.classification = code
    enter_statement.expertise = expertise
    enter_statement.tech = tech
    enter_statement.legalentity = inn

def create_user(number):
    username = 'Ivan'
    password = 'explabs'
    user = ClientUser()
    user.username = username
    user.email = 'ivan@mail.ru'
    salt = username.encode()
    hashed_password = hashlib.md5(password.encode() + salt).hexdigest()
    user.password_hash = hashed_password
    user.legalentity = Legalentity.query.filter_by(INN=number).first()
    db.session.add(user)
    db.session.commit()


def create_contract_and_app():
    l = ['explabs', 'Bi.Zone', 'Solar', 'Elcomsoft', 'Positive Technologies']
    contract = Contract()
    contract.contract_number = gen_rand_int(3)
    contract.organization = random.choice(l)
    db.session.add(contract)
    add = Addition()
    add.addition_number = gen_rand_int(5)
    add.file = gen_rand_file()
    add.document = contract
    appl = Appendix()
    appl.appendix_number = gen_rand_int(5)
    appl.file = gen_rand_file()
    appl.document = contract
    db.session.add_all([add, appl])
    db.session.commit()

def create_legal():
    lic = License()
    lic.license_number = gen_rand_int(10)
    lic.organization = 'organization'
    lic.date = time.strftime('%Y-%m-%d')
    db.session.add(lic)
    legal = Legalentity()
    inn = gen_rand_int(12)
    legal.INN = inn
    legal.full_name = '1'
    legal.short_name = '1'
    legal.company_name = '1'
    legal.OGRN = gen_rand_int(13)
    legal.legal_address = '1'
    legal.real_address = '1'
    legal.license = lic
    db.session.add(legal)
    e = ['supervisor', 'intern']
    b = ['Ivanov I.I.', 'Petrov P.P']
    for role, name in zip(e,b):
        empr = EmployeeRole()
        empr.role = role
        db.session.add(empr)


        emp = Employee()
        emp.employee_code = gen_rand_int(3)
        emp.role = empr
        emp.employee_FIO = name
        emp.legal = legal

    db.session.commit()
    return inn

def add_contracts_rel(inn, number):
    user = Legalentity.query.filter_by(INN=inn).first()
    cont = Contract.query.filter_by(contract_number=number).first()
    user.contract.append(cont)
    db.session.add(user)
    db.session.commit()

def executor_data():
    executors = ['Иванов И.И.', 'intern', 'ivanov@mail.ru']
    exe = Executor(FIO_executor=executors[0], position=executors[1], mail_address=executors[2])
    db.session.add(exe)
    db.session.commit()

inn = 678754001903
number = 781
# inn = create_legal()
# create_user(inn)
# create_enter_statement(create_classification(), create_expertise(), docs(), inn)
# create_contract_and_app()
add_contracts_rel(inn, number)
executor_data()
