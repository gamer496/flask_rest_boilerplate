from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
manager = Manager(app)
CORS(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()

from app import models, views
