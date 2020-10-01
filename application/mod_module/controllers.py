from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from werkzeug.security import check_password_hash
from application.mod_module.models import Module, ClassRoom
from application.mod_auth.models import User
from application import db, app
import flask_login
from .forms import *


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_module = Blueprint('mod_module', __name__, url_prefix='/module',\
     template_folder='templates/mod_module')


@mod_module.route('/', methods=['GET'])
def index():
    return 'herehe rehrehrehr ehrer ojtoto ojoro'
    return render_template('module_index.html')

@mod_module.route('/create', methods=['POST'])
def create():

    form = CreateModuleForm(meta={'csrf_token':False})

    try:
        m = Module(request.form['name'],
        'fake_user', #flask_login.current_user,
        request.form['session'],
        request.form['description'],
        request.form['code'])

        db.session.add(m)
        db.session.commit()
        flash("Module Created Successfully")
        return redirect(f'/module/view/{m.module_id}')
    except Exception as ex:
        return str(ex)
        flash("Something went wrong, please try again")
        return redirect(url_for('mod_module.index'))


@mod_module.route('/view/<module_id>', methods=['GET'])
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


@mod_module.route('/<module_id>/add', methods=['POST'])
def add_student(module_id):
    username = request.form['username']
    current_user = 'test'

    u = User.query.filter_by(username=username).first()
    m = get_module_object(module_id)


    if (u is not None):
        if current_user is u.username:
            # When Students joins a class
            c = ClassRoom(m.module_id, u.username)
            db.session.add(c)
            db.session.commit()
        elif current_user.user_id is m.module_tutor_id:
            # Tutor is adding student to a classroom
            # send invite that appears in the notifcation 
            # section of the student where they can accept 
            pass



@mod_module.route('/<module_id>/members', methods=[GET])
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

