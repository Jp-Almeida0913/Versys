from flask import *
from flask_login import *
from flask_sqlalchemy import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:secret@localhost/login'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)