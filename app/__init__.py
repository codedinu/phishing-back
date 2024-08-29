from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

from app.routes import user_route, scam_route, history_route, ai_route
from app.models import user_model, scam_model, history_model

with app.app_context():
    db.create_all()
