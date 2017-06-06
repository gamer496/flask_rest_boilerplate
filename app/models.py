from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    id                          =db.Column(db.Integer, primary_key = True)
    username                    =db.Column(db.String(250), nullable = False,
                                           unique = True, index = True)
    password                    =db.Column(db.String(250))


    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 2592000)
        return s.dumps({"id": self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = Nuser.query.get(data['id'])
        return user

    def __repr__(self):
        return "Nuser: %s"%(self.username)
