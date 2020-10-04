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
     template_folder='templates/')
login_manager.login_view = "mod_auth.index"
login_manager.login_message = "Please log in to access this page"


@mod_auth.route('/', methods=['GET'])
def index():
    form1 = SigninForm()
    form2 = SignupForm()
    return render_template(
        'auth/auth.html',
        form1=form1,
        form2=form2
    )



# Set the route and accepted methods
@mod_auth.route('/signup/', methods=['POST'])
def signup():
    '''
    Register a user onto the platform
    returns: flask.jsonify()
    '''
    form = SignupForm(meta={'csrf': True})

    if form.validate_on_submit():
        try:
            user = User(form.signup_username.data, form.signup_email.data, form.signup_password.data, \
                form.signup_firstname.data, form.signup_lastname.data)
            db.session.add(user)
            db.session.commit()
            flash("Account Created Successfully")
            return redirect(url_for('mod_main.dashboard'))
        except Exception:
            flash("Account Creation was Unsuccessfull")
    else:
        flash("Form submitted was invalid")
    
    return redirect(url_for('mod_auth.index'))



@mod_auth.route('/signin/', methods=['POST'])
def signin():
    '''
    Validate a username and password and 
    Sign the user in
    returns: flask.jsonify() || flask.render_template
    '''
    form = SigninForm(meta={'csrf_token':True})
    next,msg = None, ''

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login_username.data).first()

        if (user is not None) and \
            (check_password_hash(user.password, form.login_password.data)):
            flask_login.login_user(user, remember=True)
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            msg = 'Logged in Successfully.'

            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
        
        else:
            msg = 'Username or Password was incorrect.'
        return redirect(next or url_for('mod_main.index'))

    else:
        msg = 'Form submitted was invalid'

    return jsonify(msg=msg)


@mod_auth.route('/signout/', methods=['GET'])
@flask_login.login_required
def signout():
    '''
    Sign a user out from the platform 
    returns: flask.render_template()
    '''
    user = User.query.filter_by(username=\
        flask_login.current_user.username).first()
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    flask_login.logout_user()
    flash('Successfully Logged Out.')
    
    return redirect(url_for('mod_main.index'))



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



def get_user_object(username):
    '''
    Returns a user object
    returns: User
    '''
    return User.query.filter_by(username=username).first()