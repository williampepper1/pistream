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
from routes import MyAdminIndexView
from models import User

admin = Admin(app, index_view=MyAdminIndexView(), template_mode='bootstrap3')
admin.add_view(ModelView(models.User, db.session))
