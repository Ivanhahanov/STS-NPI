from flask_login import logout_user, login_required
from . import app, login
from flask import redirect, url_for, flash, render_template, request, session
from flask_login import login_user
from app.models import *
from app.forms import *
import hashlib

@login.user_loader
def user_loader(user_id):
    return ClientUser.query.get(user_id)

def reg(form):
    form = RegForm(obj=form)
    if request.method == 'POST' and form.validate():
        if db.session.query(db.exists().where(ClientUser.username == form.username.data)).scalar():
            flash('Username already exists', 'error')
        elif db.session.query(db.exists().where(ClientUser.email == form.email.data)).scalar():
            flash('Email already exists', 'error')
        else:
            username = form.username.data
            password = form.password.data.encode()
            email = form.email.data
            salt = username.encode()
            hashed_password = hashlib.md5(password + salt).hexdigest()
            print(username, password, hashed_password)
            user = ClientUser()
            user.username = username
            user.email = email
            user.password_hash = hashed_password
            db.session.add(user)
            db.session.commit()
    return form

@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data.encode()
        salt = username.encode()
        hashed_password = hashlib.md5(password + salt).hexdigest()
        user = ClientUser.query.filter_by(username=username).first()
        if username == user.username:
            print(user.password_hash)
            if hashed_password == user.password_hash:
                print(username, password, user.password_hash)
                login_user(user)
                session['user_id'] = user.id
                if username == 'admin':
                    return redirect('/admin', 302)
                else:
                    return redirect('/info', 302)
    return render_template('form.html', block_title='Login', form=form)


@app.route('/registry/', methods=['POST', 'GET'])
def registry():
    form = RegForm(request.form)
    if request.method == 'POST' and form.validate():
        if db.session.query(db.exists().where(ClientUser.username == form.username.data)).scalar():
            flash('Username already exists', 'error')
        elif db.session.query(db.exists().where(ClientUser.email == form.email.data)).scalar():
            flash('Email already exists', 'error')
        else:
            username = form.username.data
            password = form.password.data.encode()
            email = form.email.data
            salt = username.encode()
            hashed_password = hashlib.md5(password + salt).hexdigest()
            print(username, password, hashed_password)
            user = ClientUser()
            user.username = username
            user.email = email
            user.password_hash = hashed_password
            db.session.add(user)
            db.session.commit()
    return render_template('form.html', block_title='Register', form=form)

@app.route('/edit_user/', methods=['POST', 'GET'])
def edit_user():
    user = ClientUser.query.filter_by(id=session['user_id']).first_or_404()
    form = RegForm(obj=user)
    if request.method == 'POST' and form.validate():
        if user.username != form.username.data and db.session.query(db.exists().where(ClientUser.username == form.username.data)).scalar():
            flash('Username already exists', 'error')
        elif user.email != form.email.data and db.session.query(db.exists().where(ClientUser.email == form.email.data)).scalar():
            flash('Email already exists', 'error')
        else:
            username = form.username.data
            password = form.password.data.encode()
            email = form.email.data
            salt = username.encode()
            hashed_password = hashlib.md5(password + salt).hexdigest()
            print(username, password, hashed_password)
            user.username = username
            user.email = email
            user.password_hash = hashed_password
            db.session.commit()

    return render_template('form.html', block_title='Edit User', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/head', methods=['POST', 'GET'])
@login_required
def head():
    form = HeadForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form.first_name.data,
              form.last_name.data,
              form.surname.data)
        return redirect('/index', 302)
    return render_template('form.html', block_title='Register Head', form=form)


@app.route('/license', methods=['POST', 'GET'])
@login_required
def show_license():
    form = LicenseForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form.license_number.data,
              form.issued_by.data,
              form.license_file.data,
              form.license_date.data)
        return redirect('/legaldata', 302)
    return render_template('form.html', block_title='Register License', form=form)


@app.route('/legaldata', methods=['POST', 'GET'])
@login_required
def legal_data():
    form = LegalForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form.full_name.data,
              form.short_name.data,
              form.company_name.data,
              form.INN.data,
              form.OGRN.data,
              form.legal_address.data,
              form.real_address.data,
              form.index.data,
              form.tax_number.data,
              form.tax_date.data)
        return redirect('/head', 302)
    return render_template('form.html', block_title='Register Data', form=form)


@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/contract', methods=['GET', 'POST'])
def contract():
    form = ContractForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form.contract_number.data, form.organiztion_name.data)
        cont = Contract(contract_number=form.contract_number.data,
                        organization=form.organiztion_name.data)
        user = ClientUser.query.filter_by(id=session['user_id']).first()
        user = user.legalentity
        db.session.add(cont)
        user.contract.append(cont)
        db.session.add(user)
        db.session.commit()
        return redirect('/info', 302)
    return render_template('form.html', block_title='Add Contract', form=form)


@app.route('/info')
@login_required
def info():
    info = {'user': '', 'legal': '',
            'license': '', 'contract': '',
            'appendix': '', 'addition': '',
            }
    user = ClientUser.query.filter_by(id=session['user_id']).first_or_404()
    info['user'] = user
    if user.legalentity is not None:
        legal = user.legalentity
        info['legal'] = legal
        license_info = legal.license
        if license_info is not None:
            info['license'] = license_info
            contract_info = legal.contract
            if contract_info is not None:
                info['contract'] = zip([i for i in range(1,len(contract_info)+1)], contract_info)
                appendix = Appendix.query.filter_by(contract=contract_info[0].contract_number).all()
                addition = Addition.query.filter_by(contract=contract_info[0].contract_number).all()
                info['addition'] = addition
                info['appendix'] = appendix

    return render_template('info.html', info=info)

