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
        db.session.add(cont)
        db.session.commit()
    return render_template('form.html', block_title='Add Contract', form=form)


@app.route('/info')
@login_required
def info():
    user = ClientUser.query.filter_by(id=session['user_id']).first()
    legal = user.legalentity
    license_info = legal.license
    contract_info = legal.contract
    print(contract_info[0].contract_number)
    appendix = Appendix.query.filter_by(contract=contract_info[0].id).all()
    addition = Addition.query.filter_by(contract=contract_info[0].id).all()
    print(appendix)
    info = {'user': user, 'legal': legal,
            'license': license_info, 'contract': zip([i for i in range(1,len(contract_info)+1)], contract_info),
            'appendix': appendix, 'addition': addition
            }
    print(info)
    return render_template('info.html', info=info)

@app.route('/contract/<int:contract_id>')
@login_required
def contract_info_route(contract_id):
    user = ClientUser.query.filter_by(id=session['user_id']).first()
    con = (i.contract_number for i in user.legalentity.contract)
    if contract_id in con:
        contract_info = Contract.query.filter_by(contract_number=contract_id).first()
        appendix = Appendix.query.filter_by(contract=contract_info.id).all()
        addition = Addition.query.filter_by(contract=contract_info.id).all()
        print(type(addition))
        return render_template('contract_info.html',contract=contract_info,
                               addition=addition, appendix=appendix,
                               appendix_number=len(appendix), addition_number=len(addition))
    return render_template('404.html')
