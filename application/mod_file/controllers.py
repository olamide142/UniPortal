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
     template_folder='templates/')

UPLOAD_FOLDER = 'application/file_bank/docs/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

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


@mod_file.route('/upload', methods=['POST'])
@flask_login.login_required
def upload_file():
    
        file = request.files['file']
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "filename.pdf"))
            return redirect(url_for('mod_file.index'))
        else:
            flash("File upload Failed")
            return redirect(url_for('mod_file.index'))




# @mod_file.route('/upload/', methods=['GET'])
# # @flask_login.login_required
# def upload_file():

#     if request.method == 'GET':
#         if 'files' not in request.files:
#             return 'No file part'

#         file = request.files['files']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             return 'No selected file'

#         if file:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
#             return "Done!"

    # return str(get_file_size(request.args['filefile']))

    # if form.validate_on_submit() and form.file_.has_file():

    #     uploaded_file = form.file_.data

    #     file_size = get_file_size(uploaded_file)

    #     filename = secure_filename(uploaded_file.filename)

    #     file_ext = filename.split('.')
    #     file_ext = file_ext[-1]

    #     uploaded_file.save(f'application/file_bank{get_file_type_dir(filename)}/ {filename}')
    #     return 'pass'

    # if filename != '':
        
    #     if file_ext.lower() not in app.config['UPLOAD_EXTENSIONS']:
    #         flash('This file type is not supported')
    #         abort(400)
    #     uploaded_file.save(
    #             os.path.join(f'application/file_bank{get_file_type_dir(filename)}', filename)
    #         )
    #     save_file_info(filename, file_ext, file_size)
        
    #     flash('File Uploaded Successfully')
    
    #     return redirect(url_for('mod_file.index'))
    # else:

    #     flash("Error Occured")
    
    #     return redirect(url_for('mod_file.index'))




@mod_file.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    file_type_dir = get_file_type_dir(filename)
    for _ in range(10):
        print(file_type_dir,'-------------------------------------')
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
    elif ext[-1].lower() in ['txt', 'pdf', 'doc', 'docx']:
        file_type_dir = '/docs'
    else:
        file_type_dir = '/others'
    
    return file_type_dir