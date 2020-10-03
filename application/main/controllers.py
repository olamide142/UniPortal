from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from werkzeug.security import check_password_hash
from application.mod_auth.models import User
from application.mod_auth.controllers import get_user_object
from application import db, app
import flask_login


mod_main = Blueprint('mod_main', __name__, url_prefix='/',\
     template_folder='templates/')

@mod_main.route('/', methods=['GET'])
def index():
    if flask_login.current_user is not '':
        return redirect(url_for('mod_main.dashboard'))
    else:
        return render_template('index.html')


@flask_login.login_required
@mod_main.route('/dashboard/', methods=['GET'])
def dashboard():
    return render_template('dashboard/index.html')

