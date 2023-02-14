from flask_bcrypt import Bcrypt
from flask_jwt import JWT, jwt_required, current_identity, _default_jwt_payload_handler
from models import User

bcrypt = Bcrypt()


def authenticate(username, password):
    user = User.query.filter_by(username=username).scalar()
    if user and bcrypt.check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return User.query.filter_by(id=user_id).scalar()


jwt = JWT(authentication_handler=authenticate, identity_handler=identity)


def payload_callback(identity):
    payload = _default_jwt_payload_handler(identity)
    payload["is_admin"] = identity.is_admin
    return payload


jwt.jwt_payload_callback = payload_callback
