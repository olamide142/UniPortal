from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from application import db, app
import flask_login
from .forms import *
from application.mod_auth.models import *
from application.mod_auth.controllers import *
from application.mod_chat.models import * 


mod_chat = Blueprint('mod_chat', __name__, url_prefix='/chat',\
     template_folder='templates/')



@mod_chat.route('/', methods=['GET'])
@flask_login.login_required
def index():
    return render_template(
        'chat/index.html',
        current_user = str(flask_login.current_user))




@mod_chat.route('/search_user/', methods=['GET'])
@flask_login.login_required
def search_user():
    user = request.args['user'].lower()
    u = User.query.all()
    if len(user.strip()) == 0:
        return jsonify(data=[])
    # TODO: Refactor this to use filter lambda function
    # to extract users that fit criteria
    s = []
    for i in u:
        if (user in i.username.lower()) or (user in i.email.lower()) or \
            (user in i.first_name.lower())  or (user in i.last_name.lower()) :
            s.append((i.username, 
            get_fullname(i.username),
            i.email))
    return jsonify(data=s)



@mod_chat.route('/get_messages/', methods=['GET'])
@flask_login.login_required
def get_messages():
    current_user = str(flask_login.current_user)
    room = request.args['room']
    chat_id = get_chat_id(room)
    messages = Message.query.filter_by(chat_id=chat_id)
    data = []
    for i in messages:
        stat = ''
        if i.username == current_user:
            stat = 'odd'
        data.append((i.username, stat, i.content, i.created_on))
    return jsonify(data = data)




@mod_chat.route('/get_all_messages/', methods=['GET'])
@flask_login.login_required
def get_all_messages():
    # Get all chat ids that has this current user
    # and also get the receiver
    chat_ids = []
    receiver = []
    current_user = str(flask_login.current_user)
    for i in Chat.query.all():
        if i.user1 == current_user:
            receiver.append(i.user2)
            chat_ids.append(i.chat_id)
        elif i.user2 == current_user:
            receiver.append(i.user1)
            chat_ids.append(i.chat_id)
    # Get all the last messages 
    last_messages = []
    for i in chat_ids:
        m = Message.query.filter_by(chat_id = i).all()
        last_messages.append(m[-1].content)
    
    data = []
    le = 0 

    for i in receiver:
        data.append((i, last_messages[le]))

    return jsonify(data = data)




def new_chat(room):
    users = room.split('-')
    # Check if that chat already exist
    c = Chat.query.filter_by(user1=users[0], user2=users[1]).first()
    if c is None:
        c = Chat(users[0], users[1])
        db.session.add(c)
        db.session.commit()
        return c.chat_id
    else:
        return c.chat_id

def get_chat_id(room):
    users = room.split('-')
    c = Chat.query.filter_by(user1=users[0], user2=users[1]).first()
    if c is not None:
        return c.chat_id
    else:
        raise Exception

def save_msg(chat_id, msg):
    m = Message(chat_id, str(flask_login.current_user), msg)
    db.session.add(m)
    db.session.commit()
    return True


