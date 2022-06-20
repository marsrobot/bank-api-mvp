from datetime import datetime
from datetime import timedelta
from datetime import timezone

import pymysql

pymysql.install_as_MySQLdb()

from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import current_user
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_sqlalchemy import SQLAlchemy

from website.logger import get_logger
from website.config import Config

logger = get_logger()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES_SECONDS)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=Config.JWT_REFRESH_TOKEN_EXPIRES_DAYS)

jwt = JWTManager(app)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'mysql://{Config.DATABASE_USER}:{Config.DATABASE_PASSWORD}@{Config.DATABASE_SERVER}/{Config.DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)

from website.models import TokenBlocklist
from website.models import User
from website.unit_api import UnitApi


@app.route('/')
def hello():
    return 'New Bank API'


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return User.query.filter_by(username=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


def log_request():
    logger.info(
        f'remote_addr:{request.remote_addr}, remote_user:{request.remote_user}, url:{request.url}, endpoint:{request.endpoint}')


@app.route('/signup', methods=['POST'])
def signup():
    log_request()
    username = request.json.get('username', None)
    full_name = request.json.get('full_name', None)
    password = request.json.get('password', None)

    users = list(db.session.query(User).all())

    user_data = {
        'username': username,
        'full_name': full_name,
        'password': password,
        'admin': False,
    }
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        resp = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(resp)), 202
    try:
        db.session.add(User(username=user_data['username'],
                            full_name=user_data['full_name'],
                            password=user_data['password'],
                            admin=user_data['admin']))
        db.session.commit()
        responseObject = {
            'status': 'success',
            'message': 'Successfully registered.',
        }
        return make_response(jsonify(responseObject)), 201

    except Exception as ex:
        resp = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return make_response(jsonify(resp)), 401


@app.route('/login', methods=['POST'])
def login():
    log_request()
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()

    if user and Bcrypt().check_password_hash(user.password, password):
        access_token = create_access_token(identity=username).decode('utf-8')
        refresh_token = create_refresh_token(identity=username).decode('utf-8')
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User does not exist.'
        }
        return make_response(jsonify(responseObject)), 404


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    log_request()
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity).decode('utf-8')
    return jsonify(access_token=access_token)


@app.route('/logout', methods=['DELETE'])
@jwt_required()
def modify_token():
    log_request()
    jti = get_jwt()['jti']
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(msg='JWT revoked')


@app.route('/who_am_i', methods=['GET', 'POST'])
@jwt_required()
def who_am_i():
    log_request()
    return jsonify(
        id=current_user.id,
        full_name=current_user.full_name,
        username=current_user.username,
    )


@app.route('/protected', methods=['GET', 'POST'])
@jwt_required()
def protected():
    log_request()
    return jsonify(hello='world')


@app.route('/transactions', methods=['GET'])
@jwt_required()
def list_transctions():
    log_request()
    transactions = UnitApi().list_transactions()
    return jsonify(data=transactions)


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)
