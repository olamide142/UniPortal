from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from werkzeug.security import check_password_hash
from application.mod_module.models import Module, ClassRoom
from application.mod_auth.models import User
from application.mod_auth.controllers import get_user_object
from application.mod_notification.controllers import set_notification, NotificationType
from application import db, app
import flask_login
from .forms import *


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_module = Blueprint('mod_module', __name__, url_prefix='/module',\
     template_folder='templates/mod_module')


@mod_module.route('/', methods=['GET'])
def index():
    return render_template('module_index.html')

@flask_login.login_required
@mod_module.route('/create/', methods=['POST'])
def create():
    # form = CreateModuleForm(meta={'csrf_token':False})
    try:
        for i in range(100):
            print(f'{flask_login.current_user}')
        m = Module(request.form['name'],
        str(flask_login.current_user),
        request.form['session'],
        request.form['description'],
        request.form['code'])

        db.session.add(m)
        db.session.commit()
        flash("Module Created Successfully")
        return redirect(f'/module/view/{m.module_id}/')
    except Exception as ex:
        flash("Something went wrong, please try again")
        return redirect(url_for('mod_module.index'))


@flask_login.login_required
@mod_module.route('/view/<module_id>/', methods=['GET'])
def view(module_id):
    m = Module.query.filter_by(module_id=module_id).first()

    if m is None:
        redirect(url_for('not_found'))
    else:
        return jsonify(
            module_id = module_id,
            module_name = m.module_name,
            module_tutor_id = m.module_tutor_id,
            session = m.session,
            description = m.description,
            module_code = m.module_code,
            created_on = m.created_on
        )


@flask_login.login_required
@mod_module.route('/<module_id>/add/', methods=['POST'])
def add_student(module_id):
    user_making_the_addition = \
        get_user_object(str(flask_login.current_user))
    user_to_be_added = \
        get_user_object(request.form['username'])

    module = get_module_object(module_id)


    if (user_to_be_added is not None):
        # module leader cannot add himself to the module
        # since he owns the module
        if module.module_tutor_id == user_to_be_added.username:
            return 'Error encountered'


        if user_making_the_addition is user_to_be_added:
            # When Students joins a class by himself
            if not is_student_in_classroom(module_id, user_to_be_added.username):
                c = ClassRoom(module.module_id, user_to_be_added.username)
                db.session.add(c)
                db.session.commit()
                return jsonify(status='success')
            else:
                return "This student is already in this class"
        elif user_making_the_addition.username == module.module_tutor_id:
            # Tutor is adding student to a classroom
            # send invite that appears in the notifcation 
            # section of the student where they can accept 

            # TODO: call Notification system function to create
            # 'Add module' notification in student's db
            if set_notification(user_making_the_addition.username, \
                user_to_be_added.username, NotificationType.JoinModule):
                return jsonify("Notification will be sent to the student")
            else:
                return jsonify("Something Went Wrong")

    else:
        return jsonify(msg='Error encountered')



@mod_module.route('/<module_id>/members/', methods=['GET'])
def get_members(module_id):
    m = get_module_object(module_id)
    c = get_classroom_object(module_id)
    return jsonify(
        module_tutor = m.module_tutor_id,
        others = c
    )


def get_module_object(module_id):
    return Module.query.filter_by(module_id=module_id).first()

def get_classroom_object(module_id):
    return ClassRoom.query.filter_by(module_id=module_id)

def is_student_in_classroom(module_id, username):
    c = ClassRoom.query.filter_by(\
        module_id=module_id, student_username=username).first()
    if c is None:
        return False
    else:
        return True