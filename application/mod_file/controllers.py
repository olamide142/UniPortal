import os
import uuid
import flask_login
from .forms import FileForm
from application import db, app
from werkzeug.utils import secure_filename
from application.mod_file.models import FileSystem
from flask import Blueprint, request, render_template, flash, make_response, \
    send_from_directory, g, session, redirect, url_for, jsonify, abort, url_for 



mod_file = Blueprint('mod_file', __name__, url_prefix='/file',\
     template_folder='templates/mod_file/')


@mod_file.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH']+'/images')
    return render_template('file_index.html', files=files)
    # return jsonify(files=files)



# @flask_login.login_required
@mod_file.route('/upload', methods=['POST'])
def upload_file():

    uploaded_file = request.files['file']
    
    file_size = get_file_size(uploaded_file)

    filename = secure_filename('ooo.jpg')


    if filename != '':
        
        file_ext = os.path.splitext(filename)[1]
        if file_ext.lower() not in app.config['UPLOAD_EXTENSIONS']:
            flash('This file type is not supported')
            abort(400)
        if uploaded_file.save(os.path.join(app.config['UPLOAD_PATH']+ get_file_type_dir(filename),\
             filename)):
            flash('File Uploaded Successfully')
        else:
            # delete file and clear db for file name if something
            # upload did not succed
            flash('Something went wrong please try again')
    
        return redirect(url_for('mod_file.index'))
    else:

        flash("Error Occured")
    
        return redirect(url_for('mod_file.index'))




@mod_file.route('/uploads/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    file_type_dir = get_file_type_dir(filename)
    return send_from_directory(app.config['UPLOAD_PATH']+file_type_dir, filename)



def save_file_info(filename, file_type, file_size):
    try:
        file = FileSystem(
            filename, 
            file_type, 
            file_size, 
            str(flask_login.current_user))
        
        db.session.add(file)
        db.session.commit()
        return True
    except Exception:
        return False



def get_file_size(file):
    file.seek(0, os.SEEK_END)
    return file.tell()


def get_file_type_dir(filename):
    ext = filename.split('.')

    file_type_dir = ''

    if ext[-1].lower() in ['png', 'jpg', 'jpeg', 'gif']:
        file_type_dir = '/images'
    elif ext[-1].lower() in ['txt', 'pdf', '.doc', '.docx']:
        file_type_dir = '/docs'
    else:
        file_type_dir = '/others'
    
    return file_type_dir
