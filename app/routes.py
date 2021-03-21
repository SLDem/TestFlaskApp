from app import app, db
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm, ToDoListForm, TaskForm
from app.models import User, ToDoList, Task


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = None
    return render_template('index.html', username=username)


@app.route('/todolists')
def todolists():
    todolists = current_user.todolists
    return render_template('todolists.html', todolists=todolists)


@app.route('/todolist/<id>')
def todolist(id):
    todolist = ToDoList.query.filter_by(id=id).first()
    tasks = todolist.tasks
    return render_template('todolist.html', todolist=todolist, tasks=tasks)


@app.route('/add_todolist', methods =['POST', 'GET'])
def add_todolist():
    form = ToDoListForm()
    if form.validate_on_submit():
        todolist = ToDoList(name=form.name.data,
                            description=form.description.data,
                            todolist_owner=current_user)
        db.session.add(todolist)
        db.session.commit()
        return redirect(url_for('todolist', id=todolist.id))
    return render_template('add_todolist.html', form=form)


@app.route('/remove_todolist/<id>')
def remove_todolist(id):
    todolist = ToDoList.query.filter_by(id=id).first()
    tasks = todolist.tasks
    db.session.delete(todolist)
    for task in tasks:
        db.session.delete(task)
    db.session.commit()
    return redirect(url_for('todolists'))


@app.route('/add_task/<id>', methods=['POST', 'GET'])
def add_task(id):
    todolist = ToDoList.query.filter_by(id=id).first()
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data,
                    description=form.description.data,
                    deadline=form.deadline.data,
                    task_owner=current_user,
                    todolist=todolist,
                    is_completed=False)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('todolist', id=todolist.id))
    return render_template('add_task.html', todolist=todolist, form=form)


@app.route('/remove_task/<id>')
def remove_task(id):
    task = Task.query.filter_by(id=id).first()
    todolist = task.todolist_id
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('todolist', id=todolist))


@app.route('/change_task_status/<id>')
def change_task_status(id):
    task = Task.query.filter_by(id=id).first()
    todolist = task.todolist_id
    if task.is_completed:
        task.is_completed = False
        db.session.commit()
    else:
        task.is_completed = True
        db.session.commit()
    return redirect(url_for('todolist', id=todolist))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user is None:
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
