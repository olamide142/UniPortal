from flask import Blueprint, request, render_template, flash, \
    g, session, redirect, url_for, jsonify, abort, url_for, make_response
from werkzeug.security import check_password_hash
from application.mod_auth.models import User
from application import db, app
import flask_login
from .forms import *

# Login manger setup
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('mod_auth', __name__, url_prefix='/auth',\
     template_folder='templates/mod_auth')
login_manager.login_view = "mod_auth.signin"


@mod_auth.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Set the route and accepted methods
@mod_auth.route('/signup/', methods=['POST'])
def signup():
    '''
    Register a user onto the platform
    returns: flask.jsonify()
    '''
    form = SignupForm(meta={'csrf': False})

    if form.validate_on_submit():
        try:
            user = User(form.username.data, form.email.data, form.password.data, \
                form.first_name.data, form.last_name.data)
            db.session.add(user)
            db.session.commit()
        except Exception:
            return jsonify(status=False, error="Account Creation was Unsuccessfull")
        return jsonify(status=True, msg="Account Created Successfully")
    else:
        return jsonify(status=False, error="Form submitted was invalid")


@mod_auth.route('/signin/', methods=['POST'])
def signin():
    '''
    Validate a username and password and 
    Sign the user in
    returns: flask.jsonify() || flask.render_template
    '''
    form = SigninForm(meta={'csrf': False})
    next,msg = None, ''
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if (user is not None) and \
            (check_password_hash(user.password, form.password.data)):
            flask_login.login_user(user)
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            msg = 'Logged in Successfully.'

            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
        
        else:
            msg = 'Username or Password was incorrect.'
        return jsonify(next=next or url_for('mod_auth.index'), msg=msg)

    else:
        msg = 'Form submitted was invalid'

    return jsonify(msg=msg)


@flask_login.login_required
@mod_auth.route('/signout/')
def logout():
    user = User.query.filter_by(username=\
        flask_login.current_user.username).first()
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    flask_login.logout_user()
    flash('Successfully Logged Out')
    return render_template('index.html')



@flask_login.login_required
@mod_auth.route('/see/', methods=['GET'])
def see():
    return 'Done in see'
    return redirect(url_for('mod_auth.index'))


def is_safe_url(target):
    '''
    Validates a redirection url to make sure 
    it is going to the same domain as the app
    params: target (str)
    '''
    from urllib.parse import urlparse, urljoin
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc