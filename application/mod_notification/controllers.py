from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from application import db, app
from werkzeug.security import check_password_hash
from application.mod_module.models import Module, ClassRoom
from application.mod_auth.models import User
from application.mod_notification.models import Notification
from application.mod_auth.controllers import get_user_object
import flask_login
from enum import Enum, auto

class NotificationType(Enum):
    Todo            = auto()
    JoinModule      = auto()
    CommunityPost   = auto()
    Message         = auto()

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_notification = Blueprint('mod_notification', __name__, url_prefix='/notification',\
     template_folder='templates/mod_notification')

@mod_notification.route('/', methods=['GET'])
@flask_login.login_required
def index():
    notifications = get_notifications(str(flask_login.current_user))
    return jsonify(len_unseen=len(notifications))


def get_notifications(username, unseen=True):
    user = get_user_object(username)
    return Notification.query.filter_by(receiver=user.username, seen=seen)


def set_notification(sender, receiver, notification_type):
    try:
        n = Notification(
            sender, 
            receiver, 
            notification_type, 
            set_content()
        )
        db.session.add(n)
        db.session.commit()
        return True
    except Exception:
        return False