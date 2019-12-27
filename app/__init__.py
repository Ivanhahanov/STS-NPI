from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
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

class Controller(ModelView):
    def is_accessible(self):
        if current_user.username != 'admin':

            return False
        return current_user.is_authenticated
    def not_aut(self):
        return "please Login"


admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(Controller(models.ClientUser, db.session))
admin.add_view(Controller(models.Legalentity, db.session))
admin.add_view(Controller(models.AdminLogs, db.session))
admin.add_view(Controller(models.Contract, db.session))
admin.add_view(Controller(models.Addition, db.session))
admin.add_view(Controller(models.Appendix, db.session))
admin.add_view(Controller(models.License, db.session))
admin.add_view(Controller(models.EmployeeRole, db.session))
admin.add_view(Controller(models.Employee, db.session))
admin.add_view(Controller(models.Executor, db.session))
admin.add_view(Controller(models.Statement, db.session))
admin.add_view(Controller(models.Conclusion, db.session))
admin.add_view(Controller(models.Classification, db.session))
admin.add_view(Controller(models.Expertise, db.session))
admin.add_view(Controller(models.TechnicalDocument, db.session))
admin.add_view(Controller(models.SupplementaryDocument, db.session))
admin.add_view(Controller(models.Timeline, db.session))
admin.add_view(Controller(models.Team, db.session))



