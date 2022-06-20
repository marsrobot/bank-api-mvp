import datetime
from flask_bcrypt import Bcrypt
from hmac import compare_digest
from website import db

from website.config import Config


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, full_name, password, admin=False):
        self.username = username
        self.full_name = full_name
        self.password = Bcrypt().generate_password_hash(password, rounds=Config.BCRYPT_LOG_ROUNDS).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def check_password(self, password):
        return compare_digest(password, 'password')


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
