from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from werkzeug.security import check_password_hash
from application.mod_module.models import *
from application.mod_auth.models import User
from application.mod_whiteboard.models import *
from application.mod_auth.controllers import get_user_object, get_fullname
from application.mod_notification.controllers import *
from application.mod_calendar.forms import CreateEventForm
from application.mod_calendar.models import *
from application.mod_file.controllers import *
from application.mod_file.forms import FileForm
from application import db, app
import flask_login
from .forms import *


mod_module = Blueprint('mod_module', __name__, url_prefix='/module',\
     template_folder='templates/')



@mod_module.route('/create/', methods=['POST'])
@flask_login.login_required
def create():
    form = CreateModuleForm(meta={'csrf_token':False})
    username = str(flask_login.current_user)
    try:
        if form.validate_on_submit():
            m = Module(form.name.data,
            username,
            form.session.data,
            form.description.data,
            form.code.data)
            c = ClassRoom(m.module_id, username)
            b = Board(username, form.name.data)
            db.session.add(c)
            db.session.add(b)
            db.session.add(m)
            db.session.commit()
            flash("Module Created Successfully")
            return redirect(f'/module/view/{m.module_id}/')
        else:
            flash("Submitted Form was Invalid")
            return redirect(f'/module/view/{m.module_id}/')

    except Exception as ex:
        flash("Something went wrong, please try again")
        return redirect(url_for('mod_main.index'))



@mod_module.route('/view/<module_id>/', methods=['GET'])
@flask_login.login_required
def view(module_id):
    m = Module.query.filter_by(module_id=module_id).first()

    # get the next event on the calendar
    events = Event.query.filter_by(module_id=module_id)
    try:
        next_event = events[0]
        for i in events:
            if next_event.date_n_time > i.date_n_time:
                next_event = i
    except IndexError:
        next_event = NoEvent

    if m is None:
        return redirect(url_for('not_found'))
    else:
        return render_template('module/index.html',
            editForm            = CreateModuleForm(),
            topicForm           = CreateTopicForm(),
            createEventForm     = CreateEventForm(),
            module_id           = module_id,
            module_name         = m.module_name,
            module_tutor_id     = m.module_tutor_id,
            session             = m.session,
            description         = m.description,
            module_code         = m.module_code,
            current_user        = str(flask_login.current_user),
            next_event          = next_event.date_n_time,
            next_event_title    = next_event.title
        )



@mod_module.route('/<module_id>/add/', methods=['GET'])
@flask_login.login_required
def add_student(module_id):
    user_making_the_addition = \
        get_user_object(str(flask_login.current_user))
    user_to_be_added = \
        get_user_object(request.args['student'])

    module = get_module_object(module_id)


    if (user_to_be_added is not None):
        # module leader cannot add himself to the module
        # since he owns the module
        if module.module_tutor_id == user_to_be_added.username:
            return jsonify(status= False,
            msg = "Error, You can not add your self as a student")

       #Check that student isn't already a member of the module
        if ClassRoom.query.filter_by(module_id=module_id, \
            member_username=user_to_be_added.username).first() is not None:
            return jsonify(status= False,
            msg = "Student is already registered in this Module")

        # Tutor is adding student to a classroom
        # send invite that appears in the notifcation 
        # section of the student where they can accept 
        if set_notification(user_making_the_addition.username, \
            user_to_be_added.username, NOTIFICATION_JOIN_MODULE, module.module_id):
            return jsonify(status = True,
            msg = "Notification has be sent to the student")
        else:
            return jsonify(status= False,
            msg = "Something Went Wrong")

    else:
        return jsonify(msg='Error encountered')



@mod_module.route('/<module_id>/members/', methods=['GET'])
@flask_login.login_required
def get_members(module_id):
    m = get_module_object(module_id)
    c = ClassRoom.query.filter_by(module_id=module_id)
    s = []
    for i in c:
        s.append(get_fullname(i.member_username))
    return jsonify(students = s)



def get_modules():
    # get modules this user is registered in
    c = ClassRoom.query.filter_by(\
        member_username=str(flask_login.current_user))

    # get modules created by this user
    modules = []
    for i in c:
        modules.append(Module.query.filter_by(module_id=i.module_id).first())
    return modules



@mod_module.route('/join_module/', methods=['GET'])
@flask_login.login_required
def join_module():
    # Generate ajax list
    username = str(flask_login.current_user)
    if request.args['action'] == "get_mod":
        text = request.args['data'].lower()
        if text.strip() == '':
            return jsonify(data=[])
        m = Module.query.all()
        s = []
        for i in m:
            if (text in (i.module_id).lower()) or (text in (i.module_name).lower()):
                s.append((i.module_name, i.module_id, get_fullname(i.module_tutor_id)))
        return jsonify(data = s)

    if request.args['action'] == "join":
        module_id = request.args['module_id']
        try:
            if ClassRoom.query.filter_by(\
                module_id=module_id, member_username = username).first() is None:
                c = ClassRoom(module_id, username)
                db.session.add(c)
                db.session.commit()
                return jsonify(msg="Success")
            else:
                return jsonify(msg="Error Occured")
        except Exception:
            return jsonify(msg="Error Occured")



