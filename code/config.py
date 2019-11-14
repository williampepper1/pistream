import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATEBASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False