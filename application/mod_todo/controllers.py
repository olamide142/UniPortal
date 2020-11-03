from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from application import db, app
from werkzeug.security import check_password_hash
from application.mod_todo.models import Todo
from application.mod_auth.controllers import get_user_object
import flask_login

mod_todo = Blueprint('mod_todo', __name__, url_prefix='/todo',\
     template_folder='templates/')

@mod_todo.route('/', methods=['GET'])
@flask_login.login_required
def index():
    u = get_user_object(str(flask_login.current_user))
    todos = Todo.query.filter_by(owner_id=u.username)
    return render_template(
        'todo/index.html',
        todos=todos)



@mod_todo.route('/add/', methods=['GET'])
@flask_login.login_required
def add():
    data = request.args['data']
    u = get_user_object(str(flask_login.current_user))
    todo = Todo(u.username, data)
    db.session.add(todo)
    db.session.commit()
    return jsonify(
        data=True, 
        id=todo.todo_id)



@mod_todo.route('/crossoff/', methods=['GET'])
@flask_login.login_required
def crossoff():
    todo_id = request.args['todo_id']
    todo = Todo.query.filter_by(todo_id=todo_id).first()
    todo.status = 'checked'
    db.session.add(todo_id)
    db.session.commit()
    return jsonify(data=True)


@mod_todo.route('/remove/', methods=['GET'])
@flask_login.login_required
def remove():
    todo_id = request.args['todo_id']
    todo = Todo.query.filter_by(todo_id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return jsonify(data=True)




