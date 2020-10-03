# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

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
    return 'not found', 404
    # return render_template('404.html'), 404

from application.mod_auth.controllers import mod_auth as auth_module
from application.mod_file.controllers import mod_file as file_system_module
from application.mod_module.controllers import mod_module as module
from application.main.controllers import mod_main as main_module
from application.mod_notification.controllers import mod_notification as notification


# Register blueprint(s)
app.register_blueprint(main_module)
app.register_blueprint(auth_module)
app.register_blueprint(file_system_module)
app.register_blueprint(module)
app.register_blueprint(notification)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

# Helps with displaying file uploads
from werkzeug.middleware.shared_data import SharedDataMiddleware
app.add_url_rule('/file/uploads/<filename>', 'uploaded_file',build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/file/uploads': app.config['UPLOAD_PATH']})
