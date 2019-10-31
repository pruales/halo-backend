import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)
@app.before_first_request
def create_tables():
    db.create_all()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

jwt = JWTManager(app)

from .models import RevokedTokenModel
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

api = Api(app)

from .routes import auth

api.add_resource(auth.UserRegistration, '/register')
api.add_resource(auth.UserLogin, '/login')
api.add_resource(auth.UserLogoutAccess, '/logout/access')
api.add_resource(auth.AllUsers, '/users')

from .routes import kv_routes

api.add_resource(kv_routes.SetItem, '/set')
api.add_resource(kv_routes.GetItems, '/getAll')