# Import flask dependencies
from flask import Blueprint, request, render_template,flash, g, session, redirect, url_for, jsonify, abort, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash

# Import the database object from the main app module
from application import db, app


# Import flask_login for auth
import flask_login

# Import module models (i.e. User)
from application.mod_auth.models import User

# Login manger setup
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('mod_auth', __name__, url_prefix='/auth', template_folder='templates/mod_auth')
login_manager.login_view = "mod_auth.login"


@mod_auth.route('/index/', methods=['GET'])
@flask_login.login_required
def index():
    return render_template('index.html')


# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    user = User(username='olamide', email="foo@portal.com", password="password")
    db.session.add(user)
    db.session.commit()
    li = []
    for i in User.query.all():
        li.append(i.email)
    import json
    return json.dumps({'user':li})

@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():
    user = User.query.filter_by(username='olamide').first()
    flask_login.login_user(user)
    # user.authenticated = True
    next = request.args.get('next')
    
    if not is_safe_url(next):
        return abort(400)
    
    return redirect(next or url_for('index'))




def is_safe_url(target):
    from urllib.parse import urlparse, urljoin
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc