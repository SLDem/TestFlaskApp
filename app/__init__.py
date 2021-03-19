from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

CKEDITOR_ENABLE_CSRF = True
WTF_CSRF_ENABLED = False
WTF_CSRF_SECRET_KEY = 'a random string'

app.config['SECRET_KEY'] = 'SDQ(*&SD(*Q(899*DS98(*&8978sd7987s98d7q9*Q'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
