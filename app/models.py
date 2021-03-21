from app import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))

    todolists = db.relationship('ToDoList', backref='todolist_owner', lazy=True)
    tasks = db.relationship('Task', backref='task_owner', lazy=True)

    def __repr__(self):
        return self.username


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


class ToDoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(64))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tasks = db.relationship('Task', backref='todolist', lazy=True)

    def __repr__(self):
        return self.name


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    description = db.Column(db.String(246))
    is_completed = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    todolist_id = db.Column(db.Integer, db.ForeignKey('todolist.id'))

    def __repr__(self):
        return self.title