@mod_module.route('/<module_id>/update/', methods=['POST'])
@flask_login.login_required
def update(module_id):
    form = CreateModuleForm(meta={'csrf_token':True})
    username = str(flask_login.current_user)
    try:
        if form.validate_on_submit():
            m = Module.query.filter_by(module_id=module_id).first()
            m.module_name   = form.name.data
            m.description   = form.description.data
            m.session       = form.session.data
            m.module_code   = form.code.data
            db.session.add(m)
            db.session.commit()
            flash("Module Updated Successfully")
            return redirect(f'/module/view/{m.module_id}/')
        else:
            flash("Submitted Form was Invalid")
            return redirect(f'/module/view/{m.module_id}/')

    except Exception as ex:
        flash("Something went wrong, please try again")
        return redirect(f'/module/view/{module_id}/')



@mod_module.route('/search_my_module/', methods=['GET'])
@flask_login.login_required
def search_my_module():
    '''
    User can search for a module by name, tutor's name,
    module_id.
    returns: flask.jsonify
    '''
    username = str(flask_login.current_user)
    text = request.args['data'].lower()
    m = ClassRoom.query.filter_by(member_username=username)
    s = []
    # return "olamide"
    for i in m:
        # get the module info
        module = Module.query.filter_by(module_id=i.module_id).first()
        if (text in (get_fullname(module.module_tutor_id).lower()) or\
             text in (module.module_id).lower()) or \
                 (text in (module.module_name).lower()):
            s.append((module.module_name,
            get_fullname(module.module_tutor_id),
            module.module_code,
            module.module_id
            ))
    return jsonify(data = s)



@mod_module.route('/<module_id>/create_subtopic/', methods=['POST'])
@flask_login.login_required
def create_subtopic(module_id):
    form = CreateTopicForm(meta={'csrf_token':True})
    if form.validate_on_submit():
        t = ModuleSub(module_id, form.title.data, form.description.data)
        db.session.add(t)
        db.session.commit()
        flash(f"{form.title.data} has been created Successfully")
        return redirect(f'/module/view/{module_id}')
    else:
        flash("Form submitted was Invalid")
        return redirect(f'/module/view/{module_id}')



@mod_module.route('/<module_id>/get_module_materials/', methods=['GET'])
@flask_login.login_required
def get_module_subs(module_id):
    # Get all Module_sub
    ms = ModuleSub.query.filter_by(\
        module_id=module_id)
        # Get each sub's description and materail info 
    data = []
    for i in ms:
        sub_mod_info = {}
        sub_mod_info['sub_name'] =  i.sub_name
        sub_mod_info['description'] =  i.description
        sub_mod_info['sub_id'] =  i.sub_id

        # # Get Materials for this sub module
        # mm = ModuleMaterial.query.filter_by(sub_id=i.sub_id)
        # sub_mod_info['files'] = []
        # for j in mm:
        #     sub_mod_info['files'].append(get_file_name(j.file_id))

        data.append(sub_mod_info)
    return jsonify(data=data)





@mod_module.route('/<module_id>/sub/<sub_id>/', methods=['GET'])
@flask_login.login_required
def get_module_sub_materials(module_id, sub_id):
    moduleSub = ModuleSub.query.filter_by(\
        module_id=module_id, sub_id=sub_id).first()
    
    mm = ModuleMaterial.query.filter_by(sub_id=sub_id)
    files = []
    for j in mm:
        files.append(get_file_name(j.file_id))
    return render_template(
        'module/sub.html',
        fileForm = FileForm(),
        moduleSub = moduleSub,
        files = files,
        module = Module.query.filter_by(module_id=module_id).first(),
        sub_id = sub_id,
        current_user = str(flask_login.current_user))




@mod_module.route('/<module_id>/sub/<sub_id>/upload_material/', methods=['POST'])
@flask_login.login_required
def upload_material(module_id, sub_id):
        file = request.files['file']
        status, file_id = upload_file(file)
        if status:
            m = ModuleMaterial(file_id, sub_id)
            db.session.add(m)
            db.session.commit()
        return redirect(f'/module/{module_id}/sub/{sub_id}/')
    # try:
    # except Exception:
        # return redirect(f'/module/{module_id}/sub/{sub_id}/')




@mod_module.route('/<module_id>/sub/<sub_id>/delete_material/', methods=['GET'])
@flask_login.login_required
def delete_material(module_id, sub_id):
    # Make sure logged in user is the creator of the file
    if get_module_object(module_id).module_tutor_id == str(flask_login.current_user):
        # Delete file from the File System and ModuleMaterial
        file_name = request.args['data']
        return str(file_name)
        f = FileSystem.query.filter_by(file_name=file_name).first()
        m = ModuleMaterial.query.filter_by(file_id=f.file_id).first()
        db.session.delete(f)
        db.session.delete(m)
        db.session.commit()
        # Delete the actual file
        delete_file(file_name)
        return jsonify(status = True)
    else:
        return jsonify(status = False)





def get_module_object(module_id):
    return Module.query.filter_by(module_id=module_id).first()



def get_classroom_object(module_id):
    return ClassRoom.query.filter_by(module_id=module_id)



def is_student_in_classroom(module_id, username):
    c = ClassRoom.query.filter_by(\
        module_id=module_id, member_username=username).first()
    if c is None:
        return False
    else:
        return True

