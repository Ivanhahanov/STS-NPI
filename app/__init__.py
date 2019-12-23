from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin
app = Flask(__name__)
app.config.from_object(Config)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:explabs@localhost/spyregistrydatabase"
app.config['SECRET_KEY'] = 'Hello'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
login = LoginManager()
login.init_app(app)
login.login_view = "login"

from flask_admin.contrib.sqla import ModelView

# Flask and Flask-SQLAlchemy initialization here


from app import routes, models

admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(ModelView(models.ClientUser, db.session))
admin.add_view(ModelView(models.Legalentity, db.session))
admin.add_view(ModelView(models.AdminLogs, db.session))
admin.add_view(ModelView(models.Contract, db.session))
admin.add_view(ModelView(models.Addition, db.session))
admin.add_view(ModelView(models.Appendix, db.session))
admin.add_view(ModelView(models.License, db.session))
admin.add_view(ModelView(models.EmployeeRole, db.session))
admin.add_view(ModelView(models.Employee, db.session))
admin.add_view(ModelView(models.Executor, db.session))
admin.add_view(ModelView(models.Statement, db.session))
admin.add_view(ModelView(models.Conclusion, db.session))
admin.add_view(ModelView(models.Classification, db.session))
admin.add_view(ModelView(models.Expertise, db.session))
admin.add_view(ModelView(models.TechnicalDocument, db.session))
admin.add_view(ModelView(models.SupplementaryDocument, db.session))



