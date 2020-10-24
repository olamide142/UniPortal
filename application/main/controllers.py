from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from werkzeug.security import check_password_hash
from application.mod_auth.models import User
from application.mod_auth.controllers import get_user_object, get_fullname
from application.mod_module.forms import CreateModuleForm
from .forms import *
from application.mod_module.models import *
from application.mod_module.controllers import get_modules, get_quotes
from application import db, app, socketio
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
        current_user = str(flask_login.current_user),
        random_quote = get_quotes())


@mod_main.route('/profile/', methods=['GET'])
@flask_login.login_required
def profile():
    current_user=str(flask_login.current_user)
    mdoule_in_as_student, mdoule_in_as_tutor = get_number_of_module_in(current_user)
    info = User.query.filter_by(username=current_user).first()


    return render_template(
        'profile/index.html',
        current_user=current_user,
        mdoule_in_as_student = mdoule_in_as_student,
        mdoule_in_as_tutor = mdoule_in_as_tutor,
        email = info.email,
        joined_on = info.created_on.date(),
        profileForm = ProfileForm(),
        info = info)


@mod_main.route('/edit_profile/', methods=['POST'])
@flask_login.login_required
def edit_profile():
    form = ProfileForm(meta={'csrf_token' : True})
    if form.validate_on_submit():
        firstname = form.data.firstname
        lastname = form.data.lastname


    








@mod_main.route('/search_student/', methods=['GET'])
@flask_login.login_required
def search_student():
    student = request.args['student'].lower()
    u = User.query.all()
    if len(student.strip()) == 0:
        return jsonify(data=[])
    # TODO: Refactor this to use filter lambda function
    # to extract users that fit criteria
    s = []
    for i in u:
        if (student in i.username.lower()) or (student in i.email.lower()):
            s.append((i.username, 
            get_fullname(i.username),
            i.email))
    return jsonify(data=s)





def get_number_of_module_in(current_user):
    mdoule_in_as_student = 0
    mdoule_in_as_tutor = 0
    for i in ClassRoom.query.filter_by(member_username=current_user):
        m = Module.query.filter_by(module_id=i.module_id).first()
        if i.member_username == m.module_tutor_id:
            mdoule_in_as_tutor += 1
        else:
            mdoule_in_as_student += 1
    
    return mdoule_in_as_student, mdoule_in_as_tutor
