from flask_jwt_extended import create_access_token
from app.models import User
from app.security import verify_password

def authenticate(username: str, password: str):
    user = User.query.filter_by(username=username).first()

    if user and verify_password(password, user.password_hash):
        return create_access_token(identity=username)

    return None
