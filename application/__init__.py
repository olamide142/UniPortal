# Import flask and template operators
from flask import Flask, render_template, session, copy_current_request_context

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import Flask-SocketIO 
from flask_socketio import SocketIO, emit, join_room, \
    leave_room, close_room, rooms, disconnect
from threading import Lock
async_mode = None

# Define the WSGI application object

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# Configurations
app.config.from_object('config')
# file configuration
app.config['UPLOAD_PATH'] = 'application/file_bank/'
app.config['UPLOAD_EXTENSIONS'] = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'zip', 'rar']

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from application.main.controllers import mod_main as main_module
from application.mod_auth.controllers import mod_auth as auth_module
from application.mod_file.controllers import mod_file as file_system_module
from application.mod_module.controllers import mod_module as module
from application.mod_notification.controllers import mod_notification as notification_module
from application.mod_calendar.controllers import mod_calendar as calendar_module
from application.mod_todo.controllers import mod_todo as todo_module
from application.mod_whiteboard.controllers import mod_whiteboard as whiteboard_module


# Register blueprint(s)
app.register_blueprint(main_module)
app.register_blueprint(auth_module)
app.register_blueprint(file_system_module)
app.register_blueprint(module)
app.register_blueprint(notification_module)
app.register_blueprint(calendar_module)
app.register_blueprint(todo_module)
app.register_blueprint(whiteboard_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

# Helps with displaying file uploads
from werkzeug.middleware.shared_data import SharedDataMiddleware
app.add_url_rule('/file/uploads/<filename>', 'uploaded_file',build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/file/uploads': app.config['UPLOAD_PATH']})






'''
    White Board Sockets Controllers
'''
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/theboard')

@socketio.on('connect', namespace='/theboard')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})



@socketio.on('join', namespace='/theboard')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})