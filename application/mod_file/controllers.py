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
    # return jsonify(files=files)
    return render_template('file_index.html', files=files)



# @flask_login.login_required
@mod_file.route('/upload', methods=['POST'])
def upload_file():

    uploaded_file = request.files['file']

    
    file_size = get_file_size(uploaded_file)

    filename = secure_filename(uploaded_file.filename)

    file_ext = filename.split('.')
    file_ext = file_ext[-1]

    uploaded_file.save(f'application/file_bank{get_file_type_dir(filename)}/ {filename}')
    return 'pass'

    if filename != '':
        
        if file_ext.lower() not in app.config['UPLOAD_EXTENSIONS']:
            flash('This file type is not supported')
            abort(400)
        uploaded_file.save(
                os.path.join(f'application/file_bank{get_file_type_dir(filename)}', filename)
            )
        save_file_info(filename, file_ext, file_size)
        
        flash('File Uploaded Successfully')
    
        return redirect(url_for('mod_file.index'))
    else:

        flash("Error Occured")
    
        return redirect(url_for('mod_file.index'))




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


# from flask import Flask, make_response, request, session, render_template, \
#     send_file, Response, Blueprint
# from flask.views import MethodView
# from werkzeug import secure_filename
# from datetime import datetime
# import humanize
# import os
# import re
# import stat
# import json
# import mimetypes
# import sys
# from pathlib2 import Path



# mod_file = Blueprint('mod_file', __name__, url_prefix='/file',\
#      template_folder='templates/mod_file/',static_url_path='/assets', static_folder='assets')

# root = os.path.normpath("/tmp")
# key = ""

# ignored = ['.bzr', '$RECYCLE.BIN', '.DAV', '.DS_Store', '.git', '.hg', '.htaccess', '.htpasswd', '.Spotlight-V100', '.svn', '__MACOSX', 'ehthumbs.db', 'robots.txt', 'Thumbs.db', 'thumbs.tps']
# datatypes = {'audio': 'm4a,mp3,oga,ogg,webma,wav', 'archive': '7z,zip,rar,gz,tar', 'image': 'gif,ico,jpe,jpeg,jpg,png,svg,webp', 'pdf': 'pdf', 'quicktime': '3g2,3gp,3gp2,3gpp,mov,qt', 'source': 'atom,bat,bash,c,cmd,coffee,css,hml,js,json,java,less,markdown,md,php,pl,py,rb,rss,sass,scpt,swift,scss,sh,xml,yml,plist', 'text': 'txt', 'video': 'mp4,m4v,ogv,webm', 'website': 'htm,html,mhtm,mhtml,xhtm,xhtml'}
# icontypes = {'fa-music': 'm4a,mp3,oga,ogg,webma,wav', 'fa-archive': '7z,zip,rar,gz,tar', 'fa-picture-o': 'gif,ico,jpe,jpeg,jpg,png,svg,webp', 'fa-file-text': 'pdf', 'fa-film': '3g2,3gp,3gp2,3gpp,mov,qt', 'fa-code': 'atom,plist,bat,bash,c,cmd,coffee,css,hml,js,json,java,less,markdown,md,php,pl,py,rb,rss,sass,scpt,swift,scss,sh,xml,yml', 'fa-file-text-o': 'txt', 'fa-film': 'mp4,m4v,ogv,webm', 'fa-globe': 'htm,html,mhtm,mhtml,xhtm,xhtml'}

# @mod_file.template_filter('size_fmt')
# def size_fmt(size):
#     return humanize.naturalsize(size)

# @mod_file.template_filter('time_fmt')
# def time_desc(timestamp):
#     mdate = datetime.fromtimestamp(timestamp)
#     str = mdate.strftime('%Y-%m-%d %H:%M:%S')
#     return str

# @mod_file.template_filter('data_fmt')
# def data_fmt(filename):
#     t = 'unknown'
#     for type, exts in datatypes.items():
#         if filename.split('.')[-1] in exts:
#             t = type
#     return t

# @mod_file.template_filter('icon_fmt')
# def icon_fmt(filename):
#     i = 'fa-file-o'
#     for icon, exts in icontypes.items():
#         if filename.split('.')[-1] in exts:
#             i = icon
#     return i

# @mod_file.template_filter('humanize')
# def time_humanize(timestamp):
#     mdate = datetime.utcfromtimestamp(timestamp)
#     return humanize.naturaltime(mdate)

# def get_type(mode):
#     if stat.S_ISDIR(mode) or stat.S_ISLNK(mode):
#         type = 'dir'
#     else:
#         type = 'file'
#     return type

# def partial_response(path, start, end=None):
#     file_size = os.path.getsize(path)

#     if end is None:
#         end = file_size - start - 1
#     end = min(end, file_size - 1)
#     length = end - start + 1

#     with open(path, 'rb') as fd:
#         fd.seek(start)
#         bytes = fd.read(length)
#     assert len(bytes) == length

#     response = Response(
#         bytes,
#         206,
#         mimetype=mimetypes.guess_type(path)[0],
#         direct_passthrough=True,
#     )
#     response.headers.add(
#         'Content-Range', 'bytes {0}-{1}/{2}'.format(
#             start, end, file_size,
#         ),
#     )
#     response.headers.add(
#         'Accept-Ranges', 'bytes'
#     )
#     return response

