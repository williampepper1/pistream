import sys
import logging
import os

activate_this = '/var/www/pistream/pistream/cv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/var/www/pistream/pistream')

from pistream import app as application
application.secret_key = os.getenv('SECRET_KEY', 'for dev')