@app.route('/contract/<int:contract_id>')
@login_required
def contract_info_route(contract_id):
    user = ClientUser.query.filter_by(id=session['user_id']).first()
    con = (i.contract_number for i in user.legalentity.contract)
    if contract_id in con:
        contract_info = Contract.query.filter_by(contract_number=contract_id).first()
        appendix = Appendix.query.filter_by(contract=contract_info.contract_number).all()
        addition = Addition.query.filter_by(contract=contract_info.contract_number).all()
        print(type(addition))
        return render_template('contract_info.html',contract=contract_info,
                               addition=addition, appendix=appendix,
                               appendix_number=len(appendix), addition_number=len(addition))
    return render_template('404.html')

@app.route('/add_contract_additions', methods=['POST', 'GET'])
def add_contract_additions():
    form = AdditionForm(request.form)
    return render_template("form.html", block_title='Add Additions', form=form)

@app.route('/add_contract_appendix', methods=['POST', 'GET'])
def add_contract_appendix():
    form = AppendixForm(request.form)
    return render_template("form.html", block_title='Add Appendix', form=form)

@app.route('/statement')
def statement():
    info = {'executor': '',
            'legal': '',
            'contract': '',
            'contract_info': '',
            'license_info': '',
            'employee_head': '',
            'employee': '',
            'enter_statement': '',
            }
    user = ClientUser.query.filter_by(id=session['user_id']).first()
    legal = user.legalentity
    if legal is not None:
        info['legal'] = legal
        license_info = legal.license
        if license_info is not None:
            info['license_info'] = license_info
            contract_info = legal.contract
            if contract_info is not None:
                info['contract_info'] = contract_info
                head = Employee.query.filter_by(legalentity=legal.INN, employee_role=1 ).first()
                if head is not None:
                    info['employee_head'] = head
                    employee = Employee.query.filter_by(legalentity=legal.INN).filter(Employee.employee_role != 1).first()
                    if employee is not None:
                        info['employee'] = employee
                        contract = 'contract'
                        exe = Executor.query.filter_by(id=1).first()
                        if exe is not None:
                            info['executor'] = exe
                            enter_statement = EnterStatement.query.filter_by(legalentity=legal.INN).first()
                            if enter_statement is not None:
                                info['expertise'] = enter_statement.expertise
                                enter_statement = EnterStatement.query.filter_by(legalentity=legal.INN).first()
                                info['enter_statement'] = enter_statement
                                print(enter_statement.classification.code_name)

    return render_template("statement.html", info=info)

@app.route('/change_legal', methods=['GET', 'POST'])
def change_legal():
    user = ClientUser.query.filter_by(id=session['user_id']).first()
    legal = user.legalentity
    form = LegalForm(obj=legal)
    if request.method == 'POST' and form.validate():
        print(form.full_name.data,
              form.short_name.data,
              form.company_name.data,
              form.INN.data,
              form.OGRN.data,
              form.legal_address.data,
              form.real_address.data,
              form.index.data,
              form.tax_number.data,
              form.tax_date.data)
        return redirect('/head', 302)
    return render_template('form.html', block_title='Edit leglal user', form=form)

@app.route('/change_license', methods=['GET', 'POST'])
def change_license():
    user = ClientUser.query.filter_by(id=session['user_id']).first()
    legal = user.legalentity
    lic = legal.license
    form = LicenseForm(obj=lic)
    if request.method == 'POST' and form.validate():
        print(form.license_number.data,
              form.issued_by.data,
              form.license_file.data,
              form.license_date.data)
        return redirect('/legaldata', 302)
    return render_template('form.html', block_title='Register License', form=form)

@app.route('/change_expertise', methods=['GET', 'POST'])
def change_expertise():
    form = ExpertiseForm()
    return render_template('form.html', form=form)
    # return render_template('form.html', block_title='Register License', form=form)

@app.route('/change_1', methods=['GET', 'POST'])
def change_1():
    return 'change license'

@app.route('/change_2', methods=['GET', 'POST'])
def change_2():
    return 'change license'

@app.route('/change_3', methods=['GET', 'POST'])
def change_3():
    return 'change license'

@app.route('/admin_console', methods=['GET', 'POST'])
def admin_console():
    data = []
    if request.method == 'POST':
        data = request.form.get('command')
        data = db.engine.execute(data)
        print(data)
    return render_template('admin_console.html', data=data)

@app.route('/vulnerability_login', methods=['GET', 'POST'])
def vulnerability_login():
    data = []
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        print(login, password)
        salt = login.encode()
        password = hashlib.md5(password.encode() + salt).hexdigest()
        sql_login = "select id from client_user where username = '%s' and password_hash = '%s'" % (login, password)
        print(sql_login)

        data = db.engine.execute(sql_login)
        print(type(data))
        answer = [line[0] for line in data]
        print(answer)
        # session['user_id'] = answer[0]
        # return redirect('/statement', 302)
        if answer[0] == 2:
            return redirect('/admin', 302)
    return render_template('vulnerability_login.html', data=data)

