from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, FileField, PasswordField, SubmitField,FieldList, FormField
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
    submit = SubmitField("Submit")

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
    submit = SubmitField("Submit")

class LicenseForm(FlaskForm):
    license_number = IntegerField('License Number', validators=[InputRequired()])
    issued_by = StringField('Issued by', validators=[InputRequired()])
    license_file = FileField('License file')
    license_date = DateField('License date', format='%m.%d.%Y')
    submit = SubmitField("Submit")

class LegalForm(FlaskForm):
    full_name = StringField('Full name')
    short_name = StringField('Short name')
    company_name = StringField('Company name')
    INN = IntegerField('INN')
    OGRN = IntegerField('ORGN')
    legal_address = StringField('Legal address')
    real_address = StringField('Real address')
    submit = SubmitField("Submit")

class StatementForm(FlaskForm):
    classificator = StringField('classificator')

class ContractForm(FlaskForm):
    contract_number = IntegerField('Contract Number')
    organiztion_name = StringField('Name of organization')
    submit = SubmitField("Submit")

class AdditionForm(FlaskForm):
    addition_number = IntegerField('Addition Number')
    file = FileField('Addition file')

class AppendixForm(FlaskForm):
    appendix_number = IntegerField('Appendix Number')
    file = FileField('Appendix file')

class TimeForm(FlaskForm):
    opening = StringField('Opening Hour')
    closing = StringField('Closing Hour')

class ExpertiseForm(FlaskForm):
    expertise_number = IntegerField('Expertise Number')
    expertise_conclusion = StringField('Conclusion') # TODO: create new table for expertise conclusion
    address = StringField('Address')
    organization_name = StringField('Name of organization')
    expert_FIO = StringField('Expert Name')
