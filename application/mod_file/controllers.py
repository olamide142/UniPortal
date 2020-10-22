import os
import uuid
import flask_login
from .forms import FileForm
from application import db, app
from werkzeug.utils import secure_filename
from application.mod_file.models import FileSystem
from application.mod_calendar.models import gen_random_id
from flask import Blueprint, request, render_template, flash, make_response, \
    send_from_directory, g, session, redirect, url_for, jsonify, abort, url_for 



mod_file = Blueprint('mod_file', __name__, url_prefix='/file',\
     template_folder='templates/')

UPLOAD_FOLDER = 'application/file_bank/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'pptx', 'zip', 'mp4', 'md'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@mod_file.route('/')
@flask_login.login_required
def index():
    # files = os.listdir(app.config['UPLOAD_PATH']+'/images')
    # return jsonify(files=files)
    form = FileForm()
    return render_template('file/index.html', form=form)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



def upload_file(file):
    file = file
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = f'{gen_random_id()}{file.filename}'
        filename = filename.replace(' ', '_')
        f = FileSystem(filename, 
                        get_file_type(filename), '', 
                        str(flask_login.current_user))

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.add(f)
        db.session.commit()
        flash("File Uploaded Successfully")
        return True, f.file_id
    else:
        flash("File Upload Failed")
        return False, None



    
@mod_file.route('/uploads/<path:filename>', methods=['GET']) 
def download(filename):
    f = FileSystem.query.filter_by(file_name=filename).first()
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


def get_file_type(filename):
    ext = filename.split('.')
    return ext[-1]


def get_file_name(file_id):
    f = FileSystem.query.filter_by(\
        file_id=file_id).first()
    if f is not None:
        name = f.file_name.split('.')
        return  str(name[0][0:7].lower()), str(name[0][7:]), name[-1]
    else:
        return
    

def delete_file(filename):
    uploads = os.path.join(app.root_path, f"file_bank\\{filename}")
    os.remove(path=uploads)