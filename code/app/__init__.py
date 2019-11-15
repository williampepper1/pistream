from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

login = LoginManager(app)
login.login_view = 'index'

from app import routes, models
from app.routes import MyAdminIndexView, UserAdminView
from app.models import User

admin = Admin(app, index_view=MyAdminIndexView(), base_template='admin/my_master.html', template_mode='bootstrap3')
admin.add_view(UserAdminView(models.User, db.session))
