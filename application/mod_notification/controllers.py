from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from application import db, app
from werkzeug.security import check_password_hash
from application.mod_module.models import Module, ClassRoom
from application.mod_auth.models import User
from application.mod_notification.models import Notification
from application.mod_auth.controllers import get_user_object, get_fullname
import flask_login
from datetime import datetime

NOTIFICATION_JOIN_MODULE = 'NJM'
NOTIFICATION_MESSAGE_MODULE = 'NMM'

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_notification = Blueprint('mod_notification', __name__, url_prefix='/notification',\
     template_folder='templates/')




# content for join module
def get_NJM_content(sender, module, time, notification):
    return f"""<div class="curved-inner-pro" id="{notification.notification_id}">
                        <div class="curved-ctn">
                            <p class="w3-small w3-text-teal">from: Vestibulum</p>
                            <p>Invitation to Join Module</p>
                            <p class="lead">Module Name: {module.module_name}</p>
                            <p class="lead">Module Tutor: {get_fullname(module.module_tutor_id)} | Code: {module.module_code}</p>
                            <div class="btn-group notika-group-btn w3-right w3-small">
                                <br>
                                <button class="w3-button w3-teal w3-round btn-default notika-gp-default"
                                id="join{module.module_id}" onclick="joinModuleNotification('{module.module_id}')">Join</button>
                                <button id="decline_module_btn" onclick="deleteNotification('{notification.notification_id}')"
                                 class="w3-button w3-gray w3-round btn-default notika-gp-default">Decline</button>
                                <br><i class="w3-text-teal w3-small">{time}</i>
                            </div>
                        </div>
                    </div>
                """


@mod_notification.route('/', methods=['GET'])
@flask_login.login_required
def index():
    return render_template(
        'notification/index.html')




@mod_notification.route('/get_notifications/', methods=['GET'])
@flask_login.login_required
def get_notifications():
    notifications = Notification.query.filter_by(receiver = (str(flask_login.current_user)))
    s = []
    for i in notifications:
        s.append((i.sender, i.content, i.created_on, i.seen))
    return jsonify(notifications = s)


@mod_notification.route('/delete_notification/', methods=['GET'])
@flask_login.login_required
def delete_notification():
    try:
        n = Notification.query.filter_by(notification_id = request.args['nid']).first()
        db.session.delete(n)
        db.session.commit()
        return jsonify(status=True)
    except Exception:
        return False
    


def set_notification(sender, receiver, notification_type, module_id=None):
    try:
        n = Notification(
            sender, 
            receiver, 
            notification_type,
            ""
        )
        n.content = set_content(sender, notification_type,
            {'module_id':module_id, 'notification':n})
        for _ in range(100):
            print(sender, receiver, notification_type, module_id)
        db.session.add(n)
        db.session.commit()
        return True
    except Exception:
        return False


def set_content(sender, type, kwargs=None):
    if type == 'NJM':
        return get_NJM_content(
            sender, 
            Module.query.filter_by(module_id = kwargs['module_id']).first(),
            datetime.utcnow(),
            kwargs['notification']
            )
    else:
        pass
