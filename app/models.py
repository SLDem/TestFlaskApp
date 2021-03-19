from app import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))

    def __repr__(self):
        return self.username


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()