# def get_range(request):
#     range = request.headers.get('Range')
#     m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
#     if m:
#         start = m.group('start')
#         end = m.group('end')
#         start = int(start)
#         if end is not None:
#             end = int(end)
#         return start, end
#     else:
#         return 0, None

# @mod_file.route('/', methods=['GET'])
# def get():
#     hide_dotfile = request.args.get('hide-dotfile', request.cookies.get('hide-dotfile', 'no'))
#     path = os.path.join(root, p)
#     if os.path.isdir(path):
#         contents = []
#         total = {'size': 0, 'dir': 0, 'file': 0}
#         for filename in os.listdir(path):
#             if filename in ignored:
#                 continue
#             if hide_dotfile == 'yes' and filename[0] == '.':
#                 continue
#             filepath = os.path.join(path, filename)
#             stat_res = os.stat(filepath)
#             info = {}
#             info['name'] = filename
#             info['mtime'] = stat_res.st_mtime
#             ft = get_type(stat_res.st_mode)
#             info['type'] = ft
#             total[ft] += 1
#             sz = stat_res.st_size
#             info['size'] = sz
#             total['size'] += sz
#             contents.append(info)
#         page = render_template('index.html', path=p, contents=contents, total=total, hide_dotfile=hide_dotfile)
#         res = make_response(page, 200)
#         res.set_cookie('hide-dotfile', hide_dotfile, max_age=16070400)
#     elif os.path.isfile(path):
#         if 'Range' in request.headers:
#             start, end = get_range(request)
#             res = partial_response(path, start, end)
#         else:
#             res = send_file(path)
#             res.headers.add('Content-Disposition', 'attachment')
#     else:
#         res = make_response('Not found', 404)
#     return res

# def put(self, p=''):
#     if request.cookies.get('auth_cookie') == key:
#         path = os.path.join(root, p)
#         dir_path = os.path.dirname(path)
#         Path(dir_path).mkdir(parents=True, exist_ok=True)
#         info = {}
#         if os.path.isdir(dir_path):
#             try:
#                 filename = secure_filename(os.path.basename(path))
#                 with open(os.path.join(dir_path, filename), 'wb') as f:
#                     f.write(request.stream.read())
#             except Exception as e:
#                 info['status'] = 'error'
#                 info['msg'] = str(e)
#             else:
#                 info['status'] = 'success'
#                 info['msg'] = 'File Saved'
#         else:
#             info['status'] = 'error'
#             info['msg'] = 'Invalid Operation'
#         res = make_response(json.JSONEncoder().encode(info), 201)
#         res.headers.add('Content-type', 'application/json')
#     else:
#         info = {} 
#         info['status'] = 'error'
#         info['msg'] = 'Authentication failed'
#         res = make_response(json.JSONEncoder().encode(info), 401)
#         res.headers.add('Content-type', 'application/json')
#     return res


# def post(self, p=''):
#     if request.cookies.get('auth_cookie') == key:
#         path = os.path.join(root, p)
#         Path(path).mkdir(parents=True, exist_ok=True)
#         info = {}
#         if os.path.isdir(path):
#             files = request.files.getlist('files[]')
#             for file in files:
#                 try:
#                     filename = secure_filename(file.filename)
#                     file.save(os.path.join(path, filename))
#                 except Exception as e:
#                     info['status'] = 'error'
#                     info['msg'] = str(e)
#                 else:
#                     info['status'] = 'success'
#                     info['msg'] = 'File Saved'
#         else:
#             info['status'] = 'error'
#             info['msg'] = 'Invalid Operation'
#         res = make_response(json.JSONEncoder().encode(info), 200)
#         res.headers.add('Content-type', 'application/json')
#     else:
#         info = {} 
#         info['status'] = 'error'
#         info['msg'] = 'Authentication failed'
#         res = make_response(json.JSONEncoder().encode(info), 401)
#         res.headers.add('Content-type', 'application/json')
#     return res

# def delete(self, p=''):
#     if request.cookies.get('auth_cookie') == key:
#         path = os.path.join(root, p)
#         dir_path = os.path.dirname(path)
#         Path(dir_path).mkdir(parents=True, exist_ok=True)
#         info = {}
#         if os.path.isdir(dir_path):
#             try:
#                 filename = secure_filename(os.path.basename(path))
#                 os.remove(os.path.join(dir_path, filename))
#                 os.rmdir(dir_path)
#             except Exception as e:
#                 info['status'] = 'error'
#                 info['msg'] = str(e)
#             else:
#                 info['status'] = 'success'
#                 info['msg'] = 'File Deleted'
#         else:
#             info['status'] = 'error'
#             info['msg'] = 'Invalid Operation'
#         res = make_response(json.JSONEncoder().encode(info), 204)
#         res.headers.add('Content-type', 'application/json')
#     else:
#         info = {}
#         info['status'] = 'error'
#         info['msg'] = 'Authentication failed'
#         res = make_response(json.JSONEncoder().encode(info), 401)
#         res.headers.add('Content-type', 'application/json')
#     return res

# path_view = PathView.as_view('path_view')
# app.add_url_rule('/', view_func=path_view)
# app.add_url_rule('/<path:p>', view_func=path_view)

# # if __name__ == '__main__':
# #     bind = os.getenv('FS_BIND', '0.0.0.0')
# #     port = os.getenv('FS_PORT', '8000')
# #     root = os.path.normpath(os.getenv('FS_PATH', '/tmp'))
# #     key = os.getenv('FS_KEY')
# #     app.run(bind, port, threaded=True, debug=False)