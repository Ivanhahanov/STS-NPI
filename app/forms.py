from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, FileField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms import validators

def check_password(field):
    if field.data.isdigit():
        raise ValidationError("Must contain a symbols")
    if '!' not in field.data:
        raise ValidationError("Must contain a character '!'")
    if '*' not in field.data:
        raise ValidationError("Must contain a character '*'")
    if '&' not in field.data:
        raise ValidationError("Must contain a character '&'")
    if '?' not in field.data:
        raise ValidationError("Must contain a character '?'")
    if '@' not in field.data:
        raise ValidationError("Must contain a character '@'")


class RegForm(FlaskForm):
    username = StringField('Username or email', [validators.Length(min=4, max=25),
                                                 validators.DataRequired()])
    email = StringField('E-mail', [validators.DataRequired("Enter a valid email address"),
                                   validators.Email("Enter a valid email address")])
    password = PasswordField('Password', [Length(min=3, max=25),
                                          validators.DataRequired(),
                                          # check_password,
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField('Username', [Length(min=4, max=25)])
    password = PasswordField('Password', [Length(min=3, max=25),
                                          validators.DataRequired(),
                                          # check_password,
                                          ])
    submit = SubmitField("Sign In")
class HeadForm(FlaskForm):
    first_name = StringField('Firstname', validators=[InputRequired()])
    last_name = StringField('Lastname', validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    submit = SubmitField("Register")

class LicenseForm(FlaskForm):
    license_number = IntegerField('License Number', validators=[InputRequired()])
    issued_by = StringField('Issued by', validators=[InputRequired()])
    license_file = FileField('License file')
    license_date = DateField('License date', format='%m.%d.%Y')
    submit = SubmitField("Register")

class LegalForm(FlaskForm):
    full_name = StringField('full_name')
    short_name = StringField('short_name')
    company_name = StringField('company_name')
    INN = IntegerField('inn')
    OGRN = IntegerField('ogrn')
    legal_address = StringField('legal_address')
    real_address = StringField('real_address')
    index = IntegerField('index')
    tax_number = IntegerField('tax_number')
    tax_date = DateField('tax_date', format='%m.%d.%Y')
    submit = SubmitField("Register")

class StatementForm(FlaskForm):
    classificator = StringField('classificator')

class ContractForm(FlaskForm):
    contract_number = IntegerField('Contract Number')
    organiztion_name = StringField('Name of organization')
    submit = SubmitField("Submit")
