from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from werkzeug.security import check_password_hash
from application.mod_auth.models import User
from application.mod_auth.controllers import get_user_object
from application.mod_module.forms import CreateModuleForm
from application.mod_module.controllers import get_modules
from application import db, app
import flask_login

mod_main = Blueprint('mod_main', __name__, url_prefix='/',\
     template_folder='templates/')

@mod_main.route('/', methods=['GET'])
def index():

    if 'flask_login.mixins.AnonymousUserMixin' in str(flask_login.current_user):
        # Couldn't figure out a better way to do this
        return render_template('index.html')
    else:
        return redirect(url_for('mod_main.dashboard'))


@mod_main.route('/dashboard/', methods=['GET'])
@flask_login.login_required
def dashboard():
    create_form = CreateModuleForm()
    
    return render_template(
        'dashboard/index.html',
        create_form=create_form,
        modules = get_modules(),
        current_user = str(flask_login.current_user))


@mod_main.route('/profile/', methods=['GET'])
@flask_login.login_required
def profile():
    return render_template(
        'profile/index.html',
        current_user=str(flask_login.current_user)
        )
