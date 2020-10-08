from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from application import db, app
from werkzeug.security import check_password_hash
from application.mod_todo.models import Todo
import flask_login

mod_todo = Blueprint('mod_todo', __name__, url_prefix='/todo',\
     template_folder='templates/')

@mod_todo.route('/', methods=['GET'])
@flask_login.login_required
def index():
    return render_template('todo/index.html')