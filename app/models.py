from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer  # NEW
from flask import current_app  # NEW

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    devices = db.relationship('Device', backref='owner', lazy=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirm_token = db.Column(db.String(100), unique=True)
    profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self, expires_sec=3600):  # NEW
        s = Serializer(current_app.config['SECRET_KEY'])  # NEW
        return s.dumps({'user_id': self.id})  # NEW

@staticmethod
def verify_reset_token(token, expires_sec=3600):  # NEW
    s = Serializer(current_app.config['SECRET_KEY'])  # NEW
    try:  # NEW
        user_id = s.loads(token, max_age=expires_sec)['user_id']  # NEW
    except Exception:  # NEW
            return None  # NEW
    return User.query.get(user_id)  # NEW

   
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean, default=False)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ip_address = db.Column(db.String(15))
    location = db.Column(db.String(100))
    last_active = db.Column(db.DateTime)
    settings = db.Column(db.JSON)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

